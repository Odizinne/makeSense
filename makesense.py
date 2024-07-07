import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, QPoint, QPointF, Qt
from PyQt6.QtGui import QCursor, QAction, QIcon
from design import Ui_MainWindow
from dualsense_controller import DualSenseController
import pyautogui
import winshell
import vgamepad as vg

class MakeSense(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("makeSense")
        self.setWindowIcon(QIcon('icon.png'))

        self.controller = None
        self.gamepad = None
        self.last_touch_position = None
        self.handle_touchpad_events = False
        self.hidhide_path = r"C:\Program Files\Nefarius Software Solutions\HidHide\x64\hidhidecli.exe"

        self.settings_file = os.path.join(os.getenv('APPDATA'), 'makesense', 'settings.json')
        self.load_settings()

        self.ui.applyButton.clicked.connect(self.set_lightbar_color)
        self.ui.touchpadBox.stateChanged.connect(self.handle_touchpad_state_change)
        self.ui.startupBox.stateChanged.connect(self.handle_startup_state_change)
        self.ui.emulateXboxBox.stateChanged.connect(self.handle_xbox_emulation_state_change)

        self.setup_timers()
        self.create_system_tray_icon()
        self.check_for_hidhide()
        self.check_for_controller()
        self.update_battery_level()
        self.handle_touchpad_state_change()
        self.check_startup_shortcut()
        self.set_lightbar_color()
        self.handle_xbox_emulation_state_change()

    def create_system_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))

        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def quit(self):
        self.stop_xbox_emulation()
        self.controller.deactivate()
        self.controller = None
        QApplication.quit()

    def setup_timers(self):
        self.battery_timer = QTimer(self)
        self.battery_timer.timeout.connect(self.update_battery_level)
        self.battery_timer.start(10000)
        self.device_check_timer = QTimer(self)
        self.device_check_timer.timeout.connect(self.check_for_controller)
        self.device_check_timer.start(3000)

    def toggle_ui_elements(self, show):
        elements_to_toggle = [
            self.ui.r,
            self.ui.g,
            self.ui.b,
            self.ui.rLabel,
            self.ui.gLabel,
            self.ui.bLabel,
            self.ui.batteryLabel,
            self.ui.batteryBar,
            self.ui.applyButton,
            self.ui.touchpadBox,
            self.ui.touchpadLabel,
            self.ui.startupBox,
            self.ui.startupLabel,
            self.ui.emulateXboxBox,
            self.ui.emulateXboxLabel
        ]
    
        for element in elements_to_toggle:
            element.setVisible(show)

        self.ui.notFoundLabel.setVisible(not show)

    def check_for_hidhide(self):
        if not os.path.exists(self.hidhide_path):
            self.ui.emulateXboxBox.setEnabled(False) 

    def handle_touchpad_state_change(self):
        if self.controller:
            self.controller.touch_finger_1.on_change(self.on_touchpad_change)
            self.controller.btn_touchpad.on_down(self.send_mouse_left_click_pressed)
            if self.ui.touchpadBox.isChecked():
                self.handle_touchpad_events = True
            else:
                self.handle_touchpad_events = False
        self.save_settings()

    def handle_startup_state_change(self):
        if self.ui.startupBox.isChecked():
            self.create_startup_shortcut()
        else:
            self.delete_startup_shortcut()
        self.save_settings()

    def handle_xbox_emulation_state_change(self):
        if self.ui.emulateXboxBox.isChecked():
            self.start_xbox_emulation()
        else:
            self.stop_xbox_emulation()
        self.save_settings()

    def get_device_instance_path(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        result = subprocess.run([self.hidhide_path, '--dev-gaming'], capture_output=True, text=True, startupinfo=startupinfo)
        
        data = json.loads(result.stdout)
        
        for device in data:
            if device.get('friendlyName') == "Sony Interactive Entertainment Wireless Controller":
                if device['devices'] and len(device['devices']) > 0:
                    device_instance_path = device['devices'][0].get('deviceInstancePath')
                    return device_instance_path
    
    def hide_dualsense_controller(self):
        executable_path = sys.executable
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        device_instance_path = self.get_device_instance_path()

        subprocess.run([self.hidhide_path, "--dev-hide", device_instance_path], startupinfo=startupinfo)
        subprocess.run([self.hidhide_path, "--app-reg", executable_path], startupinfo=startupinfo)
        subprocess.run([self.hidhide_path, "--cloak-on"], startupinfo=startupinfo)

    def show_dualsense_controller(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        device_instance_path = self.get_device_instance_path()

        subprocess.run([self.hidhide_path, "--dev-unhide", device_instance_path], startupinfo=startupinfo)
        subprocess.run([self.hidhide_path, "--cloak-off"], startupinfo=startupinfo)

    def rumble_callback(self, client, target, large_motor, small_motor, led_number, user_data):
        if self.controller:
            print(f"received rumble callback: {large_motor} and {small_motor}")
            self.controller.left_rumble.set(large_motor)
            self.controller.right_rumble.set(small_motor)

    def start_xbox_emulation(self):
        if self.controller is None:
            return
        self.hide_dualsense_controller()
        self.gamepad = vg.VX360Gamepad()
        def map_ds_to_xbox():
            if self.controller.btn_cross.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            else: 
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            if self.controller.btn_circle.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            if self.controller.btn_square.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            if self.controller.btn_triangle.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
            if self.controller.btn_l1.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            if self.controller.btn_r1.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            if self.controller.btn_l3.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
            if self.controller.btn_r3.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
            if self.controller.btn_create.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
            if self.controller.btn_options.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            if self.controller.btn_ps.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
            if self.controller.btn_up.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            if self.controller.btn_down.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            if self.controller.btn_left.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            if self.controller.btn_right.pressed:
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            else:
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

            self.gamepad.left_joystick(
                x_value=int(self.controller.left_stick_x.value * 32767),
                y_value=int(self.controller.left_stick_y.value * 32767)
            )

            self.gamepad.right_joystick(
                x_value=int(self.controller.right_stick_x.value * 32767),
                y_value=int(self.controller.right_stick_y.value * 32767)
            )

            self.gamepad.left_trigger(value=int(self.controller.left_trigger.value * 255))
            self.gamepad.right_trigger(value=int(self.controller.right_trigger.value * 255))

            self.gamepad.register_notification(callback_function=self.rumble_callback)
            self.gamepad.update()

        self.xbox_emulation_timer = QTimer(self)
        self.xbox_emulation_timer.timeout.connect(map_ds_to_xbox)
        self.xbox_emulation_timer.start(10)

    def stop_xbox_emulation(self):
        if hasattr(self, 'xbox_emulation_timer'):
            self.xbox_emulation_timer.stop()
            self.gamepad = None
            self.show_dualsense_controller()

    def check_for_controller(self):
        if self.controller is None:
            device_infos = DualSenseController.enumerate_devices()
            if len(device_infos) > 0:
                self.controller = DualSenseController()
                self.controller.activate()
                self.controller.microphone.set_unmuted()
                self.toggle_ui_elements(True)
            else:
                self.controller = None
                self.toggle_ui_elements(False)
        elif self.controller is not None:
            device_infos = DualSenseController.enumerate_devices()
            if len(device_infos) == 0:
                self.controller.deactivate()
                self.controller = None
                self.toggle_ui_elements(False)

    def on_touchpad_change(self, value):
        if self.controller and self.handle_touchpad_events:
            touch_position = QPointF(value.x, value.y)

            if self.last_touch_position is not None:
                delta = touch_position - self.last_touch_position
                max_move = 10
                delta.setX(max(-max_move, min(delta.x(), max_move)))
                delta.setY(max(-max_move, min(delta.y(), max_move)))
                current_cursor_pos = QCursor.pos()
                new_cursor_pos = current_cursor_pos + QPoint(int(delta.x()), int(delta.y()))
                QCursor.setPos(new_cursor_pos)

            self.last_touch_position = touch_position

    def send_mouse_left_click_pressed(self):
        if self.controller and self.handle_touchpad_events:
            pyautogui.leftClick()

    def set_lightbar_color(self):
        r = self.ui.r.value()
        g = self.ui.g.value()
        b = self.ui.b.value()

        if self.controller:
            self.controller.lightbar.set_color(r, g, b)
        
        self.save_settings()

    def update_battery_level(self):
        if self.controller:
            battery_level = round(self.controller.battery.value.level_percentage)
            self.ui.batteryBar.setValue(battery_level)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def load_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                settings = json.load(file)
                
            touchpad_checked = settings.get("touchpad_checked", False)
            self.ui.touchpadBox.setCheckState(Qt.CheckState.Checked if touchpad_checked else Qt.CheckState.Unchecked)
                
            color = settings.get("lightbar_color", {"r": 0, "g": 0, "b": 0})
            self.ui.r.setValue(color["r"])
            self.ui.g.setValue(color["g"])
            self.ui.b.setValue(color["b"])

            emulate_xbox_checked = settings.get("emulate_xbox_checked", False)
            self.ui.emulateXboxBox.setCheckState(Qt.CheckState.Checked if emulate_xbox_checked else Qt.CheckState.Unchecked)

    def save_settings(self):
        settings = {
            "touchpad_checked": self.ui.touchpadBox.isChecked(),
            "lightbar_color": {
                "r": self.ui.r.value(),
                "g": self.ui.g.value(),
                "b": self.ui.b.value()
            },
            "emulate_xbox_checked": self.ui.emulateXboxBox.isChecked()
        }
    
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)

    def create_startup_shortcut(self):
        target = sys.executable
        start_dir = os.path.dirname(os.path.realpath(__file__))
        shortcut_path = os.path.join(winshell.startup(), "MakeSense.lnk")

        winshell.CreateShortcut(
            Path=shortcut_path,
            Target=target,
            StartIn=start_dir,
            Icon=(target, 0),
            Description="MakeSense Application"
        )

    def delete_startup_shortcut(self):
        shortcut_path = os.path.join(winshell.startup(), "MakeSense.lnk")
        os.remove(shortcut_path)

    def check_startup_shortcut(self):
        shortcut_path = os.path.join(winshell.startup(), "MakeSense.lnk")
        if os.path.exists(shortcut_path):
            self.ui.startupBox.setChecked(True)
        else:
            self.ui.startupBox.setChecked(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    makesense = MakeSense()
    sys.exit(app.exec())

import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, QPointF, QPoint
from PyQt6.QtGui import QIcon, QAction, QCursor
import pyautogui
import winshell
import vgamepad as vg
from design import Ui_MainWindow
from dualsense_controller import DualSenseController

class ControllerChecker(QThread):
    controller_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = None
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            current_controller_present = self.controller is not None
            device_infos = DualSenseController.enumerate_devices()
            controller_present_now = len(device_infos) > 0

            if current_controller_present and not controller_present_now:
                self.controller.deactivate()
                self.controller = None
                self.controller_changed.emit(False)
            elif not current_controller_present and controller_present_now:
                self.controller = DualSenseController()
                self.controller.activate()
                self.controller.microphone.set_unmuted() # Disable mic led
                self.controller_changed.emit(True)

            self.msleep(1000)

    def stop(self):
        self.running = False

class MakeSense(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("MakeSense")
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setFixedSize(self.size())

        self.controller = None
        self.gamepad = None
        self.last_touch_position = None
        self.handle_touchpad_events = False
        self.device_instance_path = None
        self.touchpad_slots_created = False
        self.rumble_enabled = None
        self.hidhide_path = r"C:\Program Files\Nefarius Software Solutions\HidHide\x64\hidhidecli.exe"

        self.settings_file = os.path.join(os.getenv('APPDATA'), 'makesense', 'settings.json')
        self.load_settings()

        self.setup_ui_connections()
        self.setup_timers()
        self.create_system_tray_icon()
        self.controller_checker = ControllerChecker()
        self.controller_checker.controller_changed.connect(self.on_controller_changed)
        self.controller_checker.start()
        self.initialize_ui_state()


    def initialize_ui_state(self):
        device_infos = DualSenseController.enumerate_devices()
        controller_present_now = len(device_infos) > 0
        self.on_controller_changed(controller_present_now)

    def setup_ui_connections(self):
        # Lightbar color control connections
        self.ui.applyButton.clicked.connect(self.set_lightbar_color)

        # Two-way synchronization between sliders and spinboxes
        self.ui.r.valueChanged.connect(self.sync_r_slider_spinbox)
        self.ui.rSlider.valueChanged.connect(self.sync_r_spinbox_slider)
        self.ui.g.valueChanged.connect(self.sync_g_slider_spinbox)
        self.ui.gSlider.valueChanged.connect(self.sync_g_spinbox_slider)
        self.ui.b.valueChanged.connect(self.sync_b_slider_spinbox)
        self.ui.bSlider.valueChanged.connect(self.sync_b_spinbox_slider)

        # Other UI connections
        self.ui.touchpadBox.stateChanged.connect(self.handle_touchpad_state_change)
        self.ui.startupBox.stateChanged.connect(self.handle_startup_state_change)
        self.ui.emulateXboxBox.stateChanged.connect(self.handle_xbox_emulation_state_change)
        self.ui.rumbleBox.stateChanged.connect(self.handle_rumble_state_change)

    def sync_r_slider_spinbox(self, value):
        self.ui.rSlider.setValue(value)

    def sync_r_spinbox_slider(self, value):
        self.ui.r.setValue(value)

    def sync_g_slider_spinbox(self, value):
        self.ui.gSlider.setValue(value)

    def sync_g_spinbox_slider(self, value):
        self.ui.g.setValue(value)

    def sync_b_slider_spinbox(self, value):
        self.ui.bSlider.setValue(value)

    def sync_b_spinbox_slider(self, value):
        self.ui.b.setValue(value)

    def setup_timers(self):
        self.battery_timer = QTimer(self)
        self.battery_timer.timeout.connect(self.update_battery_level)
        self.battery_timer.start(10000)
        self.xbox_emulation_timer = QTimer(self)
        self.xbox_emulation_timer.timeout.connect(self.map_ds_to_xbox)

    def create_system_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icons/icon.png'))

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
        if self.controller:
            self.controller.deactivate()
        self.controller_checker.stop()
        QApplication.quit()

    def load_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                settings = json.load(file)

            self.ui.touchpadBox.setChecked(settings.get("touchpad_checked", False))
            r_value = settings.get("lightbar_color", {"r": 0, "g": 0, "b": 0}).get("r", 0)
            g_value = settings.get("lightbar_color", {"r": 0, "g": 0, "b": 0}).get("g", 0)
            b_value = settings.get("lightbar_color", {"r": 0, "g": 0, "b": 0}).get("b", 0)
            self.ui.r.setValue(r_value)
            self.ui.g.setValue(g_value)
            self.ui.b.setValue(b_value)
            self.ui.rSlider.setValue(r_value)
            self.ui.gSlider.setValue(g_value)
            self.ui.bSlider.setValue(b_value)

            self.ui.emulateXboxBox.setChecked(settings.get("emulate_xbox_checked", False))
            self.ui.rumbleBox.setEnabled(settings.get("emulate_xbox_checked", False))
            self.ui.rumbleLabel.setEnabled(settings.get("emulate_xbox_checked", False))
            self.ui.rumbleBox.setChecked(settings.get("rumble_checked", False))

    def save_settings(self):
        settings = {
            "touchpad_checked": self.ui.touchpadBox.isChecked(),
            "lightbar_color": {
                "r": self.ui.r.value(),
                "g": self.ui.g.value(),
                "b": self.ui.b.value()
            },
            "emulate_xbox_checked": self.ui.emulateXboxBox.isChecked(),
            "rumble_checked": self.ui.rumbleBox.isChecked()
        }

        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)

    def on_controller_changed(self, connected):
        if connected:
            self.controller = self.controller_checker.controller
            if self.controller:
                self.controller.microphone.set_unmuted()
                self.toggle_ui_elements(True)
                self.set_lightbar_color()
                if self.ui.emulateXboxBox.isChecked():
                    self.start_xbox_emulation()
        else:
            if self.controller:
                try:
                    self.controller.deactivate()
                except AssertionError as e:
                    print(f"Error deactivating controller: {e}")
                finally:
                    self.controller = None

            self.toggle_ui_elements(False)
            self.stop_xbox_emulation()

        self.device_instance_path = self.get_device_instance_path()
        self.handle_touchpad_state_change()
        self.update_battery_level()
        self.check_startup_shortcut()

    def toggle_ui_elements(self, show):
        self.ui.controllerFrame.setVisible(show)
        self.ui.notFoundLabel.setVisible(not show)

    def handle_touchpad_state_change(self):
        if self.controller:
            if not self.touchpad_slots_created:
                self.controller.touch_finger_1.on_change(self.on_touchpad_change)
                self.controller.btn_touchpad.on_down(self.send_mouse_left_click_pressed)
                self.touchpad_slots_created = True
        self.handle_touchpad_events = self.ui.touchpadBox.isChecked()
        self.save_settings()

    def handle_startup_state_change(self):
        if self.ui.startupBox.isChecked():
            self.create_startup_shortcut()
        else:
            self.delete_startup_shortcut()
        self.save_settings()

    def handle_rumble_state_change(self):
        if self.controller:
            if self.ui.rumbleBox.isChecked():
                self.rumble_enabled = True
            else:
                self.rumble_enabled = False
        self.save_settings()

    def handle_xbox_emulation_state_change(self):
        if self.ui.emulateXboxBox.isChecked():
            self.start_xbox_emulation()
            self.ui.rumbleBox.setEnabled(True)
            self.ui.rumbleLabel.setEnabled(True)
        else:
            self.stop_xbox_emulation()
            self.ui.rumbleBox.setEnabled(False)
            self.ui.rumbleLabel.setEnabled(False)
        self.save_settings()

    def start_xbox_emulation(self):
        if self.controller and self.gamepad is None:
            self.gamepad = vg.VX360Gamepad()
            self.hide_dualsense_controller()
            self.map_ds_to_xbox()
            self.xbox_emulation_timer.start(10)

    def stop_xbox_emulation(self):
        if self.gamepad:
            self.gamepad = None
            self.show_dualsense_controller()
            self.xbox_emulation_timer.stop()

    def hide_dualsense_controller(self):
        self.device_instance_path = self.get_device_instance_path()
        if self.device_instance_path:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            subprocess.run([self.hidhide_path, "--dev-hide", self.device_instance_path], startupinfo=startupinfo)
            subprocess.run([self.hidhide_path, "--app-reg", sys.executable], startupinfo=startupinfo)
            subprocess.run([self.hidhide_path, "--cloak-on"], startupinfo=startupinfo)

    def show_dualsense_controller(self):
        if self.device_instance_path:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            subprocess.run([self.hidhide_path, "--dev-unhide", self.device_instance_path], startupinfo=startupinfo)
            subprocess.run([self.hidhide_path, "--cloak-off"], startupinfo=startupinfo)

    def map_ds_to_xbox(self):
        if self.controller and self.gamepad:
            mappings = [
                (self.controller.btn_cross, vg.XUSB_BUTTON.XUSB_GAMEPAD_A),
                (self.controller.btn_circle, vg.XUSB_BUTTON.XUSB_GAMEPAD_B),
                (self.controller.btn_square, vg.XUSB_BUTTON.XUSB_GAMEPAD_X),
                (self.controller.btn_triangle, vg.XUSB_BUTTON.XUSB_GAMEPAD_Y),
                (self.controller.btn_l1, vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER),
                (self.controller.btn_r1, vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER),
                (self.controller.btn_l3, vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB),
                (self.controller.btn_r3, vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB),
                (self.controller.btn_create, vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK),
                (self.controller.btn_options, vg.XUSB_BUTTON.XUSB_GAMEPAD_START),
                (self.controller.btn_ps, vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE),
                (self.controller.btn_up, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP),
                (self.controller.btn_down, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN),
                (self.controller.btn_left, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT),
                (self.controller.btn_right, vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            ]

            for btn_ds, btn_xbox in mappings:
                if btn_ds.pressed:
                    self.gamepad.press_button(button=btn_xbox)
                else:
                    self.gamepad.release_button(button=btn_xbox)

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

            if self.rumble_enabled:
                self.gamepad.register_notification(callback_function=self.rumble_callback)
            self.gamepad.update()

    def rumble_callback(self, client, target, large_motor, small_motor, led_number, user_data):
        if self.controller:
            self.controller.left_rumble.set(large_motor)
            self.controller.right_rumble.set(small_motor)

    def update_battery_level(self):
        if self.controller:
            battery_level = round(self.controller.battery.value.level_percentage)
            self.ui.batteryBar.setValue(battery_level)

    def get_device_instance_path(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        result = subprocess.run([self.hidhide_path, '--dev-gaming'], capture_output=True, text=True, startupinfo=startupinfo)
        data = json.loads(result.stdout)
        for device in data:
            if device.get('friendlyName') == "Sony Interactive Entertainment DualSense Wireless Controller" or device.get('friendlyName') == "Sony Interactive Entertainment Wireless Controller":
                if device['devices'] and len(device['devices']) > 0:
                    return device['devices'][0].get('deviceInstancePath')

    def create_startup_shortcut(self):
        target = sys.executable
        start_dir = os.path.dirname(target)
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
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)

    def check_startup_shortcut(self):
        shortcut_path = os.path.join(winshell.startup(), "MakeSense.lnk")
        self.ui.startupBox.setChecked(os.path.exists(shortcut_path))

    def closeEvent(self, event):
        event.ignore()
        self.hide()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    makesense = MakeSense()
    sys.exit(app.exec())

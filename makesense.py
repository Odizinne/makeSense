import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon

hidhide_path = r"C:\Program Files\Nefarius Software Solutions\HidHide\x64\hidhidecli.exe"
vigembus_path = r"C:\Program Files\Nefarius Software Solutions\ViGEm Bus Driver\nefconw.exe"

def check_dependencies():
    missing_components = []

    if not os.path.exists(hidhide_path):
        missing_components.append("HidHide")
    if not os.path.exists(vigembus_path):
        missing_components.append("ViGEm Bus Driver")

    if missing_components:
        error_message = "The following components are missing:\n" + "\n".join(missing_components) + "\n\nPlease install the missing components."
        show_error_and_exit("Missing Dependencies", error_message)

def show_error_and_exit(title, message):
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icons/icon.png'))
    QMessageBox.critical(None, title, message)
    sys.exit(1)

check_dependencies()

import vgamepad as vg
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, QPointF, QPoint
from PyQt6.QtGui import QAction, QCursor
import json
import subprocess
import pyautogui
import winshell
from design import Ui_MainWindow
from dualsense_controller import DualSenseController
from controller_checker import ControllerChecker

class MakeSense(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("makeSense")
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setFixedSize(self.size())

        self.controller = None
        self.gamepad = None
        self.last_touch_position = None
        self.handle_touchpad_events = False
        self.device_instance_path = None
        self.touchpad_slots_created = False
        self.toggle_mic_slot_created = False
        self.toggle_touchpad_slot_created = False
        self.toggle_xbox_emulation_slot_created = False
        self.rumble_intensity = 50
        self.settings_file = os.path.join(os.getenv('APPDATA'), 'makesense', 'settings.json')
        self.setup_comboboxes()
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

    def setup_comboboxes(self):
        self.ui.shortcutComboBox.addItems(["Toggle mic state", "Toggle touchpad", "Toggle virtual XBOX"])
        self.ui.triggerComboBox.addItems(["Off", "Full press", "Soft press", "Medium press", "Hard press", "Pulse", "Choppy", "Soft rigidity", "Medium rigidity", "Hard rigidity", "Max rigidity", "Half press"])
    
    def setup_ui_connections(self):
        self.setup_slider_spinbox_sync(self.ui.rSlider, self.ui.r)
        self.setup_slider_spinbox_sync(self.ui.gSlider, self.ui.g)
        self.setup_slider_spinbox_sync(self.ui.bSlider, self.ui.b)

        self.ui.touchpadBox.stateChanged.connect(self.handle_touchpad_state_change)
        self.ui.startupBox.stateChanged.connect(self.handle_startup_state_change)
        self.ui.emulateXboxBox.stateChanged.connect(self.handle_xbox_emulation_state_change)
        self.ui.rumbleSlider.valueChanged.connect(self.handle_rumble_value_change)

        self.ui.triggerComboBox.currentIndexChanged.connect(self.handle_trigger_effect_change)
        self.ui.shortcutComboBox.currentIndexChanged.connect(self.handle_mic_shortcut_change)

    def setup_slider_spinbox_sync(self, slider, spinbox):
        slider.valueChanged.connect(lambda value: spinbox.setValue(value))
        spinbox.valueChanged.connect(lambda value: slider.setValue(value))
        spinbox.valueChanged.connect(self.set_lightbar_color)

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
        show_action.triggered.connect(self.toggle_window)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
                self.tray_icon.contextMenu().actions()[0].setText("Show")
            else:
                self.show()
                self.tray_icon.contextMenu().actions()[0].setText("Hide")

    def toggle_window(self):
        if self.isVisible():
            self.hide()
            self.tray_icon.contextMenu().actions()[0].setText("Show")
        else:
            self.show()
            self.tray_icon.contextMenu().actions()[0].setText("Hide")

    def quit(self):
        self.stop_xbox_emulation()
        if self.controller:
            self.controller.lightbar.set_color(0, 0, 255)
            self.controller.deactivate()
            self.controller = None
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
            shortcut_combo_index = settings.get("shortcut_combo_index", 0)
            trigger_combo_index = settings.get("trigger_combo_index", 0)
            self.ui.r.setValue(r_value)
            self.ui.g.setValue(g_value)
            self.ui.b.setValue(b_value)
            self.ui.rSlider.setValue(r_value)
            self.ui.gSlider.setValue(g_value)
            self.ui.bSlider.setValue(b_value)

            self.ui.emulateXboxBox.setChecked(settings.get("emulate_xbox_checked", False))
            self.ui.rumbleSlider.setEnabled(settings.get("emulate_xbox_checked", False))
            self.ui.rumbleLabel.setEnabled(settings.get("emulate_xbox_checked", False))
            self.ui.rumbleSlider.setValue(settings.get("rumble_intensity", 50))

            self.ui.shortcutComboBox.setCurrentIndex(shortcut_combo_index)
            self.ui.triggerComboBox.setCurrentIndex(trigger_combo_index)

    def save_settings(self):
        settings = {
            "touchpad_checked": self.ui.touchpadBox.isChecked(),
            "lightbar_color": {
                "r": self.ui.r.value(),
                "g": self.ui.g.value(),
                "b": self.ui.b.value()
            },
            "emulate_xbox_checked": self.ui.emulateXboxBox.isChecked(),
            "rumble_intensity": self.ui.rumbleSlider.value(),
            "shortcut_combo_index" : self.ui.shortcutComboBox.currentIndex(),
            "trigger_combo_index" : self.ui.triggerComboBox.currentIndex()
        }
        print(f"saved mic shortcut: {self.ui.shortcutComboBox.currentIndex()}")
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)

    def on_controller_changed(self, connected):
        if connected:
            self.controller = self.controller_checker.controller
            if self.controller:
                self.toggle_ui_elements(True)
                self.set_lightbar_color()
                if self.ui.emulateXboxBox.isChecked():
                    self.start_xbox_emulation()
        else:
            if self.controller:
                self.controller = None
                self.toggle_ui_elements(False)
            self.toggle_ui_elements(False)
            self.stop_xbox_emulation()

        self.device_instance_path = self.get_device_instance_path()
        self.handle_touchpad_state_change()
        self.update_battery_level()
        self.check_startup_shortcut()
        self.handle_xbox_emulation_state_change()
        self.handle_rumble_value_change()
        self.handle_mic_shortcut_change()
        self.handle_trigger_effect_change()

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

    def handle_rumble_value_change(self):
        if self.controller:
            self.rumble_intensity = self.ui.rumbleSlider.value()
        self.save_settings()

    def toggle_mic_led(self):
        if self.ui.shortcutComboBox.currentIndex() == 0:
            self.controller.microphone.toggle_muted()

    def toggle_touchpad(self):
        if self.ui.shortcutComboBox.currentIndex() == 1:
            self.ui.touchpadBox.setChecked(not self.ui.touchpadBox.isChecked())

    def toggle_xbox_emulation(self):
        if self.ui.shortcutComboBox.currentIndex() == 2:
            self.ui.emulateXboxBox.setChecked(not self.ui.emulateXboxBox.isChecked())

    def handle_trigger_effect_change(self):
        if self.controller:
            index = self.ui.triggerComboBox.currentIndex()
            effects = {
                0: lambda: (self.controller.left_trigger.effect.off(), self.controller.right_trigger.effect.off()),
                1: lambda: (self.controller.left_trigger.effect.full_press(), self.controller.right_trigger.effect.full_press()),
                2: lambda: (self.controller.left_trigger.effect.soft_press(), self.controller.right_trigger.effect.soft_press()),
                3: lambda: (self.controller.left_trigger.effect.medium_press(), self.controller.right_trigger.effect.medium_press()),
                4: lambda: (self.controller.left_trigger.effect.hard_press(), self.controller.right_trigger.effect.hard_press()),
                5: lambda: (self.controller.left_trigger.effect.pulse(), self.controller.right_trigger.effect.pulse()),
                6: lambda: (self.controller.left_trigger.effect.choppy(), self.controller.right_trigger.effect.choppy()),
                7: lambda: (self.controller.left_trigger.effect.soft_rigidity(), self.controller.right_trigger.effect.soft_rigidity()),
                8: lambda: (self.controller.left_trigger.effect.medium_rigidity(), self.controller.right_trigger.effect.medium_rigidity()),
                9: lambda: (self.controller.left_trigger.effect.max_rigidity(), self.controller.right_trigger.effect.max_rigidity()),
                10: lambda: (self.controller.left_trigger.effect.half_press(), self.controller.right_trigger.effect.half_press()),
            }
            if index in effects:
                effects[index]()
            self.save_settings()
            
    def handle_mic_shortcut_change(self):
        if self.controller:
            index = self.ui.shortcutComboBox.currentIndex()
            if index == 0:
                if not self.toggle_mic_slot_created:
                    self.controller.btn_mute.on_down(self.toggle_mic_led)
                    self.toggle_mic_slot_created = True
            elif index == 1:
                if not self.toggle_touchpad_slot_created:
                    self.controller.btn_mute.on_down(self.toggle_touchpad)
                    self.toggle_touchpad_slot_created = True
            elif index == 2:
                if not self.toggle_xbox_emulation_slot_created:
                    self.controller.btn_mute.on_down(self.toggle_xbox_emulation)
                    self.toggle_xbox_emulation_slot_created = True
            self.save_settings()

    def handle_xbox_emulation_state_change(self):
        if self.ui.emulateXboxBox.isChecked():
            self.start_xbox_emulation()
            self.ui.rumbleSlider.setEnabled(True)
            self.ui.rumbleLabel.setEnabled(True)
        else:
            self.stop_xbox_emulation()
            self.ui.rumbleSlider.setEnabled(False)
            self.ui.rumbleLabel.setEnabled(False)
        self.save_settings()

    def start_xbox_emulation(self):
        if self.controller and self.gamepad is None:
            self.device_instance_path = self.get_device_instance_path()
            self.gamepad = vg.VX360Gamepad()
            self.gamepad.register_notification(callback_function=self.rumble_callback)
            self.toggle_dualsense_controller_visibility(True)
            self.map_ds_to_xbox()
            self.xbox_emulation_timer.start(4)

    def stop_xbox_emulation(self):
        if self.gamepad:
            self.gamepad.unregister_notification()
            self.gamepad = None
            self.toggle_dualsense_controller_visibility(False)
            self.xbox_emulation_timer.stop()

    def toggle_dualsense_controller_visibility(self, hide):
        if self.device_instance_path:
            action = "--dev-hide" if hide else "--dev-unhide"
            cloak_action = "--cloak-on" if hide else "--cloak-off"

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.run([hidhide_path, "--app-reg", sys.executable], startupinfo=startupinfo)
            subprocess.run([hidhide_path, action, self.device_instance_path], startupinfo=startupinfo)
            subprocess.run([hidhide_path, cloak_action], startupinfo=startupinfo)

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

            
            
            self.gamepad.update()

    def rumble_callback(self, client, target, large_motor, small_motor, led_number, user_data):
        if self.controller:
            converted_large_motor = (large_motor / 255.0) * (self.rumble_intensity / 100)
            converted_small_motor = (small_motor / 255.0) * (self.rumble_intensity / 100)
            self.controller.left_rumble.set(converted_large_motor)
            self.controller.right_rumble.set(converted_small_motor)

    def update_battery_level(self):
        if self.controller:
            battery_level = round(self.controller.battery.value.level_percentage)
            battery_status = self.controller.battery.value.charging
            if battery_status:
                battery_status = "Charging"
            else:
                battery_status = "Discharging"
            self.ui.batteryBar.setValue(battery_level)
            self.ui.batteryLabel.setText(f"{battery_level}%")
            self.ui.batteryStatusLabel.setText(battery_status)

    def get_device_instance_path(self):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        result = subprocess.run([hidhide_path, '--dev-gaming'], capture_output=True, text=True, startupinfo=startupinfo)
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
        self.toggle_window()

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
        print("Setting lightbar color")
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

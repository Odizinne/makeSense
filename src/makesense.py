import sys
import os
import winreg
import json
import subprocess
import pyautogui
import winshell
import darkdetect
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, QPointF, QPoint, QSharedMemory
from PyQt6.QtGui import QAction, QCursor
from design import Ui_MainWindow
from dualsense_controller import DualSenseController
from controller_checker import ControllerChecker
from virtual_xbox_gamepad import VirtualXBOXGamepad

hidhide_path = r"C:\Program Files\Nefarius Software Solutions\HidHide\x64\hidhidecli.exe"
vigembus_path = r"C:\Program Files\Nefarius Software Solutions\ViGEm Bus Driver\nefconw.exe"


def check_dependencies():
    missing_components = []

    if not os.path.exists(hidhide_path):
        missing_components.append("HidHide")
    if not os.path.exists(vigembus_path):
        missing_components.append("ViGEm Bus Driver")

    if missing_components:
        error_message = (
            "The following components are missing:\n"
            + "\n".join(missing_components)
            + "\n\nPlease install the missing components."
        )
        show_error_and_exit("Missing Dependencies", error_message)


def show_error_and_exit(title, message):
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/icon.png"))
    QMessageBox.critical(None, title, message)
    sys.exit(1)


def single_instance_check():
    shared_memory = QSharedMemory("makeSense")

    if shared_memory.attach() or not shared_memory.create(1):
        sys.exit(1)

    return shared_memory


check_dependencies()


class MakeSense(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("makeSense")
        self.setWindowIcon(QIcon(self.detect_system_theme()))
        self.default_size = self.size()
        self.controller = None
        self.virtual_xbox_gamepad = None
        self.last_touch_position = None
        self.device_instance_path = None
        self.notification_sent = None
        self.hide_dualsense = None
        self.shared_memory = shared_memory
        self.rumble_intensity = 50
        self.settings_file = os.path.join(os.getenv("APPDATA"), "makesense", "settings.json")
        self.setup_comboboxes()
        self.load_settings()
        self.setup_ui_connections()
        self.setup_timers()
        self.create_system_tray_icon()
        self.controller_checker = ControllerChecker()
        self.controller_checker.controller_changed.connect(self.on_controller_changed)
        self.controller_checker.start()
        self.initialize_ui_state()

    def detect_system_theme(self):
        if darkdetect.isDark():
            return "icons/icon.png"
        else:
            return "icons/icon_light.png"

    def initialize_ui_state(self):
        device_infos = DualSenseController.enumerate_devices()
        controller_present_now = len(device_infos) > 0
        self.on_controller_changed(controller_present_now)

    def setup_comboboxes(self):
        self.ui.shortcutComboBox.addItems(
            ["Toggle mic state", "Toggle touchpad", "Toggle virtual XBOX", "Start or focus Steam"]
        )
        self.ui.triggerComboBox.addItems(
            [
                "Off",
                "Full press",
                "Soft press",
                "Medium press",
                "Hard press",
                "Pulse",
                "Choppy",
                "Soft rigidity",
                "Medium rigidity",
                "Hard rigidity",
                "Max rigidity",
                "Half press",
            ]
        )

    def setup_ui_connections(self):
        self.setup_slider_spinbox_sync(self.ui.rSlider, self.ui.r)
        self.setup_slider_spinbox_sync(self.ui.gSlider, self.ui.g)
        self.setup_slider_spinbox_sync(self.ui.bSlider, self.ui.b)

        self.ui.touchpadBox.stateChanged.connect(self.on_touchpadBox_state_changed)
        self.ui.startupBox.stateChanged.connect(self.on_startupBox_state_changed)
        self.ui.emulateXboxBox.stateChanged.connect(self.on_emulateXboxBox_state_changed)
        self.ui.rumbleSlider.valueChanged.connect(self.on_rumbleSlider_value_changed)
        self.ui.triggerComboBox.currentIndexChanged.connect(self.on_triggerComboBox_index_changed)
        self.ui.shortcutComboBox.currentIndexChanged.connect(self.on_shortcutComboBox_index_changed)
        self.ui.batteryNotificationBox.stateChanged.connect(self.save_settings)
        self.ui.hideDualsenseBox.stateChanged.connect(self.on_hideDualsenseBox_state_changed)

    def setup_slider_spinbox_sync(self, slider, spinbox):
        slider.valueChanged.connect(lambda value: spinbox.setValue(value))
        spinbox.valueChanged.connect(lambda value: slider.setValue(value))
        spinbox.valueChanged.connect(self.set_lightbar_color)

    def setup_timers(self):
        self.battery_timer = QTimer(self)
        self.battery_timer.timeout.connect(self.update_battery_level)
        self.battery_timer.start(10000)

    def create_system_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.detect_system_theme()))
        self.tray_icon.setToolTip("makeSense")

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
        if self.controller:
            self.stop_xbox_emulation()
            self.controller.lightbar.set_color(0, 0, 255)
            self.controller.deactivate()
            self.controller = None
        self.controller_checker.stop()
        QApplication.quit()

    def load_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as file:
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
                self.ui.hideDualsenseBox.setEnabled(settings.get("emulate_xbox_checked", False))
                self.ui.hideDualsenseLabel.setEnabled(settings.get("emulate_xbox_checked", False))
                self.ui.batteryNotificationBox.setChecked(settings.get("battery_notification_checked", False))
                self.ui.hideDualsenseBox.setChecked(settings.get("hide_dualsense_checked", False))
                self.ui.rumbleSlider.setValue(settings.get("rumble_intensity", 50))
                self.ui.shortcutComboBox.setCurrentIndex(shortcut_combo_index)
                self.ui.triggerComboBox.setCurrentIndex(trigger_combo_index)

            else:
                self.ui.rumbleLabel.setEnabled(False)
                self.ui.rumbleSlider.setEnabled(False)
                self.ui.hideDualsenseLabel.setEnabled(False)
                self.ui.hideDualsenseBox.setEnabled(False)
        except Exception as e:
            print(f"Unexpected error: {e}")
        self.save_settings()

    def save_settings(self):
        settings = {
            "touchpad_checked": self.ui.touchpadBox.isChecked(),
            "lightbar_color": {"r": self.ui.r.value(), "g": self.ui.g.value(), "b": self.ui.b.value()},
            "emulate_xbox_checked": self.ui.emulateXboxBox.isChecked(),
            "battery_notification_checked": self.ui.batteryNotificationBox.isChecked(),
            "hide_dualsense_checked": self.ui.hideDualsenseBox.isChecked(),
            "rumble_intensity": self.ui.rumbleSlider.value(),
            "shortcut_combo_index": self.ui.shortcutComboBox.currentIndex(),
            "trigger_combo_index": self.ui.triggerComboBox.currentIndex(),
        }
        with open(self.settings_file, "w") as file:
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

        self.on_touchpadBox_state_changed()
        self.update_battery_level()
        self.check_startup_shortcut()
        self.on_rumbleSlider_value_changed()
        self.on_shortcutComboBox_index_changed()
        self.on_triggerComboBox_index_changed()
        self.on_hideDualsenseBox_state_changed()

    def toggle_ui_elements(self, show):
        self.ui.controllerFrame.setVisible(show)
        self.ui.notFoundLabel.setVisible(not show)
        if show:
            self.setFixedSize(self.default_size)
        else:
            self.setFixedSize(300, 200)

    def on_touchpadBox_state_changed(self):
        if self.controller:
            self.controller.touch_finger_1._state.remove_all_change_listeners()
            self.controller.btn_touchpad._state.remove_all_change_listeners()
            if self.ui.touchpadBox.isChecked():
                self.controller.touch_finger_1.on_change(self.map_touchpad_to_pointer)
                self.controller.btn_touchpad.on_down(self.send_mouse_left_click_pressed)
        self.save_settings()

    def on_startupBox_state_changed(self):
        if self.ui.startupBox.isChecked():
            self.create_startup_shortcut()
        else:
            self.delete_startup_shortcut()
        self.save_settings()

    def on_rumbleSlider_value_changed(self):
        if self.controller and self.virtual_xbox_gamepad:
            self.rumble_intensity = self.ui.rumbleSlider.value()
            self.virtual_xbox_gamepad.set_rumble_intensity(self.rumble_intensity)
        self.save_settings()

    def on_triggerComboBox_index_changed(self):
        if self.controller:
            index = self.ui.triggerComboBox.currentIndex()
            effects = {
                0: lambda: (self.controller.left_trigger.effect.off(), self.controller.right_trigger.effect.off()),
                1: lambda: (
                    self.controller.left_trigger.effect.full_press(),
                    self.controller.right_trigger.effect.full_press(),
                ),
                2: lambda: (
                    self.controller.left_trigger.effect.soft_press(),
                    self.controller.right_trigger.effect.soft_press(),
                ),
                3: lambda: (
                    self.controller.left_trigger.effect.medium_press(),
                    self.controller.right_trigger.effect.medium_press(),
                ),
                4: lambda: (
                    self.controller.left_trigger.effect.hard_press(),
                    self.controller.right_trigger.effect.hard_press(),
                ),
                5: lambda: (self.controller.left_trigger.effect.pulse(), self.controller.right_trigger.effect.pulse()),
                6: lambda: (
                    self.controller.left_trigger.effect.choppy(),
                    self.controller.right_trigger.effect.choppy(),
                ),
                7: lambda: (
                    self.controller.left_trigger.effect.soft_rigidity(),
                    self.controller.right_trigger.effect.soft_rigidity(),
                ),
                8: lambda: (
                    self.controller.left_trigger.effect.medium_rigidity(),
                    self.controller.right_trigger.effect.medium_rigidity(),
                ),
                9: lambda: (
                    self.controller.left_trigger.effect.max_rigidity(),
                    self.controller.right_trigger.effect.max_rigidity(),
                ),
                10: lambda: (
                    self.controller.left_trigger.effect.half_press(),
                    self.controller.right_trigger.effect.half_press(),
                ),
            }
            if index in effects:
                effects[index]()
            self.save_settings()

    def on_shortcutComboBox_index_changed(self):
        if self.controller:
            index = self.ui.shortcutComboBox.currentIndex()
            self.controller.btn_mute._state.remove_all_change_listeners()
            if index == 0:
                self.controller.btn_mute.on_down(self.toggle_mic_led)
            elif index == 1:
                self.controller.btn_mute.on_down(self.toggle_touchpad)
            elif index == 2:
                self.controller.btn_mute.on_down(self.toggle_xbox_emulation)
            elif index == 3:
                self.controller.btn_mute.on_down(self.start_steam)

            self.save_settings()

    def on_emulateXboxBox_state_changed(self):
        if self.ui.emulateXboxBox.isChecked():
            self.start_xbox_emulation()
            self.hide_dualsense = self.ui.hideDualsenseBox.isChecked()
            self.virtual_xbox_gamepad.hide_dualsense = self.hide_dualsense
            self.ui.rumbleSlider.setEnabled(True)
            self.ui.rumbleLabel.setEnabled(True)
            self.ui.hideDualsenseBox.setEnabled(True)
            self.ui.hideDualsenseLabel.setEnabled(True)
        else:
            self.stop_xbox_emulation()
            self.ui.rumbleSlider.setEnabled(False)
            self.ui.rumbleLabel.setEnabled(False)
            self.ui.hideDualsenseBox.setEnabled(False)
            self.ui.hideDualsenseLabel.setEnabled(False)
        self.save_settings()

    def on_hideDualsenseBox_state_changed(self):
        if self.virtual_xbox_gamepad:
            self.hide_dualsense = self.ui.hideDualsenseBox.isChecked()
            self.virtual_xbox_gamepad.hide_dualsense = self.hide_dualsense
            print("Hiding dualsense controller")
            self.virtual_xbox_gamepad.toggle_dualsense_controller_visibility(self.hide_dualsense)
        self.save_settings()

    def toggle_mic_led(self):
        self.controller.microphone.toggle_muted()

    def toggle_touchpad(self):
        self.ui.touchpadBox.setChecked(not self.ui.touchpadBox.isChecked())

    def toggle_xbox_emulation(self):
        self.ui.emulateXboxBox.setChecked(not self.ui.emulateXboxBox.isChecked())
        xbox_status = "enabled" if self.ui.emulateXboxBox.isChecked() else "disabled"
        dualsense_status = "hidden" if self.ui.emulateXboxBox.isChecked() else "visible"
        icon = QIcon("icons/xb_logo.png") if self.ui.emulateXboxBox.isChecked() else QIcon("icons/ps_logo.png")
        self.tray_icon.showMessage(
            f"XBOX controller emulation {xbox_status}.", f"Dualsense controller is now {dualsense_status}.", icon, 3000
        )

    def start_steam(self):
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
            install_path, _ = winreg.QueryValueEx(reg_key, "InstallPath")
            winreg.CloseKey(reg_key)
            if not install_path:
                return
            steam_exe_path = os.path.join(install_path, "steam.exe")
            if not os.path.exists(steam_exe_path):
                return
            subprocess.Popen([steam_exe_path])
        except FileNotFoundError:
            return

    def start_xbox_emulation(self):
        self.virtual_xbox_gamepad = VirtualXBOXGamepad(self.controller)
        self.hide_dualsense = self.ui.hideDualsenseBox.isChecked()
        self.virtual_xbox_gamepad.hide_dualsense = self.hide_dualsense
        self.virtual_xbox_gamepad.start_emulation()

    def stop_xbox_emulation(self):
        if self.virtual_xbox_gamepad:
            self.virtual_xbox_gamepad.stop_emulation()
            self.virtual_xbox_gamepad = None

    def update_battery_level(self):
        if self.controller:
            controller_battery_level = round(self.controller.battery.value.level_percentage)
            controller_battery_status = self.controller.battery.value.charging
            controller_connection_type = self.controller.connection_type.name
            if controller_battery_status:
                battery_status = "Charging"
            else:
                battery_status = "Discharging"

            if controller_connection_type == "USB_01":
                connexion_type = "Wired"
            else:
                connexion_type = "Bluetooth"
            self.ui.batteryBar.setValue(controller_battery_level)
            self.ui.batteryLabel.setText(f"{controller_battery_level}%")
            self.ui.batteryStatusLabel.setText(battery_status)
            self.ui.connectionTypeLabel.setText(connexion_type)
            if (
                self.ui.batteryNotificationBox.isChecked()
                and controller_battery_level < 20
                and not controller_battery_status
            ):
                if not self.notification_sent:
                    self.tray_icon.showMessage(
                        "Low battery", "Dualsense controller battery is low.", QIcon("icons/icon.png"), 3000
                    )
                    self.notification_sent = True
            if self.notification_sent and controller_battery_level > 25:
                self.notification_sent = False

    def create_startup_shortcut(self):
        target = sys.executable
        start_dir = os.path.dirname(target)
        shortcut_path = os.path.join(winshell.startup(), "MakeSense.lnk")

        winshell.CreateShortcut(
            Path=shortcut_path, Target=target, StartIn=start_dir, Icon=(target, 0), Description="MakeSense Application"
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

    def map_touchpad_to_pointer(self, value):
        if self.controller:
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
        if self.controller:
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
    shared_memory = single_instance_check()
    makesense = MakeSense()
    sys.exit(app.exec())

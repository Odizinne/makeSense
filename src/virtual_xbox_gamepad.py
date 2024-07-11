import vgamepad as vg
import subprocess
import json
import sys
from PyQt6.QtCore import QTimer

hidhide_path = r"C:\Program Files\Nefarius Software Solutions\HidHide\x64\hidhidecli.exe"

class VirtualXBOXGamepad:
    def __init__(self, controller):
        self.controller = controller
        self.gamepad = None
        self.device_instance_path = self.get_device_instance_path()
        self.rumble_intensity = 50

    def start_emulation(self):
        if self.controller and self.gamepad is None:
            self.device_instance_path = self.get_device_instance_path()
            self.gamepad = vg.VX360Gamepad()
            self.gamepad.register_notification(callback_function=self.rumble_callback)
            self.toggle_dualsense_controller_visibility(True)
            self.map_ds_to_xbox()
            self.xbox_emulation_timer = QTimer()
            self.xbox_emulation_timer.timeout.connect(self.map_ds_to_xbox)
            self.xbox_emulation_timer.start(4)

    def stop_emulation(self):
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

    def set_rumble_intensity(self, intensity):
        self.rumble_intensity = intensity

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

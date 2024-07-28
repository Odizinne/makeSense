from PyQt6.QtCore import QThread, pyqtSignal
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
                # Unmute microphone by default, disable LED
                self.controller = DualSenseController(microphone_initially_muted=False)
                self.controller.activate()
                self.controller_changed.emit(True)

            self.msleep(1000)

    def stop(self):
        self.running = False

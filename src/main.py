import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTranslator, QLocale, QSharedMemory
from utils import is_windows_10
from makesense import MakeSense


def single_instance_check():
    shared_memory = QSharedMemory("makeSense")

    if shared_memory.attach() or not shared_memory.create(1):
        sys.exit(1)

    return shared_memory


if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    locale_name = QLocale.system().name()
    locale = locale_name[:2]
    if locale:
        file_name = f"makesense_{locale}.qm"
    else:
        file_name = None

    if file_name and translator.load(file_name):
        app.installTranslator(translator)
    if is_windows_10():
        app.setStyle("Fusion")
    shared_memory = single_instance_check()
    makesense = MakeSense()
    sys.exit(app.exec())

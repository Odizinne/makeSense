import os
from cx_Freeze import setup, Executable
from setuptools.command.install import install as _install

src_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = "build/makeSense"
install_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'programs', 'makeSense')

zip_include_packages = ['PyQt6', 'winshell', 'dualsense-controller', 'pyautogui']

include_files = [
    os.path.join(src_dir, 'icons/'), 
    os.path.join(src_dir, 'dependencies/hidapi/hidapi.dll'), 
    os.path.join(src_dir, 'dependencies/hidapi/hidapi.lib')
]

build_exe_options = {
    "include_files": include_files,
    "build_exe": build_dir,
    "zip_include_packages": zip_include_packages,
    "excludes": ["tkinter", "PyQt5", "PySide6", "pygetwindow", "PyQt6-WebEngine", "numpy"],
}

executables = [
    Executable(os.path.join(src_dir, 'makesense.py'), base="Win32GUI", icon=os.path.join(src_dir, "icons/icon.ico"), target_name="makeSense.exe")
]

class InstallCommand(_install):
    def run(self):
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        if not os.path.exists(build_dir):
            print("##################################################")
            print("# Nothing to install.                            #")
            print("# Please build the project first.                #")
            print("##################################################")
            return
        self.copy_tree(build_dir, install_dir)
        print(f"Executable installed to {install_dir}")

setup(
    name='makeSense',
    version='1.0',
    options={"build_exe": build_exe_options},
    executables=executables,
    cmdclass={'install': InstallCommand}
)

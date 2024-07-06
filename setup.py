from cx_Freeze import setup, Executable
import sys

build_dir = "build/makeSense"
base = None
zip_include_packages = ['PyQt6', 'dualsense-controller']
include_files = ['icon.png']

if sys.platform == "win32":
    base = "Win32GUI"
    zip_include_packages = ['PyQt6', 'winshell', 'dualsense-controller', 'pyautogui']
    include_files = ['icon.png', 'dependencies/hidapi/hidapi.dll', 'dependencies/hidapi/hidapi.lib']

build_exe_options = {
    "include_files": include_files,
    "build_exe": build_dir,
    "zip_include_packages": zip_include_packages,
    "excludes": ["tkinter", "PyQt5", "PySide6", "pygetwindow", "PyQt6-WebEngine", "numpy"],
}

executables = [
    Executable('makesense.py', base=base)
]

setup(
    name='makeSense',
    version='1.0',
    options={"build_exe": build_exe_options},
    executables=executables
)
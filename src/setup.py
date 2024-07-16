import os
from cx_Freeze import setup, Executable

src_dir = os.path.dirname(os.path.abspath(__file__))

build_dir = "build/makeSense"

base = "Win32GUI"

icon = os.path.join(src_dir, "icons/icon.ico")

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
    Executable(os.path.join(src_dir, 'makesense.py'), base=base, icon=icon, target_name="makeSense.exe")
]

setup(
    name='makeSense',
    version='1.0',
    options={"build_exe": build_exe_options},
    executables=executables
)

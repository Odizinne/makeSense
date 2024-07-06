from cx_Freeze import setup, Executable

build_dir = "build/makeSense"
base = "Win32GUI"
#system_icon = "icons/steamos-logo.ico"

zip_include_packages = ['PyQt6', 'winshell', 'dualsense-controller', 'pyautogui']

build_exe_options = {
    "include_files": ['icon.png'],
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
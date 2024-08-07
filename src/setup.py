import os
from cx_Freeze import setup, Executable

src_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = "build/makeSense"
install_dir = os.path.join(os.getenv("LOCALAPPDATA"), "programs", "makeSense")

zip_include_packages = ["PyQt6", "winshell", "dualsense-controller", "pyautogui"]

include_files = [
    os.path.join(src_dir, "icons/"),
    os.path.join(src_dir, "dependencies/hidapi/hidapi.dll"),
    os.path.join(src_dir, "dependencies/hidapi/hidapi.lib"),
]

build_exe_options = {
    "include_files": include_files,
    "build_exe": build_dir,
    "zip_include_packages": zip_include_packages,
    "excludes": ["tkinter"],
}

executables = [
    Executable(
        os.path.join(src_dir, "makesense.py"),
        base="Win32GUI",
        icon=os.path.join(src_dir, "icons/icon.ico"),
        target_name="makeSense.exe",
    )
]


setup(
    name="makeSense",
    version="1.0",
    options={"build_exe": build_exe_options},
    executables=executables,
)

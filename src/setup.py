import os
from cx_Freeze import setup, Executable
from setuptools.command.install import install as _install
import winshell

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
        print("")
        print(f"Executable installed to {install_dir}")

        shortcut_path = os.path.join(winshell.programs(), "makeSense.lnk")
        target = os.path.join(install_dir, "makeSense.exe")
        icon = os.path.join(src_dir, "icons/icon.ico")

        winshell.CreateShortcut(
            Path=shortcut_path, Target=target, Icon=(icon, 0), Description="makeSense", StartIn=install_dir
        )

        print("Created shortcut in start menu")


setup(
    name="makeSense",
    version="1.0",
    options={"build_exe": build_exe_options},
    executables=executables,
    cmdclass={"install": InstallCommand},
)

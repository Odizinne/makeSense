# makeSense

Python Dualsense driver using dualsense-controller.

**If you appreciate my work and would like to support me:**<br/>
<a href="https://ko-fi.com/odizinne">
  <img src="assets/kofi_button_red.png" alt="Ko-fi" width="200" height="auto">
</a>

## Features

![image](assets/makeSense.png)

What's working:
- LED
- Touchpad
- Virtual XBOX controller
- Trigger effects

What's partially working:
- Battery percentage (Can return wrong value)

What's not implemented:
- Multiple controller support

Every change will be saved and restored on restart.

## Download

You need Nefarius [HidHide](https://github.com/nefarius/HidHide/releases/download/v1.5.230.0/HidHide_1.5.230_x64.exe) and [ViGEmBus Driver](https://github.com/nefarius/ViGEmBus/releases/download/v1.22.0/ViGEmBus_1.22.0_x64_x86_arm64.exe) installed in default location.

Restart your computer after installation.

Download [latest build](https://github.com/Odizinne/makeSense/releases/download/v7/makeSense.zip) and extract it.

Run `makeSense.exe`.

## Build

To build an executable by yourself, you'll need the following dependencies:

- Python
- cx_freeze
- vgamepad
- dualsense-controller
- PyQt6
- winshell
- PyAutoGUI

`pip install cx_freeze PyQt6 winshell PyAutoGUI dualsense-controller vgamepad`

If you do not have ViGEmBus driver installer, vgamepad will prompt you to install it.  
You must install HidHide.

- Clone this repository:  
`git clone https://github.com/Odizinne/makeSense.git`

- Place yourself inside the cloned folder:  
`cd .\makeSense`

- Build with cx_freeze:  
`python .\setup.py build`

## To-do
- Big code cleanup
- New icon

## Credits

- [Nefarius](https://github.com/nefarius) (Hidhide, ViGemBus Driver)
- [Yesbotics](https://github.com/yesbotics) (dualsense-controller-python)

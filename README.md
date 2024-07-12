# makeSense

Python Dualsense driver using [dualsense-controller](https://github.com/yesbotics/dualsense-controller-python).

⚠️ makeSense is in continuous development. ⚠️  
While i do my best to ensure everything is working when i release a new build, things may break from time to time. 

**If you appreciate my work and would like to support me:**<br/>
<a href="https://ko-fi.com/odizinne">
  <img src="assets/kofi_button_red.png" alt="Ko-fi" width="200" height="auto">
</a>

## Features

![image](assets/makeSense_screenshot.png)

- Multiple controller support is not implemented. I will probably do it one day.  
- Wireless dongle is not implemented. I will do it if someone request it.

Every setting you change in makeSense will be saved and restored on application restart.

## Download

You need Nefarius [HidHide](https://github.com/nefarius/HidHide/releases/download/v1.5.230.0/HidHide_1.5.230_x64.exe) and [ViGEmBus Driver](https://github.com/nefarius/ViGEmBus/releases/download/v1.22.0/ViGEmBus_1.22.0_x64_x86_arm64.exe) installed in default location.

Restart your computer after installation.

Download [latest build](https://github.com/Odizinne/makeSense/releases/) and extract it.

Run `makeSense.exe`.

## Build

To build an executable by yourself, you'll need Python and install the following dependencies:

`pip install cx_freeze PyQt6 winshell winreg PyAutoGUI dualsense-controller vgamepad darkdetect`

If you do not have ViGEmBus driver installer, vgamepad will prompt you to install it.  
You must install HidHide to run makeSense.

- Clone this repository:  
`git clone https://github.com/Odizinne/makeSense.git`

- Place yourself inside the cloned folder:  
`cd .\makeSense`

- Build with cx_freeze:  
`python .\src\setup.py build`

## To-do
- Big code cleanup
- New icon

## Credits

- [Nefarius](https://github.com/nefarius) (Hidhide, ViGemBus Driver)
- [Yesbotics](https://github.com/yesbotics) (dualsense-controller-python)
- Edited PS logo from [wikimedia](https://commons.wikimedia.org/wiki/File:PlayStation_logo.svg)
- Edited XBOX logo from [wikimedia](https://commons.wikimedia.org/wiki/File:Xbox_Logo.svg)
- Edited dualsense square icon from [Ignire](https://next.nexusmods.com/profile/Ignire/about-me?gameId=1392)

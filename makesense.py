from pydualsense import pydualsense
import vgamepad as vg
import time
import pyautogui

ds = pydualsense()
ds.init()
#pyautogui.FAILSAFE = False
gamepad = vg.VX360Gamepad()

def map_inputs():
    if ds.state.cross:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    
    if ds.state.square:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

    if ds.state.triangle:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

    if ds.state.circle:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

    if ds.state.L1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

    if ds.state.R1:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    
    if ds.state.L3:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
    
    if ds.state.R3:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)

    if ds.state.options:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)

    if ds.state.share:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

    if ds.state.ps:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
    
    if ds.state.DpadUp:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)

    if ds.state.DpadDown:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

    if ds.state.DpadLeft:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)

    if ds.state.DpadRight:
        gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    else:
        gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

    scaling_factor_x = -32768 / -128
    scaling_factor_y = 32767 / 128
    gamepad.left_joystick(
        x_value=int(ds.state.LX * scaling_factor_x),
        y_value=int(-ds.state.LY * scaling_factor_y)
    )
    
    gamepad.right_joystick(
        x_value=int(ds.state.RX * scaling_factor_x),
        y_value=int(-ds.state.RY * scaling_factor_y)
    )
    
    gamepad.left_trigger(value=int(ds.state.L2 / 255 * 255))
    gamepad.right_trigger(value=int(ds.state.R2 / 255 * 255))

try:
    while True:
        map_inputs()
        gamepad.update()
        time.sleep(0.01)
finally:
    ds.close()

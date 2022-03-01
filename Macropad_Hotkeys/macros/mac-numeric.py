# MACROPAD Hotkeys example: Safari web browser for Mac

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                # REQUIRED dict, must be named 'app'
    'name' : 'Numeric', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, '7', [Keycode.COMMAND, '7']),
        (0x004000, '8', [Keycode.COMMAND, '8']),
        (0x400000, '9', [Keycode.COMMAND, '9']),
        # 2nd row ----------
        (0x202000, '4', [Keycode.COMMAND, '4']),
        (0x202000, '5', [Keycode.COMMAND, '5']),
        (0x400000, '6', [Keycode.COMMAND, '6']),
        # 3rd row ----------
        (0x000040, '1', [Keycode.COMMAND, '1']),
        (0x000040, '2', [Keycode.COMMAND, '2']),
        (0x000040, '3', [Keycode.COMMAND, '3']),
        # 4th row ----------
        (0x000000, '0', [Keycode.COMMAND, '0']),
        (0x800000, '.', [Keycode.COMMAND, '.']),
        (0x101010, 'enter', [Keycode.CONTROL, Keycode.ENTER]), # Hack-a-Day in new win
        # Encoder button ---
        (0x000000, '', [Keycode.COMMAND, 'w']) # Close window/tab
    ]
}

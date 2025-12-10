import board
import busio
from storage import getmount

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers
from kmk.extensions.rgb import RGB
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

keyboard = KMKKeyboard()
keyboard.debug_enabled = False

# https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/split_keyboards.md#split_side
side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

keyboard.col_pins = (board.GP1, board.GP2, board.GP3, board.GP4, board.GP5)
keyboard.row_pins = (board.GP6, board.GP7, board.GP8, board.GP9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Layers support
# https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/layers.md
layers = Layers()
keyboard.modules.append(layers)

# Split support
# https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/split_keyboards.md#split_side
split = Split(
    split_type=SplitType.UART,
    split_side=side,
    split_target_left=True, # main split is left (to which the USB cable will be connceted)
    data_pin=board.GP20,         # Jack connector SDA_1 (1)
    data_pin2=board.GP21,        # Jack connector SCL_1 (2)
    uart_flip=True,              # TX is connected to TX (noticed this just now, but thankfully there's this option, that can flip them)
    # use_pio=True,               # not sure, if I need this
    uart_interval=10,
)
keyboard.modules.append(split)

# --- RGB SK6812 per-key LEDs ---
rgb = RGB(
    pixel_pin=board.GP0,   # LED_DIN
    num_pixels=17,
    val=150, # brightness
    rgb_order=(0, 1, 2), # why is (1, 0, 2)/GRB the default?!
)
keyboard.extensions.append(rgb)

# OLED
i2c = busio.I2C(board.GP11, board.GP10)
display_driver = SSD1306(i2c=i2c)
display = Display(
    display=display_driver,
    width=128,
    height=32,
    entries=[
        TextEntry(text="HELLO:", x=0, y=0),
        TextEntry(text="WORLD", x=0, y=30)
        brightness=1.0
    ],
)
keyboard.extensions.append(display)

# Layout
LAYOUT_LEFT = [
    KC.B,    KC.Y,    KC.O,    KC.U,    KC.QUOT,
    KC.C,    KC.I,    KC.E,    KC.A,    KC.COMM,
    KC.G,    KC.X,    KC.J,    KC.K,    KC.MINS,
                            KC.LSFT,    KC.SPC,
]

LAYOUT_RIGHT = [
    KC.SCLN,  KC.L,    KC.D,    KC.W,    KC.V,
    KC.DOT,   KC.H,    KC.T,    KC.S,    KC.N,
    KC.SLSH,  KC.R,    KC.M,    KC.F,    KC.P,
    KC.ENT,   KC.MO(1)
]

MO_FN = KC.MO(1)

keyboard.keymap = [
    LAYOUT_LEFT + LAYOUT_RIGHT,
    # layer 1
    [
        KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,
        KC.EXLM, KC.AT, KC.HASH, KC.DLR, KC.PERC,
        KC.GRV, KC.TILD, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO

        KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN,
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO
    ],
]

if __name__ == '__main__':
    keyboard.go()

import board
import digitalio
#import adafruit_dotstar
import time
from adafruit_debouncer import Button
#from switches.gpio import GPIO as Switches

#import usb_hid

#from adafruit_hid.keyboard import Keyboard
#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
#from adafruit_hid.keycode import Keycode

#from adafruit_hid.consumer_control import ConsumerControl
#from adafruit_hid.consumer_control_code import ConsumerControlCode
#cc = ConsumerControl(usb_hid.devices)

#pixels=adafruit_dotstar.DotStar(board.GP10, board.GP11,3)
#kbd = Keyboard(usb_hid.devices)
#layout = KeyboardLayoutUS(kbd)

_PINS = [board.GP17,
        board.GP22,
        board.GP6]

#intialize the array of Debounce Buttons
switches = []

#define the button array
for i in range(len(_PINS)):
    #basic Button() setup per PIN in the array above
    _pin = digitalio.DigitalInOut(_PINS[i])
    _pin.direction = digitalio.Direction.INPUT
    _pin.pull = digitalio.Pull.UP
    #adafruit_debouncer.Button(pin: Union[ROValueIO, Callable[[], bool]],
    #                          short_duration_ms: int = 200,
    #                          long_duration_ms: int = 500,
    #                          value_when_pressed: bool = False,
    #                            **kwargs)
    _switches = Button(_pin)
    switches.append(_switches)

while True:
    for k in range(len(switches)):
        switches[k].update()
        if switches[k].long_press:
            print("Long Press", k)
        if switches[k].short_count != 0:
            print("Short Press Count =", switches[k].short_count, "k = ", k)
        if switches[k].long_press and switches[k].short_count == 1:
            print("That's a long double press !" , k)
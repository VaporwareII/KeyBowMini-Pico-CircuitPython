import board
import digitalio
import adafruit_dotstar as dotstar
import random
import time
from adafruit_debouncer import Button

import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Set up consumer control (used to send media key presses)
consumer_control = ConsumerControl(usb_hid.devices)

#IO locations
_PINS = [board.GP17,
        board.GP22,
        board.GP6]
NUM_KEYS = len(_PINS)
#LED locations
_LEDS = [2,
         1,
         0]

def random_color():
    return random.randrange(0, 7) * 32

#intialize the array of LEDs
pixels=dotstar.DotStar(board.GP10, board.GP11, NUM_KEYS, brightness=0.2)
#initialize Debounce Buttons
switches = []

#define the button array per PIN in the array above
for i in range(len(_PINS)):
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
    
# Our layers. The key of item in the layer dictionary is the key number on
# Keybow to map to, and the value is the key press to send.

# Note that keys 0-3 are reserved as the modifier and layer selector keys 
# respectively.

layer_1 =     {0: Keycode.ZERO,
               1: Keycode.ONE,
               2: Keycode.FOUR
               }

layer_2 =     {0: "pack ",
               1: "my ",
               2: "box "
               }

layer_3 =     {0: ConsumerControlCode.MUTE,
               1: ConsumerControlCode.VOLUME_DECREMENT,
               2: ConsumerControlCode.VOLUME_INCREMENT
               }

layers =      {0: layer_1,
               1: layer_2,
               2: layer_3
               }
# Define the modifier key and layer selector keys
modifier = [0]
selectors = [1,2]

# Start on layer 1
current_layer = 0

# The colours for each layer
colours = {0: (255, 0, 255),
           1: (0, 255, 255),
           2: (255, 255, 0)}

layer_keys = range(4, 16)
# Set the LEDs for each key in the current layer
for x in range(NUM_KEYS):
    pixels[_LEDS[x]] = colours[current_layer]
 
# To prevent the strings (as opposed to single key presses) that are sent from 
# refiring on a single key press, the debounce time for the strings has to be 
# longer.
short_debounce = 0.03
long_debounce = 0.15
debounce = 0.03
fired = False

while True:
    # Always remember to call keybow.update()!
    for k in range(NUM_KEYS):
        switches[k].update()
        if current_layer == -1 and switches[k].short_count != 0:
            current_layer = k
            for layer in layers.keys():
                pixels[_LEDS[layer]] = colours[current_layer]
        
        elif switches[k].long_press and switches[k].short_count == 1:
            print("That's a long double press !" , k)
            pixels[_LEDS[k]] = (random_color(), random_color(), random_color())
            
        elif switches[k].long_press:
            if k is 0:
                print("MODIFIER TRIGGER", k)
                #pixels[_LEDS[k]] = (0,0,0)
                # If the modifier key is held, light up the layer selector keys
                for layer in layers.keys():
                    pixels[_LEDS[layer]] = colours[layer]
                    current_layer = -1
            else:
                print("Long Press", k)
        elif switches[k].short_count != 0:
            print("Short Press Count =", switches[k].short_count, "k = ", k)
            key_press = layers[current_layer][k]
            if current_layer == 0:
                debounce = short_debounce
                #print(key_press, "current_layer ", current_layer)
                keyboard.send(key_press)
            elif current_layer == 1:
                debounce = long_debounce
                #print(key_press, "current_layer ", current_layer)
                layout.write(key_press)
            elif current_layer == 2:
                debounce = short_debounce
                #print(key_press, "current_layer ", current_layer)
                consumer_control.send(key_press)

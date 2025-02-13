import board
import digitalio
import adafruit_dotstar
import time
from adafruit_debouncer import Button

import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
cc = ConsumerControl(usb_hid.devices)

pixels=adafruit_dotstar.DotStar(board.GP10, board.GP11,3)
kbd = Keyboard(usb_hid.devices)
# we're americans :)
layout = KeyboardLayoutUS(kbd)

class KeyLight:
    def __init__(self,keynum,pinnum,lednum,press_string,press_func):
        self.keynum=keynum
        self.pinnum=pinnum
        self.lednum=lednum
        self.press_string=press_string
        self.press_func=press_func
        self.pressed=False
        self.set_base_color((self.keynum*100,0,255-(self.keynum*100) , 0.5))
        self.activate_pin()

    def activate_pin(self):
        self.pin=digitalio.DigitalInOut(self.pinnum)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.UP
        self.pin.switch_to_input(pull=digitalio.Pull.UP)

    def set_pixel(self,color):
        pixels[self.lednum]=color

    def get_pixel(self):
        return pixels[self.lednum]

    def set_base_color(self,color):
        self.base_color=color
        self.set_pixel(color)

    def key_pressed(self):
        self.pressed=True

    def key_was_pressed(self):
        return self.pressed

    def key_released(self):
        self.pressed=False

    def key_down(self):
        return self.pin.value==False


macro_n=0

def key_macroinckey(kdb,layout):
    global macro_n
    layout.write(f"Macro {macro_n}")  
    macro_n += 1

def key_mac_undo(kdb,layout):
    kbd.press(Keycode.COMMAND,Keycode.Z)
    kbd.release_all()

# Raise volume.
def key_vol_up(kdb,layout):
    cc.send(ConsumerControlCode.VOLUME_INCREMENT)

# Lower volume.
def key_vol_down(kdb,layout):
    cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    
# Pause or resume playback.
def key_play_pause(kdb,layout):
    cc.send(ConsumerControlCode.PLAY_PAUSE)
    
# Pause or resume playback.
def key_mute(kdb,layout):
    cc.send(ConsumerControlCode.MUTE)

keyArray=[]
#                 KeyLight(keynum,pinnum,lednum,press_string,press_func)
#keyArray.append( KeyLight( 0, board.GP17,   0,  None, key_macroinckey))
keyArray.append( KeyLight( 0, board.GP17,   2,  None, key_mute))
keyArray.append( KeyLight( 1, board.GP22,   1,  None, key_vol_up))
keyArray.append( KeyLight( 2, board.GP6,    0,  None, key_vol_down))
#keyArray.append( KeyLight( 0, board.GP7,   3,  None, key_macroinckey))
#keyArray.append( KeyLight( 1, board.GP8,   7,  "1",  None))
#keyArray.append( KeyLight( 2, board.GP27,  11, "2",  None))
#keyArray.append( KeyLight( 3, board.GP9,   2,  "3",  None))
#keyArray.append( KeyLight( 4, board.GP26,  6,  "4",  None))
#keyArray.append( KeyLight( 5, board.GP10,  10, "5",  None))
#keyArray.append( KeyLight( 6, board.GP11,  1,  "6",  None))
#keyArray.append( KeyLight( 7, board.GP18,  5,  "7",  None))
#keyArray.append( KeyLight( 8, board.GP12,  9,  "8",  None))
#keyArray.append( KeyLight( 9, board.GP16,  0,  "9",  None))
#keyArray.append( KeyLight( 10, board.GP17, 4,  "Ten", None))
#keyArray.append( KeyLight( 11, board.GP14, 8,  "Eleven", None))

#while True:
#    switch.update()
#    if switch.long_press:
#        print("Long Press")
#    if switch.short_count != 0:
#        print("Short Press Count =", switch.short_count)
#   if switch.long_press and switch.short_count == 1:
#        print("That's a long double press !")
        
while True:
    keydown=False
    for k in keyArray:
        if k.key_down():
            if not k.key_was_pressed(): 
                k.set_pixel((255,255,255,0.5))
                k.key_pressed()
                if k.press_func!=None:
                    k.press_func(kbd,layout)
                else:
                    layout.write(k.press_string)
            else:
                pass # held down behaviour here
        elif k.key_was_pressed():
                k.key_released()
                k.set_pixel(k.base_color)
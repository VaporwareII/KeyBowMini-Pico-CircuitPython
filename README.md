# KeyBowMini-Pico-CircuitPython

Read about the original 12-key keybow project at [Codepope's Development Hell](https://codepope.dev/post/revamping-pi-keybow-into-pico-keybow/)

I used a Waveshare Pico-to-HAT since the originally suggested pico hat never came back in stock. Note there aren't any pictures of the waveshare pico-to-hat adapter with a pHAT attached, but the HAT is rotated 180 degrees so that it will not overhang the Pico in the middle slot.  i.e. the keybow keys are hanging over the edge of the adapter board. https://www.waveshare.com/product/raspberry-pi/boards-kits/raspberry-pi-pico-cat/pico-to-hat.htm
![IMG_0993](https://user-images.githubusercontent.com/12813849/205525103-1e25fcb0-55c4-41fb-8f7a-c86c74293519.jpeg)

the GPIO numbers changed according to https://pinout.xyz/pinout/keybow_mini#.
LED controls are on GP10 (data) and GP11 (clock)
Key 1 is Blue / left
Key 2 is Pink / middle
Key 3 is Magenta / right

Key 1 is GP17
Key 2 is GP22
Key 3 is GP06

LEDs are backwards
Key1 is LED2
Key2 is LED1
Key3 is LED0

KeybowMiniMacro.py is the modified macro code from https://github.com/codepope/KeyBow-Pico-CircuitPython. I have added a copy renamed as code.py to have it automatically run when you plug in the Pico.

keybow_mini.py is from https://github.com/dglaude/circuitpython_phat_on_pico but with the GPIO changed for this adapter.

testLights.py and testRainbow.py are just for testing the LEDs, since I had trouble with them until I figured out the controls were on GP10 & GP11 not on GP2 & GP3

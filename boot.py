import storage
import board, digitalio

# If not pressed, the key will be at +V (due to the pull-up).
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/circuitpy-midi-serial#circuitpy-mass-storage-device-3096583-4
button = digitalio.DigitalInOut(board.GP17)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Disable devices only if button is not pressed.
if button.value:
    print(f"boot: button not pressed, disabling drive")
    storage.disable_usb_drive()
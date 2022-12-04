import time
import board
import adafruit_dotstar
from rainbowio import colorwheel

pixels=adafruit_dotstar.DotStar(board.GP10, board.GP11,3)

for i in range(3):
    pixels[i]=(i*20,0,255-(i*20) , 0.5)
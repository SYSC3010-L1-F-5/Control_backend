"""

    This hardware test tests Sense HAT by using flask test

    Author: Haoyu Xu

"""

from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
BLACK = [0, 0, 0]
RED = [255, 0, 0]
YELLOW = [255, 255, 0]
BLUE = [54, 113, 248]

def test_on(app, client):
    sense.show_letter("M", back_colour=RED)
    sleep(1)
    sense.show_letter("H", text_colour=BLACK, back_colour=YELLOW)
    sleep(1)
    sense.show_letter("H", back_colour=RED)
    sleep(1)
    sense.show_letter("H", text_colour=BLACK, back_colour=BLUE)
    sleep(1)
    sense.show_letter("T", back_colour=RED)
    sleep(1)
    sense.show_letter("T", back_colour=YELLOW)
    sleep(1)
    sense.show_letter("P", back_colour=RED)
    sleep(1)
    sense.show_letter("P", text_colour=BLACK, back_colour=BLUE)
    sleep(1)

def test_off(app, client):
    sense.clear()
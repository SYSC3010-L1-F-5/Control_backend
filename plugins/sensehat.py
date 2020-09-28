"""

    SenseHAT for quick status check

    Author: Haoyu Xu

"""
from time import sleep
from sense_hat import SenseHat

from lib.configs import Configs
config = Configs().get()

black = [0, 0, 0]
red = [255, 0, 0]
yellow = [255, 255, 0]
blue = [54, 113, 248]

class SenseHAT:

    def __init__(self):
        self.sense = SenseHat()

    def on(self, event):
        type = event["type"]
        if type == "motion_detected":
            self.sense.show_letter("M", back_colour=red)
        else:
            details = int(event["details"])
            if type == "temperature":
                if details > config["threshold"]["temperature"]["upper"]:
                    self.sense.show_letter("T", back_colour=red)
                elif details < config["threshold"]["temperature"]["lower"]:
                    self.sense.show_letter("T", text_colour=black, back_colour=blue)
            elif type == "humidity":
                if details > config["threshold"]["humidity"]["upper"]:
                    self.sense.show_letter("H", back_colour=red)
                elif details < config["threshold"]["humidity"]["lower"]:
                    self.sense.show_letter("H", text_colour=black, back_colour=blue)
            elif type == "pressure":
                if details > config["threshold"]["pressure"]["upper"]:
                    self.sense.show_letter("P", back_colour=red)
                elif details < config["threshold"]["pressure"]["lower"]:
                    self.sense.show_letter("P", text_colour=black, back_colour=blue)

    def off(self):
        self.sense.clear()
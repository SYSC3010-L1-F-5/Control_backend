"""

    SenseHAT for quick status check

    Author: Haoyu Xu

"""
from sense_hat import SenseHat

BLACK = [0, 0, 0]
RED = [255, 0, 0]
YELLOW = [255, 255, 0]
BLUE = [54, 113, 248]

class SenseHAT:

    def __init__(self, config):
        """

            self.sense: access SenseHAT
            self.config: system config

        """
        self.sense = SenseHat()
        self.config = config

    def on(self, event):
        """
        
            Turn on SenseHAT LEDs with inital letter and corresponding background color

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """

        type = event["type"]
        if type == "motion_detected":
            self.sense.show_letter("M", back_colour=RED)
        else:
            details = int(event["details"])
            if type == "temperature":
                if details > self.config["threshold"]["temperature"]["upper"]:
                    self.sense.show_letter("T", back_colour=RED)
                elif details < self.config["threshold"]["temperature"]["lower"]:
                    self.sense.show_letter("T", text_colour=BLACK, back_colour=BLUE)
            elif type == "humidity":
                if details > self.config["threshold"]["humidity"]["upper"]:
                    self.sense.show_letter("H", back_colour=RED)
                elif details < self.config["threshold"]["humidity"]["lower"]:
                    self.sense.show_letter("H", text_colour=BLACK, back_colour=BLUE)
            elif type == "pressure":
                if details > self.config["threshold"]["pressure"]["upper"]:
                    self.sense.show_letter("P", back_colour=RED)
                elif details < self.config["threshold"]["pressure"]["lower"]:
                    self.sense.show_letter("P", text_colour=BLACK, back_colour=BLUE)

    def off(self, event):
        """
        
            Turn off SenseHAT LEDs

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """
        self.sense.clear()

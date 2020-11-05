"""

    Alarm system

    Author: Haoyu Xu

"""

class Alarm:

    def __init__(self, config):
        """

            self.sense: access SenseHAT
            self.config: system config

        """
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
            return
        else:
            return

    def off(self, event):
        """
        
            Turn off SenseHAT LEDs

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """
        return

"""

    Alert system

    alert.mp3: acquire from https://www.youtube.com/watch?v=BQI1Fvp6rBw
    notification.mp3: acquire from https://www.youtube.com/watch?v=qtkbydBmz0o

    Author: Haoyu Xu

"""
from pygame import mixer
import pathlib
import os
class Alert:

    def __init__(self, config):
        """

            self.config: system config
            self.path: plugin file path
            self.sound: sound configuration from config.yml

        """
        self.config = config
        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "alert")
        self.sound = config["plugins"]["alert"]["type"]
        mixer.init()

    def on(self, event):
        """
        
            Start to play sound

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """

        type = event["type"]

        # prevent the playing sound from getting overridden
        if mixer.music.get_busy() == 0:
            mixer.music.load(os.path.join(self.path, self.sound[type]["file"]))
            mixer.music.play(loops=self.sound[type]["times"])

    def off(self, event):
        """
        
            Stop playing the sound

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """
        mixer.music.fadeout(100)
        # unload requires pygame 2.0, which is a pain to install
        # mixer.music.unload()

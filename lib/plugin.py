"""

    All plugin related methods will be here
    Author: Haoyu Xu

"""

from lib.configs import Configs
config = Configs().get()

if config["plugins"]["SenseHAT"] is True:
    from plugins.sensehat import SenseHAT
    plugin = SenseHAT(config)

class Plugin:

    def __init__(self):
        self.debug = False

    def on(self, event=None):
        plugin.on(event)

    def off(self, event=None):
        plugin.off()
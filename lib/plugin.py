"""

    All plugin related methods will be here
    Author: Haoyu Xu

"""

from route.config import Config
CONFIG = Config().fetch()

if CONFIG["plugins"]["SenseHAT"] is True:
    from plugins.sensehat import SenseHAT
    PLUGIN = SenseHAT(CONFIG)

class Plugin:

    def __init__(self):
        return

    def on(self, event=None):
        """
        
            Set the status of enabled plugin to "on"

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """
        
        PLUGIN.on(event)

    def off(self, event=None):
        """
        
            Set the status of enabled plugin to "off"

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """

        PLUGIN.off(event)

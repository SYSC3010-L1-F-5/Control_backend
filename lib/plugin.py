"""

    All plugin related methods will be here
    Author: Haoyu Xu

"""
from lib.libconfig import LibConfig
CONFIG = LibConfig().fetch()

plugin_list = []

if CONFIG["plugins"]["SenseHAT"] is True:
    try:
        from plugins.sensehat import SenseHAT
        plugin_list.append(SenseHAT(CONFIG))
    except Exception as e:
        print(e)

if CONFIG["plugins"]["alert"]["enable"] is True:
    try:
        from plugins.alert import Alert
        plugin_list.append(Alert(CONFIG))
    except Exception as e:
        print(e)

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
        for plugin in plugin_list:
            plugin.on(event)

    def off(self, event=None):
        """
        
            Set the status of enabled plugin to "off"

            Args:
                self: access global variables
                event: an event that triggers the plugin
        
        """
        for plugin in plugin_list:
            plugin.off(event)

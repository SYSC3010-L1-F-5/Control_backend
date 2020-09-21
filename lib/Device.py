"""

    All device related methods will be here
    Author: Haoyu Xu

"""

class Device:
    
    def __init__(self, name, key):
        self.name = name # device name
        self.key = key # access key

    def connect(self):
        """
        
            This method connects the device to the system
        
        """
"""

    All device related methods will be here
    Author: Haoyu Xu

"""

from flask_restful import Resource

class Device(Resource):
    
    def __init__(self):
        self.operation = None
        self.zone = None # device zone
        self.type = None # device type
        self.name = None # device name
        self.key = None # access key

    def get(self, operation, zone, type, name):
        self.operation = operation
        self.zone = zone
        self.type = type
        self.name = name
        return {
            "operation": self.operation,
            "zone": self.zone,
            "type": self.type,
            "name": self.name
        }

    def connect(self):
        """
        
            This method connects the device to the system
        
        """
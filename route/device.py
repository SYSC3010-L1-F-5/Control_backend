"""

    All device related methods will be here

    Only add method can user zone, type, name; others like
    delete can only be access by key

    Author: Haoyu Xu

    - GET: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    - POST: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
    - PUT: The PUT method replaces all current representations of the target resource with the request payload.
    - DELETE: The DELETE method deletes the specified resource.

    Todos:
        - add operation will be accessing by POST
        - delete operation will be accessing by DEL
        - device pulse will be accessing by POST

"""

from flask_restful import Resource
from lib.key import Key
from lib.database import Database

from lib.message import Message
message = Message()

class Device(Resource):
    
    def __init__(self):
        self.operation = None
        self.zone = None # device zone
        self.type = None # device type
        self.name = None # device name
        self.key = None # access key
        self.database = Database("devices")

    @message.response
    def post(self, operation, zone, type, name):
        """
        
            This method is used by flask restful to 
            provide api access

            Args:
                self: access global variables
                operation: add a device
                zone: where the device locates
                type: device type
                name: device name
            
            Returns:
                string: the accessing key or error
                int: status code
        
        """
        self.operation = operation
        self.zone = zone
        self.type = type
        self.name = name

        if operation == "add":
            return self.__connect()

    def __connect(self):
        """
        
            This method connects the device to the system

            Todos:
                - check if the same palce has the same named device
                    in database

            Args:
                self: access global variables
        
        """

        self.key = Key(device={
            "zone": self.zone,
            "type": self.type,
            "name": self.name
        }).generate()

        device = {
            "zone": self.zone,
            "type": self.type,
            "name": self.name,
            "key": self.key
        }

        flag = self.database.insert(data=device)

        if flag is True:
            return self.key, 200
        else:
            return "Device exists", 403 

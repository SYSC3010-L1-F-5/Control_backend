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
        - device pulse will be accessing by PUT

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
    def get(self):
        """

            This method provides all devices infomation 
            to frontend requires user access key

        """

        return "get", 200

    @message.response
    def post(self, zone=None, type=None, name=None):
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
        if (zone is None) or (type is None) or (name is None):
            return  "", 404

        
        self.operation = operation
        self.zone = zone
        self.type = type
        self.name = name
        return self.__connect()

    @message.response
    def delete(self, key):
        """
        
            This method is used by flask restful to 
            delete device

            Args:
                self: access global variables
                key: device key
            
            Returns:
                string: the accessing key or error
                int: status code
        
        """

        if key is not None:
            return "delete", 200
        


        return "", 404

    @message.response
    def put(self, key=None):
        """
        
            This method is used by flask restful to 
            get device pulse

            Args:
                self: access global variables
                key: device key
            
            Returns:
                string: the accessing key or error
                int: status code
        
        """
        if key is not None:
            return "pulse", 200
        


        return "", 404

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

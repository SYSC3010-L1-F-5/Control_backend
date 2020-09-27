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

from flask_restful import Resource, reqparse
from lib.key import Key
from lib.database import Database

from lib.message import Message
message = Message()

parser = reqparse.RequestParser()

class Device(Resource):
    
    def __init__(self):
        self.ip = None # device ip
        self.port = None # device port
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
        
        return self.database.get(), 200

    @message.response
    def post(self):
        """
        
            This method is used by flask restful to 
            provide api access

            Todos:
                - change to parser.parse_args() type

            Args:
                self: access global variables
            
            Returns:
                string: the accessing key or error
                int: status code
        
        """

        parser.add_argument('ip', type=str, help='Device IP')
        parser.add_argument('port', type=int, help='Device port')
        parser.add_argument('zone', type=str, help='Device Zone')
        parser.add_argument('type', type=str, help='Device Type')
        parser.add_argument('name', type=str, help='Device Name')
        args = parser.parse_args(strict=True)

        self.ip = args["ip"]
        self.port = args["port"]
        self.zone = args["zone"]
        self.type = args["type"]
        self.name = args["name"]

        self.key = Key().generate()

        device = {
            "ip": self.ip,
            "port": self.port,
            "zone": self.zone,
            "type": self.type,
            "name": self.name,
            "key": self.key,
            "pulse": -1
        }

        flag = self.database.insert(data=device)

        if flag is True:
            return self.key, 200
        else:
            return "Device exists", 403 

    @message.response
    def delete(self):
        """
        
            This method is used by flask restful to 
            delete device

            Args:
                self: access global variables
            
            Returns:
                string: the accessing key or error
                int: status code
        
        """
        parser.add_argument('key', type=str, help='Device Key')
        args = parser.parse_args(strict=True)

        self.key = args["key"]
        status = self.database.remove(self.key)

        if status is True:
            return "Device is deleted", 200
        else:
            return "Device not found", 404
            

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

 

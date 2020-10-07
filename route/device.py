"""

    All device related methods will be here

    Only add method can user zone, type, name; others like
    delete can only be access by key

    TODO:
        - send an email when a device is offline/online

    Author: Haoyu Xu

    - GET: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    - POST: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
    - PUT: The PUT method replaces all current representations of the target resource with the request payload.
    - DELETE: The DELETE method deletes the specified resource.

"""

from flask_restful import Resource, reqparse, request
from lib.key import Key
from lib.database import Database

from lib.message import Message
MESSAGE = Message()

PARASER = reqparse.RequestParser()

class Device(Resource):
    
    def __init__(self):
        """

            self.ip: device ip
            self.port: device port
            self.zone: device zone
            self.type: device type
            self.name: device name
            self.key: access key
            self.database: connect to devices table in the databse

        """
        self.ip = None
        self.port = None
        self.zone = None
        self.type = None
        self.name = None
        self.key = None
        self.database = Database("devices")

    @MESSAGE.response
    def get(self, key=None):
        """

            This method provides all devices/specific device infomation 
            to frontend

            Args:
                self: access global variables
                key: device key

            Returns:
                json: device list/device details
                int: status code

        """

        # /deivces
        if request.path.split("/")[1] == "devices":

            order = {
                    "name": "pulse",
                    "value": "DESC"
                }

            return self.database.get(order=order), 200
        
        # /device/<key>
        if request.path.split("/")[2] == key:
            details = self.details(key)
            if details is not None:
                return details, 200
            else:
                return "Device not found", 404
        
        return "", 404

    @MESSAGE.response
    def post(self):
        """
        
            This method adds a device into database

            Args:
                self: access global variables
            
            Returns:
                string: the accessing key or error
                int: status code
        
        """

        if request.path.split("/")[2] != "add":
            return "", 404
        
        PARASER.add_argument('ip', type=str, help='Device IP')
        PARASER.add_argument('port', type=int, help='Device port')
        PARASER.add_argument('zone', type=str, help='Device Zone')
        PARASER.add_argument('type', type=str, help='Device Type')
        PARASER.add_argument('name', type=str, help='Device Name')
        args = PARASER.parse_args(strict=True)
        
        if args["ip"] and args["port"] and args["zone"] and args["type"] and args["name"] is not None \
        and \
        args["ip"] and args["port"] and args["zone"] and args["type"] and args["name"] != "":
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
        else:
            return "The request has unfulfilled fields", 401

    @MESSAGE.response
    def delete(self):
        """
        
            This method is used by flask restful to 
            delete device

            Args:
                self: access global variables
            
            Returns:
                string: deleted or not
                int: status code
        
        """
        if request.path.split("/")[2] != "delete":
            return "", 404

        PARASER.add_argument('key', type=str, help='Device Key')
        args = PARASER.parse_args(strict=True)

        if args["key"] is not None and args["key"] != "": 
            self.key = args["key"]
            status = self.database.remove(self.key)

            if status is True:
                return "Device is deleted", 200
            else:
                return "Device not found", 404
        else:
            return "The request has unfulfilled fields", 401
            

    @MESSAGE.response
    def put(self):
        """
        
            This method is used by flask restful to 
            get device pulse

            Args:
                self: access global variables
                key: device key
            
            Returns:
                string: pulsed or not
                int: status code
        
        """
        if request.path.split("/")[1] != "pulse":
            return "", 404

        PARASER.add_argument('who', type=str, help='Device Key')
        args = PARASER.parse_args(strict=True)
        if args["who"] is not None and args["who"] != "": 
            self.key = args["who"]
            
            status = self.database.update(self.key)

            if status is True:
                return "Pulsed", 200
            else:
                return "Device not found", 404
        else:
            return "The request has unfulfilled fields", 401

    def is_exists(self, key):
        """

            Check if a device exists in the database

            Args:
                self: access global variables
                key: device key
            
            Returns: 
                bool: True if exists, False otherwise

        """

        data = self.details(key)

        if data is None:
            return False
        else:
            return True

    def details(self, key):
        """

            Return device details

            Args:
                self: access global variables
                key: device key
            
            Returns:
                json: device details

        """

        where = {
            "name": "key",
            "value": key
        }

        data = self.database.get(where=where)

        # only one entity should be returnd
        if len(data) == 0:
            return None
        else:
            return data[0]
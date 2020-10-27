"""

    All device related methods will be here

    Only add method can user zone, type, name; others like
    delete can only be access by key

    TODO:
        - send an email when a device is offline/online
        - enable or disable device

    Author: Haoyu Xu

    - GET: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
    - POST: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
    - PUT: The PUT method replaces all current representations of the target resource with the request payload.
    - DELETE: The DELETE method deletes the specified resource.

"""
import time
import json
from flask_restful import Resource, reqparse, request
from lib.libdevice import LibDevice
LIBDEVICE = LibDevice()
from lib.libevent import LibEvent
LIBEVENT = LibEvent()
from lib.libuser import LibUser
LIBUSER = LibUser()
from lib.message import response

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
            self.uuid: device uuid
            self.auth_uuid: use for authentication
            self.auth_otp: use for authentication

        """
        self.ip = None
        self.port = None
        self.zone = None
        self.type = None
        self.name = None
        self.key = None
        self.uuid = None
        self.auth_uuid = None
        self.auth_otp = None

    @response
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

        # check url
        urls = [
            "/devices",
            "/device/{key}".format(key=key)
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400
        
        PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
        PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
        args = PARASER.parse_args(strict=True)
        self.auth_uuid = args["X-UUID"]
        self.auth_otp = args["X-OTP"]

        if LIBUSER.check_otp(uuid=self.auth_uuid, otp=self.auth_otp) is False:
            # /deivces
            if path.split("/")[1] == "devices":

                devices = LIBDEVICE.get_all_devices()
                if devices is not None:
                    # hide device key
                    for item in devices:
                        item["key"] = ""

                return devices, 200
            
            # /device/<key>
            if path.split("/")[2] == key:
                details = LIBDEVICE.details(key)
                if details is not None:
                    events = LIBEVENT.device(key)
                    if events is not None:
                        # Hide the device key
                        for item in events:
                            item["device"] = ""
                    details["key"] = ""
                    message = dict(
                        device = details,
                        events = events
                    )
                    return message, 200
                else:
                    return "Device not found", 404
            
            return "", 404
        else:
            return "You are unauthorized", 401

    @response
    def post(self):
        """
        
            This method adds a device into database

            Args:
                self: access global variables
            
            Returns:
                string: the accessing key or error
                int: status code
        
        """

        # check url
        urls = [
            "/device/add"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        if path.split("/")[2] != "add":
            return "", 404
        
        PARASER.add_argument('ip', type=str, help='Device IP')
        PARASER.add_argument('port', type=int, help='Device port')
        PARASER.add_argument('zone', type=str, help='Device Zone')
        PARASER.add_argument('type', type=str, help='Device Type')
        PARASER.add_argument('name', type=str, help='Device Name')
        PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
        PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
        args = PARASER.parse_args(strict=True)
        self.ip = args["ip"]
        self.port = args["port"]
        self.zone = args["zone"]
        self.type = args["type"]
        self.name = args["name"]
        self.auth_uuid = args["X-UUID"]
        self.auth_otp = args["X-OTP"]

        if LIBUSER.check_otp(uuid=self.auth_uuid, otp=self.auth_otp) is False:
            if LIBUSER.is_admin(self.auth_uuid):
                if self.__is_empty_or_none(self.ip, self.port, self.zone, self.type, self.name) is False:

                    device = {
                        "ip": self.ip,
                        "port": self.port,
                        "zone": self.zone,
                        "type": self.type,
                        "name": self.name
                    }

                    self.key = LIBDEVICE.add_device(device)

                    if self.key is not None:
                        return self.key, 200
                    else:
                        return "Device exists", 403
                else:
                    return "The request has unfulfilled fields", 400
            else:
                return "You don't have this permission", 403
        else:
            return "You are unauthorized", 401

    @response
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
        # check url
        urls = [
            "/device/delete"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        if path.split("/")[2] != "delete":
            return "", 404

        PARASER.add_argument('key', type=str, help='Device Key')
        PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
        PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
        args = PARASER.parse_args(strict=True)
        self.auth_uuid = args["X-UUID"]
        self.auth_otp = args["X-OTP"] 

        if LIBUSER.check_otp(uuid=self.auth_uuid, otp=self.auth_otp) is False:
            if LIBUSER.is_admin(self.auth_uuid):
                if args["key"] is not None and args["key"] != "": 
                    self.key = args["key"]
                    is_deleted = LIBDEVICE.delete_device(self.key)

                    if is_deleted is True:
                        return "Device is deleted", 200
                    else:
                        return "Device not found", 404
                else:
                    return "The request has unfulfilled fields", 400
            else:
                return "You don't have this permission", 403
        else:
            return "You are unauthorized", 401
            
    @response
    def put(self):
        """
        
            This method is used by flask restful to 
            get device pulse, or update the device

            Args:
                self: access global variables
            
            Returns:
                string: pulsed or not
                int: status code
        
        """
        # check url
        urls = [
            "/pulse",
            "/device/update"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        if path.split("/")[1] == "pulse":
            PARASER.add_argument('who', type=str, help='Device Key')
            args = PARASER.parse_args(strict=True)
            if args["who"] is not None and args["who"] != "": 
                self.key = args["who"]
                set = {
                    "name": "pulse",
                    "value": int(time.time() * 1000)
                }
                is_updated = LIBDEVICE.update_device(self.key, set)

                if is_updated is True:
                    return "Pulsed", 200
                else:
                    return "Device not found", 404
            else:
                return "The request has unfulfilled fields", 400

        elif path.split("/")[2] == "update":
            PARASER.add_argument('key', type=str, help='Device key')
            PARASER.add_argument('fields', type=str, help='Fields to be updated')
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.auth_uuid = args["X-UUID"]
            self.auth_otp = args["X-OTP"] 
            if LIBUSER.check_otp(uuid=self.auth_uuid, otp=self.auth_otp) is False:
                if LIBUSER.is_admin(self.auth_uuid):
                    if args["key"] is not None and args["key"] != "": 
                        self.key = args["key"]
                        is_exists = LIBDEVICE.is_exists(self.key)
                        if is_exists is True:
                            if args["fields"] is not None and args["fields"] != "":
                                fields = json.loads(args["fields"].replace("'", '"'))
                                if "ip" in fields:
                                    if self.__is_empty_or_none(fields["ip"]) is False:
                                        self.ip = fields["ip"]
                                        set = {
                                            "name": "ip",
                                            "value": self.ip
                                        }
                                        LIBDEVICE.update_device(self.key, set)
                                    else:
                                        return "The request has unfulfilled fields", 401

                                if "port" in fields:
                                    if self.__is_empty_or_none(fields["port"]) is False:
                                        
                                        self.port = fields["port"]
                                        set = {
                                            "name": "port",
                                            "value": self.port
                                        }
                                        LIBDEVICE.update_device(self.key, set)
                                    else:
                                        return "The request has unfulfilled fields", 401
                        
                                if "zone" in fields:
                                    if self.__is_empty_or_none(fields["zone"]) is False:
                                        self.zone = fields["zone"]
                                        set = {
                                            "name": "zone",
                                            "value": self.zone
                                        }
                                        LIBDEVICE.update_device(self.key, set)
                                    else:
                                        return "The request has unfulfilled fields", 401

                                if "type" in fields:
                                    if self.__is_empty_or_none(fields["type"]) is False:
                                        self.type = fields["type"]
                                        set = {
                                            "name": "type",
                                            "value": self.type
                                        }
                                        LIBDEVICE.update_device(self.key, set)
                                    else:
                                        return "The request has unfulfilled fields", 401

                                if "name" in fields:
                                    if self.__is_empty_or_none(fields["name"]) is False:
                                        self.name = fields["name"]
                                        set = {
                                            "name": "name",
                                            "value": self.name
                                        }
                                        LIBDEVICE.update_device(self.key, set)
                                    else:
                                        return "The request has unfulfilled fields", 401

                                # update device uuid
                                details = LIBDEVICE.details(self.key)
                                device = {
                                    "ip": details["ip"],
                                    "port": details["port"],
                                    "zone": details["zone"],
                                    "type": details["type"],
                                    "name": details["name"]
                                }
                                uuid_field = ";".join("{key}:{value}".format(key=key, value=value) for key, value in device.items())
                                self.uuid = LIBDEVICE.uuid(uuid_field)
                                set = {
                                        "name": "uuid",
                                        "value": self.uuid
                                    }
                                LIBDEVICE.update_device(self.key, set)
                            else:
                                return "Device is not updated", 400
                            
                            return "Device is updated", 200
                        else:
                            return "Device not found", 404
                    else:
                        return "The request has unfulfilled fields", 400
                else:
                    return "You don't have this permission", 403
            else:
                return "You are unauthorized", 401
        else:
            return "", 404
    
    def __is_empty_or_none(self, *argv):
        """

            Check if there is a empty or None in the args

            Args:
                self: access global variables
                *argv: argument(s) to check if is None or "" or " " with spaces
            
            Returns:
                bool: True if exists, False otherwise

        """
        is_exists = True

        for arg in argv:
            if arg is None:
                is_exists = True
                break
            elif str(arg).replace(" ", "") == "":
                is_exists = True
                break
            else:
                is_exists = False
        
        return is_exists
        
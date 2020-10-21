"""

    All user related methods will be here
    Author: Haoyu Xu

    For every api access that needs user authentication, add this line
    PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
    PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')

    OTP should expire in 30 mins

    TODO:
        - PUT /set/: user setting related

"""

from flask_restful import Resource, reqparse, request
from lib.message import response
from lib.libuser import LibUser
LIBUSER = LibUser()
from lib.libconfig import LibConfig
CONFIG = LibConfig().fetch()

PARASER = reqparse.RequestParser()

class User(Resource):

    def __init__(self):
        self.uuid = None
        self.otp = None
        self.perm = False
    
    @response
    def get(self):
        """

            This method provides user details

            Args:
                self: access global variables

            Returns:
                json: device list/device details
                int: status code

        """

        # check url
        urls = [
            "/user"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400
        
        if path.split("/")[1] == "user":
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]

            if self.__is_empty_or_none(self.uuid, self.otp) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    user_details = LIBUSER.details(self.uuid)
                    user_details["uuid"] = ""
                    user_details["password"] = ""
                    user_details["otp"] = ""
                    user_details["otp_time"] = ""
                    return user_details, 200
                else:
                    return "You are unauthorized", 401

        else:
            return "", 404

    @response
    def post(self):
        """

            This method provides user login

            Args:
                self: access global variables

            Returns:
                json: device list/device details
                int: status code

        """

        # check url
        urls = [
            "/user/login"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        if path.split("/")[2] == "login":
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-PERM', type=bool, location='headers', help='Remember Me')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.perm = args["X-PERM"]

            if self.__is_empty_or_none(self.uuid, self.perm) is False:
                user_otp = LIBUSER.get_otp(uuid=self.uuid, permanent=self.perm)
                if user_otp is None:
                    return "Either username or password is incorrect", 401
                else:
                    return user_otp, 200
        else:
            return "", 404

    @response
    def put(self):
        """

            This method updates user

            Args:
                self: access global variables

            Returns:
                json: device list/device details
                int: status code

        """

        # check url
        urls = [
            "/user/update"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400

        if path.split("/")[2] == "update":
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]

            if self.__is_empty_or_none(self.uuid, self.otp) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    
                    return "", 200
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
"""

    All user related methods will be here
    Author: Haoyu Xu

    For every api access that needs user authentication, add this line
    UUID SPEC: "username:<username>;password:<password md5>"
    PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
    PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')

    OTP should expire in 30 mins

"""
import json
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
    def get(self, uuid=None):
        """

            This method provides user details

            Args:
                self: access global variables
                uuid: user uuid

            Returns:
                json: user details
                int: status code

        """

        # check url
        urls = [
            "/user",
            "/users",
            "/user/{uuid}".format(uuid=uuid)
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400
        
        if path.split("/")[1] == "user" and uuid is None:
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]

            if self.__is_empty_or_none(self.uuid, self.otp) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    user_details = LIBUSER.details(self.uuid)
                    user_details["password"] = ""
                    user_details["otp"] = ""
                    user_details["otp_time"] = ""
                    return user_details, 200
                else:
                    return "You are unauthorized", 401
        elif path.split("/")[1] == "users":
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]
            if self.__is_empty_or_none(self.uuid, self.otp) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    if LIBUSER.is_admin(self.uuid):
                        users = LIBUSER.get_all_users()
                        if users is not None:
                            for item in users:
                                item["password"] = ""
                                item["otp"] = ""
                                item["otp_time"] = ""
                        return users, 200
                    else:
                        return "You don't have this permission", 403
                else:
                    return "You are unauthorized", 401
            else:
                return "The request has unfulfilled fields", 400
        elif path.split("/")[2] == uuid:
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]
            if self.__is_empty_or_none(self.uuid, self.otp) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    if LIBUSER.is_admin(self.uuid):
                        user_details = LIBUSER.details(uuid)
                        user_details["password"] = ""
                        user_details["otp"] = ""
                        user_details["otp_time"] = ""
                        return user_details, 200
                    else:
                        return "You don't have this permission", 403
                else:
                    return "You are unauthorized", 401
            else:
                return "The request has unfulfilled fields", 400
        else:
            return "", 404

    @response
    def delete(self):
        """

            This method provides user logout

            Args:
                self: access global variables

            Returns:
                string: logout status
                int: status code

        """
        # check url
        urls = [
            "/user/logout",
            "/user/delete"
        ]
        path = request.path
        if path not in urls:
            return "Incorrect HTTP Method", 400
        
        if path.split("/")[2] == "logout":
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]

            if self.__is_empty_or_none(self.uuid, self.otp) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    is_logged_out = LIBUSER.otp_to_expire(self.uuid)
                    if is_logged_out is True:
                        return "You are logged out", 200
                    else:
                        return "Unexpected behaviour", 500 # should never reach this line
                else:
                    return "You are unauthorized", 401
            else:
                return "The request has unfulfilled fields", 400
        elif path.split("/")[2] == "delete":
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]

            if self.__is_empty_or_none(self.uuid, self.otp) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    fields = json.loads(args["fields"])

                    if LIBUSER.is_admin(self.uuid):
                        if self.__is_empty_or_none(fields["uuid"]) is False:
                            self.uuid = fields["uuid"]

                    is_deleted = LIBUSER.delete_user(self.uuid)
                    if is_deleted is True:
                        return "User is deleted", 200
                    else:
                        return "User not found", 404
                else:
                    return "You are unauthorized", 401
            else:
                return "The request has unfulfilled fields", 400
        else:
            return "", 404

    @response
    def post(self):
        """

            This method provides user login

            Args:
                self: access global variables

            Returns:
                string: user otp
                int: status code

        """

        # check url
        urls = [
            "/user/login",
            "/user/add"
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
                return "The request has unfulfilled fields", 400
        elif path.split("/")[2] == "add":
            PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
            PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')
            PARASER.add_argument('fields', type=str, help='Fields to be updated')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]
            fields = args["fields"]

            if self.__is_empty_or_none(self.uuid, self.otp, fields) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    if LIBUSER.is_admin(self.uuid):
                        fields = json.loads(args["fields"])
                        # "username:<username>;password:<password md5>;type:<type>"
                        if self.__is_empty_or_none(fields["username"], fields["password"], fields["type"]) is False:
                            user = {
                                "username": fields["username"],
                                "password": fields["password"]
                            }
                            is_added = LIBUSER.add_user(user, fields["type"])
                            if is_added is True:
                                return "User is added", 200
                            else:
                                return "Unexpected behaviour", 500
                    else:
                        return "You don't have this permission", 403
                else:
                    return "You are unauthorized", 401
            else:
                return "The request has unfulfilled fields", 400
        else:
            return "", 404

    @response
    def put(self):
        """

            This method updates user

            Args:
                self: access global variables

            Returns:
                string: update status
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
            PARASER.add_argument('fields', type=str, help='Fields to be updated')
            args = PARASER.parse_args(strict=True)
            self.uuid = args["X-UUID"]
            self.otp = args["X-OTP"]
            fields = args["fields"]

            if self.__is_empty_or_none(self.uuid, self.otp, fields) is False:
                if LIBUSER.check_otp(uuid=self.uuid, otp=self.otp) is False:
                    fields = json.loads(args["fields"])

                    if LIBUSER.is_admin(self.uuid):
                        if "uuid" in fields:
                            self.uuid = fields["uuid"]
                            if "type" in fields:
                                set = {
                                    "name": "type",
                                    "value": fields["type"]
                                }
                                LIBUSER.update_user(self.uuid, set)

                    if "username" in fields:
                        set = {
                            "name": "username",
                            "value": fields["username"]
                        }
                        LIBUSER.update_user(self.uuid, set)

                    if "password" in fields:
                        set = {
                            "name": "password",
                            "value": fields["password"]
                        }
                        LIBUSER.update_user(self.uuid, set)
                    
                    if "email" in fields:
                        set = {
                            "name": "email",
                            "value": fields["email"]
                        }
                        LIBUSER.update_user(self.uuid, set)

                    # update user uuid
                    user_details = LIBUSER.details(self.uuid)
                    user = {
                        "username": user_details["username"],
                        "password": user_details["password"]
                    }
                    old_uuid = self.uuid
                    self.uuid = LIBUSER.uuid(user)
                    set = {
                        "name": "uuid",
                        "value": self.uuid
                    }
                    LIBUSER.update_user(old_uuid, set)

                    return "User is updated", 200
                else:
                    return "You are unauthorized", 401
            else:
                return "The request has unfulfilled fields", 400
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

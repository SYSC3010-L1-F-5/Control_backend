"""

    All configuration related methods will be here
    Author: Haoyu Xu

"""
from flask_restful import Resource, reqparse
from lib.libconfig import LibConfig
from lib.message import response
from lib.libuser import LibUser
LIBUSER = LibUser()
PARASER = reqparse.RequestParser()

class Config(Resource):

    def __init__(self):
        """
        
            self.config: system config
            self.auth_uuid: use for authentication
            self.auth_otp: use for authentication

        """
        self.config = LibConfig().fetch()
        self.auth_uuid = None
        self.auth_otp = None

    @response
    def get(self):
        """

            This method provides the configuration of the system
            to the frontend

            Args:
                self: access global variables

            Returns:
                str: system config
                int: status code

        """
        PARASER.add_argument('X-UUID', type=str, location='headers', help='User UUID')
        PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')

        args = PARASER.parse_args()
        self.auth_uuid = args["X-UUID"]
        self.auth_otp = args["X-OTP"]

        if LIBUSER.check_otp(uuid=self.auth_uuid, otp=self.auth_otp) is False:
            if LIBUSER.is_admin(self.auth_uuid):
                return self.config, 200
            else:
                return "You don't have this permission", 403
        else:
            return "You are unauthorized", 401


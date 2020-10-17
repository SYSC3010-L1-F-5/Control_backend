"""

    All user related methods will be here
    Author: Haoyu Xu

    For every api access that needs user authentication, add this line
    PARASER.add_argument('X-OTP', type=str, location='headers', help='User OTP')

    OTP should expire in 30 mins

    TODO:
        - POST /set/: user setting related
        - GET /<string:username>/: get user profile

"""

from flask_restful import Resource
from lib.message import response

from lib.libconfig import LibConfig
CONFIG = LibConfig().fetch()

class User(Resource):

    def __init__(self):
        return
    
    @response
    def get(self):
        return CONFIG["users"]
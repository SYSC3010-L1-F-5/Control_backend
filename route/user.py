"""

    All user related methods will be here
    Author: Haoyu Xu

    TODO: not in SYSC 3010 project scope
        - POST /set/: user setting related
        - GET /<string:username>/: get user profile

"""

from flask_restful import Resource
from .config import Config

class User(Resource):

    def __init__(self):
        self.config = Config()
    
    def get(self):
        return self.config.get()["users"]
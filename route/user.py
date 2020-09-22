"""

    All user related methods will be here
    Author: Haoyu Xu

"""

from flask_restful import Resource
from .config import Config

class User(Resource):

    def __init__(self):
        self.config = Config()
    
    def get(self):
        return self.config.get()["users"]
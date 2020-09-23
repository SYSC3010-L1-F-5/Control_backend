"""

    All configuration related methods will be here
    Author: Haoyu Xu

"""

from flask_restful import Resource
from lib.configs import Configs

from lib.message import Message
message = Message()

class Config(Resource):

    def __init__(self):
        self.config = Configs().get()

    @message.response
    def get(self):
        return self.config, 200
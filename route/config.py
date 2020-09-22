"""

    All configuration related methods will be here
    Author: Haoyu Xu

"""

from flask_restful import Resource
from lib.message import Message
import os
import pathlib
import yaml

message = Message()

class Config(Resource):

    def __init__(self):
        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "config.yml")
        self.config = yaml.safe_load(open(self.path, "r"))

    @message.response
    def get(self):
        return self.config, 200
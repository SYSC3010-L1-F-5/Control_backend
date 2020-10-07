"""

    All configuration related methods will be here
    Author: Haoyu Xu

"""
from flask_restful import Resource
from lib.libconfig import LibConfig

from lib.message import Message
MESSAGE = Message()

class Config(Resource):

    def __init__(self):
        """
        
            self.config: system config

        """
        self.config = LibConfig().fetch()

    @MESSAGE.response
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

        return self.config, 200

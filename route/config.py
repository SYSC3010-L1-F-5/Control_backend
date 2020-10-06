"""

    All configuration related methods will be here
    Author: Haoyu Xu

"""
import os
import pathlib
import yaml

from flask_restful import Resource

from lib.message import Message
MESSAGE = Message()

class Config(Resource):

    def __init__(self):
        """

            self.path: config path
            self.config: system config

        """
        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "config.yml")
        self.config = yaml.safe_load(open(self.path, "r"))

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

    def fetch(self):
        """

            This method provides the configuration of the system

            Args:
                self: access global variables

            Returns:
                str: system config

        """

        return self.config
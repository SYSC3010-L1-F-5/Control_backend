"""

    All configuration related methods will be here
    Author: Haoyu Xu

"""

import os
import pathlib
import yaml


class Configs:

    def __init__(self):
        """

            self.path: config path
            self.configs: loaded config

        """
        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "config.yml")
        self.configs = yaml.safe_load(open(self.path, "r"))

    def get(self):
        """

            This method provides the configuration of the system

            Args:
                self: access global variables

            Returns:
                str: system config

        """

        return self.configs
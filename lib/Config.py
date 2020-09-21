"""

    All configuration related methods will be here
    Author: Haoyu Xu

"""

import os
import pathlib
import yaml

class Config:

    def __init__(self):
        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "config.yml")
        self.config = yaml.safe_load(open(self.path, "r"))

    def get(self):
        return self.config
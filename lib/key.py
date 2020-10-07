"""

    All access key related methods will be here
    Author: Haoyu Xu

"""

import secrets
import uuid
import hashlib

class Key:

    def __init__(self, key=None):
        """

            self.key: the key to do stuff

        """
        self.key = key
    
    def generate(self):
        """

            This method add a new device to the
            database, and assign a access key for it

            Args:
                self: accessing global parameters
                device: the device to be added

            Returns:
                str: the generated key

        """

        self.key = secrets.token_urlsafe(32)

        return self.key

    def uuid(self, seed=None):
        """

            This method generates uuid

            Todo:
                - use string to generate reproducilbe uuid (have no idea)

            Arg:
                seed: used to generate reproducilbe uuid

            Returns:
                string: uuid
            
        """

        self.key = str(uuid.uuid4())

        return self.key

    def md5(self, seed):
        """

            This method generates md5 of a string

            Arg:
                seed: a string to generate md5

            Returns:
                string: uuid
            
        """

        self.key = str(hashlib.md5(seed.encode('utf-8')).hexdigest())

        return self.key

    def get(self):
        """

            This method returns the assigned key
            of the device

            Args:
                self: accessing global parameters

            Returns:
                string: the access key

        """

        return self.key

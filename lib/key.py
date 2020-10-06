"""

    All access key related methods will be here
    Author: Haoyu Xu

"""

import secrets
import uuid

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

        self.key = self.__generate()

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

        return str(uuid.uuid4())

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

    def __generate(self):
        """

            This method generates access key

            Args:
                self: accessing global parameters

            Returns:
                string: the access key

        """
        return secrets.token_urlsafe(32)

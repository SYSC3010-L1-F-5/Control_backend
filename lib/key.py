"""

    All access key related methods will be here
    Author: Haoyu Xu

"""

import os
import secrets

class Key:

    def __init__(self, device=None, key=None):
        self.key = key
        self.device = device
    
    def generate(self):
        """

            This method add a new device to the
            database, and assign a access key for it

            Todos:
                - databse operations

            Args:
                self: accessing global parameters
                device: the device to be added

            Returns:
                bool: True if the key successful added, False
                        otherwise

        """

        self.key = self.__generate()

        return self.key

    def get(self, device=None):
        """

            This method returns the assigned key
            of the device

            Todos:
                - databse operations, such as read the 
                    key from database

            Args:
                self: accessing global parameters
                device: the device to be added, if 
                        is None, then the key will be 
                        associated to self.device,
                        otherwise, return False

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


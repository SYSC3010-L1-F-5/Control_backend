"""

    All access key related methods will be here
    Author: Haoyu Xu

"""

from base64 import b64encode
import os

class Key:

    def __init__(self):
        self.key = None
        self.device = None

    def generate(self):
        """

            This method generates access key

            Args:
                self: accessing global parameters

            Returns:
                string: the access key

        """
        return b64encode(os.urandom(64)).decode('utf-8')
    
    def add(self, device):
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
        if device is None:
            return False
        
        self.device = device
        self.key = self.generate()

        return True

    def get_key(self, device=None):
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

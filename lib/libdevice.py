
from lib.database import Database

class LibDevice:

    def __init__(self):
        """
        
            self.database: connect to devices table in the databse

        """
        self.database = Database("devices")

    def is_exists(self, key):
        """

            Check if a device exists in the database

            Args:
                self: access global variables
                key: device key
            
            Returns: 
                bool: True if exists, False otherwise

        """

        data = self.details(key)

        if data is None:
            return False
        else:
            return True

    def details(self, key):
        """

            Return device details

            Args:
                self: access global variables
                key: device key
            
            Returns:
                json: device details

        """

        where = {
            "name": "key",
            "value": key
        }

        data = self.database.get(where=where)

        # only one entity should be returnd
        if len(data) == 0:
            return None
        else:
            return data[0]
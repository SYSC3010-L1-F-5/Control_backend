from lib.database import Database

class LibEvent:

    def __init__(self):
        """
        
            self.database: connect to event table in the databse

        """
        self.database = Database("events")

    def is_exists(self, uuid):
        """

            Check if a event exists in the database

            Args:
                self: access global variables
                uuid: event uuid
            
            Returns: 
                bool: True if exists, False otherwise

        """

        data = self.details(uuid)

        if data is None:
            return False
        else:
            return True

    def details(self, uuid):
        """

            Return event details

            Args:
                self: access global variables
                uuid: event uuid
            
            Returns:
                json: event uuid

        """

        where = {
            "name": "uuid",
            "value": uuid
        }

        data = self.database.get(where=where)

        # only one entity should be returnd
        if len(data) == 0:
            return None
        else:
            return data[0]

    def device(self, key):
        """

            Return all events added by a specfic device

            Args:
                self: access global variables
                key: device key
            
            Returns:
                json: events

        """
        where = {
            "name": "device",
            "value": key
        }

        data = self.database.get(where=where)

        if len(data) == 0:
            return None
        else:
            return data[0]
from lib.database import Database
from lib.key import Key

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

        order = {
            "name": "time",
            "value": "DESC"
        }

        data = self.database.get(where=where, order=order)

        if len(data) == 0:
            return None
        else:
            return data

    def uuid(self, details):
        """

            Return uuid of specfic details

            Args:
                self: access global variables
                details: detials to get uuid
            
            Returns:
                string: uuid

        """
        return Key().uuid(details)

    def get_all_events(self):
        """

            Return all event details

            Args:
                self: access global variables
            
            Returns:
                json: all event details

        """
        order = {
            "name": "time",
            "value": "DESC"
        }

        events = self.database.get(order=order)

        if len(events) == 0:
            return None
        else:
            return events

    def add_event(self, details):
        """

            Add an event to the database

            Arg:
                self: access global variables
                details: event details

            Returns:
                string: event uuid if successful, None otherwise

        """
        event_uuid = self.uuid(details)
        details["uuid"] = event_uuid
        details["hidden"] = 0

        is_inserted = self.database.insert(data=details)

        if is_inserted is True:
            return event_uuid
        else:
            return None

    def delete_event(self, uuid):
        """

            Delete an existing event

            Args:
                self: access global variables
                uuid: event uuid

            Returns:
                boolean: True if successful, Falase otherwise

        """
        is_exists = self.is_exists(uuid)
        is_deleted = False
        if is_exists is True:
            is_deleted = self.database.remove(uuid)

        return is_deleted

    def update_event(self, uuid, set):
        """

            Update an existing event

            Args:
                self: access global variables
                uuid: event uuid
                set: field to be updated

            Returns:
                boolean: True if successful, Falase otherwise

        """
        is_exists = self.is_exists(uuid)
        is_updated = False
        if is_exists is True:
            where = {
                "name": "uuid",
                "value": uuid
            }
            is_updated = self.database.update(where=where, set=set)

        print(is_updated)
        return is_updated
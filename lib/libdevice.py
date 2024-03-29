
from lib.database import Database
from lib.key import Key

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

    def is_exists_uuid(self, uuid):
        """

            Check if a device exists in the database

            Args:
                self: access global variables
                uuid: device uuid
            
            Returns: 
                bool: True if exists, False otherwise

        """

        where = {
            "name": "uuid",
            "value": uuid
        }

        data = Database("devices").get(where=where)

        # only one entity should be returnd
        if len(data) == 0:
            return False
        else:
            return True

    def is_enabled(self, key):
        """

            Check if a device is enabled

            Args:
                self: access global variables
                key: device key
            
            Returns: 
                bool: True if enabled, False otherwise

        """

        data = self.details(key)
        
        if data is None:
            return False
        else:
            if data["is_enabled"] == 1:
                return True
            else:
                return False

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

        data = Database("devices").get(where=where)

        # only one entity should be returnd
        if len(data) == 0:
            return None
        else:
            return data[0]
    
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

    def get_all_devices(self):
        """

            Return all device details

            Args:
                self: access global variables
            
            Returns:
                json: all device details

        """
        order = {
            "name": "pulse",
            "value": "DESC"
        }

        devices = Database("devices").get(order=order)

        if len(devices) == 0:
            return None
        else:
            return devices

    def add_device(self, details):
        """

            Add a device to the database

            Arg:
                self: access global variables
                details: device details

            Returns:
                string: device key if successful, None otherwise

        """
        is_enabled = details["is_enabled"]
        details.pop("is_enabled")
        uuid_field = ";".join("{key}:{value}".format(key=key, value=value) for key, value in details.items())
        device_uuid = self.uuid(uuid_field)
        device_key = Key().generate()
        details["uuid"] = device_uuid
        details["key"] = device_key
        details["pulse"] = -1
        details["is_enabled"] = is_enabled

        is_inserted = Database("devices").insert(data=details)

        if is_inserted is True:
            return device_key
        else:
            return None

    def delete_device(self, key):
        """

            Delete an existing device

            Args:
                self: access global variables
                key: device key

            Returns:
                boolean: True if successful, Falase otherwise

        """
        is_exists = self.is_exists(key)
        is_deleted = False
        if is_exists is True:
            where = {
                "name": "key",
                "value": key
            }
            is_deleted = Database("devices").remove(where)

        return is_deleted

    def update_device(self, key, set):
        """

            Update an existing device

            Args:
                self: access global variables
                key: device key
                set: field to be updated

            Returns:
                boolean: True if successful, Falase otherwise

        """
        is_exists = self.is_exists(key)
        is_updated = False
        if is_exists is True:
            where = {
                "name": "key",
                "value": key
            }
            is_updated = Database("devices").update(where=where, set=set)

        return is_updated
        
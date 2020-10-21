import time

from lib.database import Database
from lib.key import Key
from lib.libconfig import LibConfig
CONFIG = LibConfig().fetch()
import hashlib

class LibUser:

    def __init__(self):
        """
        
            self.database: connect to users table in the databse

        """
        self.database = Database("users")

    def initialize(self):
        """

            Initialize user configs from config.yml

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        users = CONFIG["users"]

        for key, value in users.items():
            user = {
                "username": key,
                "password": Key().md5(value)
            }
            
            user_uuid = self.uuid(";".join("{field_key}:{field_value}".format(field_key=field_key, field_value=field_value) for field_key, field_value in user.items()))
            item_struct = {
                "uuid": user_uuid,
                "username": user["username"],
                "password": user["password"],
                "email": "",
                "type": "admin",
                "otp": "",
                "otp_time": -1
            }
            is_inserted = self.database.insert(data=item_struct)

            if is_inserted is True:
                print("User {user} {uuid} is initialized".format(user=key, uuid=user_uuid))
            else:
                print("User {user} {uuid} already exists or failed to initialize".format(user=key, uuid=user_uuid))

    def add_user(self, details, user_type):
        """

            Add a new user to database

            Args:
                self: accessing global parameters
                details: user details
                user_type: user type

            Returns:
                bool: True if successful, False otherwise

        """

        user_uuid = self.uuid(";".join("{field_key}:{field_value}".format(field_key=field_key, field_value=field_value) for field_key, field_value in details.items()))
        item_struct = {
            "uuid": user_uuid,
            "username": details["username"],
            "password": details["password"],
            "email": "",
            "type": user_type,
            "otp": "",
            "otp_time": -1
        }
        is_inserted = self.database.insert(data=item_struct)

        return is_inserted

    def delete_user(self, uuid):
        """

            Delete an existing user in database

            Args:
                self: accessing global parameters
                details: user details
                user_type: user type

            Returns:
                bool: True if successful, False otherwise

        """

        is_exists = self.is_exists(uuid)
        is_deleted = False
        if is_exists is True:
            is_deleted = self.database.remove(uuid)

        return is_deleted
        
    def is_exists(self, uuid):
        """

            Check if a user exists in the database

            Args:
                self: access global variables
                uuid: user uuid
            
            Returns: 
                bool: True if exists, False otherwise

        """

        data = self.details(uuid)

        if data is None:
            return False
        else:
            return True
    
    def get_otp(self, uuid, permanent=False):
        """

            Generate an OTP when a user login

            Args:
                self: accessing global parameters
                uuid: user uuid
                permanent: if user choose to "Remember Me"

            Returns:
                string: user otp

        """

        # check is_exists
        is_exists = self.is_exists(uuid)

        if is_exists is True:
            data_struct = {
                "otp": Key().generate(),
                "otp_time": int(time.time() * 1000) + (30 * 60 * 1000) # by default, user login expires in 30 mins
            }
            if permanent is True:
                data_struct["otp_time"] = -1

            # insert into database
            for key, value in data_struct.items():
                set = {
                    "name": key,
                    "value": value
                }
                self.update_user(uuid=uuid, set=set)
        
            return data_struct["otp"]
        
        else:
            return None
    
    def check_otp(self, uuid, otp):
        """

            Check if an OTP is expired

            Args:
                self: accessing global parameters
                uuid: user uuid
                otp: otp to check

            Returns:
                boolean: True if expired, False otherwise

        """
        is_expired = True

        user_details = self.details(uuid)

        if user_details is not None:
            current_time = int(time.time() * 1000)
            if otp == user_details["otp"]:
                if user_details["otp_time"] == -1:
                    is_expired = False
                elif current_time < user_details["otp_time"]:
                    is_expired = False
                else:
                    is_expired = True
        
        return is_expired

    def otp_to_expire(self, uuid):
        """

            Make an OTP expire when a user logout

            Args:
                self: accessing global parameters
                uuid: user uuid

            Returns:
                boolean: True if expired, False otherwise

        """
        is_expired = False
        
        user_details = self.details(uuid)

        if user_details is not None:
            set = {
                "name": "otp",
                "value": None
            }
            self.update_user(uuid=uuid, set=set)
            set = {
                "name": "otp_time",
                "value": 0
            }
            self.update_user(uuid=uuid, set=set)
            is_expired = True

        return is_expired

    def details(self, uuid):
        """

            Return user details

            Args:
                self: access global variables
                uuid: event uuid
            
            Returns:
                json: user details

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

    def update_user(self, uuid, set):
        """

            Update an existing user

            Args:
                self: access global variables
                uuid: user uuid
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

        return is_updated
        
    def uuid(self, details):
        """

            Return uuid of specfic details

            Args:
                self: access global variables
                details: detials to get uuid
            
            Returns:
                string: uuid

        """
        return Key().sha256(details)

    def is_admin(self, uuid):
        """

            Check if a user is admin

            Args:
                self: access global variables
                uuid: uuid
            
            Returns:
                boolean: True if a user is admin, False otherwise

        """
        is_admin = False

        user_details = self.details(uuid)

        if user_details is not None:
            is_admin = user_details["type"] == "admin"

        return is_admin

    def get_all_users(self):
        """

            Return all user details

            Args:
                self: access global variables
            
            Returns:
                json: all delete_user details

        """
        order = {
            "name": "username",
            "value": "ASC"
        }

        users = self.database.get(order=order)

        if len(users) == 0:
            return None
        else:
            return users
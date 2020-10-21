import time

from lib.database import Database
from lib.key import Key
from lib.libconfig import LibConfig
CONFIG = LibConfig().fetch()

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
                "password": value
            }
            user_uuid = Key().uuid(user)
            item_struct = {
                "uuid": user_uuid,
                "username": key,
                "password": value,
                "email": "",
                "type": "",
                "otp": "",
                "otp_time": -1
            }
            is_inserted = self.database.insert(data=item_struct)

            if is_inserted is True:
                print("User {user} is initialized".format(user=key))
            else:
                print("User {user} already exists or failed to initialize".format(user=key))
        
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
            where = {
                "name": "uuid",
                "value": uuid
            }

            for key, value in data_struct.items():
                set = {
                    "name": key,
                    "value": value
                }
                self.database.update(where=where, set=set)
        
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

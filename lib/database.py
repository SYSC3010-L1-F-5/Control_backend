"""

    All databse related methods will be here
    Author: Haoyu Xu

"""

import os
import json
import sqlite3
import pathlib
import time

from lib.configs import Configs
configs = Configs().get()

tables = {
    "devices": {
        "ip": "text",
        "port": "numeric",
        "zone": "text",
        "type": "text",
        "name": "text",
        "key": "text",
        "pulse": "numeric"
    },
    "users": {
        "username": "text",
        "password": "text",
        "email": "text",
        "type": "text"
    },
    "events": {
        "uuid": "text",
        "device": "text",
        "time": "numeric",
        "type": "text",
        "details": "text",
        "hidden": "boolean" # 0 => false, 1 => true
    }
}

class Database:

    def __init__(self, table=None):
        self.database = None # database filename
        self.table = table # the table to be access
        self.connection = None # database connection
        self.path = None # database path
        self.cursor = None

    def create(self):
        """

            This method creates a database files

            Todos:
                - handle exceptions
                - if database exists, verify tables:
                    - successful: pass
                    - fail: backup the old one and create a new one

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        status = False

        if configs["database"]["name"].endswith(".db") is False:
            self.database = configs["database"]["name"] + ".db"
        else:
            self.database = configs["database"]["name"]

        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", self.database)

        status = self.__check_db()

        self.connection.close()

        return status

    def insert(self, data, table=None):
        """

            This method inserts data to databse table

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters
                data: the data
                table: wheere the data is stored

            Returns:
                bool: True if successful, False otherwise

        """
        status = False
        
        if self.table is None and table is None:
            return False
        elif self.table is None:
            self.table = table
        
        self.__connect_db()

        is_exists = self.__verify_data("insert", data)

        if self.table == "devices" and is_exists is False:
            self.cursor.execute('''insert into devices values (?, ?, ?, ?, ?, ?, ?)''', (data["ip"], data["port"], data["zone"], data["type"], data["name"], data["key"], data["pulse"]))
            self.connection.commit()
            status = True

        if self.table == "users" and is_exists is False:
            self.cursor.execute('''insert into users values (?, ?, ?, ?)''', (data["username"], data["password"], data["email"], data["type"]))
            self.connection.commit()
            status = True

        if self.table == "events" and is_exists is False:
            self.cursor.execute('''insert into events values (?, ?, ?, ?, ?, ?)''', (data["uuid"], data["device"], data["time"], data["type"], data["details"], data["hidden"]))
            self.connection.commit()
            status = True

        self.connection.close()
        return status

    def remove(self, data, table=None):
        """

            This method deletes data in databse table

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters
                data: the data
                table: wheere the data is stored

            Returns:
                bool: True if successful, False otherwise

        """
        status = False
        
        if self.table is None and table is None:
            return False
        elif self.table is None:
            self.table = table
        
        self.__connect_db()

        where=None

        if self.table == "devices":
            where = {
                "name": "key",
                "value": data
            }
        elif self.table == "events":
            where = {
                "name": "uuid",
                "value": data
            }

        status = self.__delete_row(where=where)

        self.connection.close()
        return status

    def get(self, table=None, where=None):
        """

            This method get data from databse table

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters
                table: wheere the data is stored
                where: select specific row field in
                        {
                            "name": table_name,
                            "value": value
                        }

            Returns:
                list: empty list if the operation failed
                        list with specific table data

        """

        if self.table is None and table is None:
            return False
        elif self.table is None:
            self.table = table
        
        status = self.__connect_db()
        data = []

        if status is True:
            self.__select_table(self.table, where)
            data = [dict((self.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in self.cursor.fetchall()]

        #close the connection
        self.connection.close()

        return data

    def update(self, data, table=None):
        """

            This method update data in databse table

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters
                table: wheere the data is stored
                where: select specific row field in
                        {
                            "name": table_name,
                            "value": value
                        }

            Returns:
                list: empty list if the operation failed
                        list with specific table data

        """

        if self.table is None and table is None:
            return False
        elif self.table is None:
            self.table = table
        
        status = self.__connect_db()

        where=None
        set=None

        if self.table == "devices":
            where = {
                "name": "key",
                "value": data
            }
            set = {
                "name": "pulse",
                "value": int(time.time() * 1000)
            }
        elif self.table == "events":
            where = {
                    "name": "uuid",
                    "value": data["uuid"]
            }
            if data["type"] == "hidden":
                set = {
                    "name": "hidden",
                    "value": data["hidden"]
                }
            elif data["type"] == "details":
                set = {
                    "name": "details",
                    "value": data["details"]
                }
                print(type(set["value"]))

        if status is True:
            status = self.__update_row(where, set)

        #close the connection
        self.connection.close()

        return status

    def __check_db(self):
        """

            This method checks database, if verify databse failed
            then backup and create a new db

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        status = False

        if os.path.exists(self.path) is True:
            self.__connect_db()
            status = self.__verify_table()
            self.connection.close()
        
        if status is False:
            # verify table failed or db does not exist
            status = self.__create_db()

        return status

    def __verify_table(self):
        """

            This method verifies tables

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """

        status = False

        self.__select_table(table="devices")
        names = [description[0] for description in self.cursor.description]
        if names != ["ip", "port", "zone", "type", "name", "key", "pulse"]:
            # need some clean up here
            return status
        
        self.__select_table(table="users")
        names = [description[0] for description in self.cursor.description]
        if names != ["username", "password", "email", "type"]:
            # need some clean up here
            return status

        self.__select_table(table="events")
        names = [description[0] for description in self.cursor.description]
        if names != ["uuid", "device", "time", "type", "details", "hidden"]:
            # need some clean up here
            return status
        
        status = True
        
        return True

    def __create_db(self):
        """

            This helper method creates a database files

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        status = False

        if os.path.exists(self.path) is True:
            backup_path = self.path + '.bak'
            os.rename(self.path, backup_path)

        with open(self.path, 'w') as fp: 
            pass

        self.__connect_db()

        status = self.__initiate_table()

        return status

    def __connect_db(self):
        """

            This method connects db

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        status = False

        if configs["database"]["name"].endswith(".db") is False:
            self.database = configs["database"]["name"] + ".db"
        else:
            self.database = configs["database"]["name"]

        if self.path is None:
            self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", self.database)

        self.connection = sqlite3.connect(self.path);
        
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        return True

    def __initiate_table(self):
        """

            This method initiates tables

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """

        status = False

        status = self.__create_table(name="devices")
        status = self.__create_table(name="users")
        status = self.__create_table(name="events")

        return status

    def __create_table(self, name):
        """

            This method creates table

            Todos:
                - handle exceptions
                - add pulse to devices table
                - add events table
            
            Args:
                self: accessing global parameters
                name: table name
            
            Returns:
                bool: True if successful, False otherwise

        """

        status = False

        if name == "devices":
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS devices (
                                ip text,
                                port numeric,
                                zone text,
                                type text,
                                name text,
                                key text,
                                pulse numeric
                            ); """)
            self.connection.commit()
            status = True
        elif name == "users":
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                                username text,
                                password text,
                                email text,
                                type text
                            ); """)
            self.connection.commit()
            status = True
        elif name == "events":
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS events (
                                uuid text,
                                device text,
                                time numeric,
                                type text,
                                details text,
                                hidden boolean
                            ); """)
            self.connection.commit()
            status = True
        else:
            status = False

        return status

    def __select_table(self, table, where=None):
        """

            This method selects table

            Todos:
                - handle exceptions
            
            Args:
                self: accessing global parameters
                name: table name
                where: select specific row field in
                        {
                            "name": table_name,
                            "value": value
                        }
            
            Returns:
                string: return table data

        """
        if where is None:
            self.cursor.execute('SELECT * FROM {};'.format(table))
        else:
            self.cursor.execute('SELECT * FROM {} WHERE {}="{}";'.format(table, where["name"], where["value"]))

    def __verify_data(self, mode, data):
        """

            This method verify if data exists in the table

            Todos:
                - handle exceptions
            
            Args:
                self: accessing global parameters
                mode: insert or get
                data: data to be verified
            
            Returns:
                bool: exists => True
                        does not exist => False

        """
        flag = False

        if mode == "insert":
            self.__select_table(table=self.table)
            for row in self.cursor:
                if self.table == "devices":
                    if row["ip"] == data["ip"] and row["port"] == data["port"] and row["zone"] == data["zone"] and row["type"] == data["type"] and row["name"] == data["name"]:
                        flag = True
                        break
                elif self.table == "users":
                    if row["username"] == data["username"]:
                        flag = True
                        break
                elif self.table == "events":
                    if row["device"] == data["device"] and row["time"] == data["time"] and row["details"] == data["details"] and row["type"] == data["type"]:
                        flag = True
                        break

        return flag

    def __delete_row(self, where, table=None):
        """

            This method delete data from in the table

            Todos:
                - handle exceptions
            
            Args:
                self: accessing global parameters
                where: select specific row field in
                        {
                            "name": table_name,
                            "value": value
                        }
                table: table name
            
            Returns:
                bool: True if successful, False otherwise 

        """
        flag = False

        # should have only one entity
        self.__select_table(self.table, where)
        data = [dict((self.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in self.cursor.fetchall()]

        if len(data) == 0:
            return False
        else:
            self.cursor.execute("""DELETE FROM {} WHERE {}="{}"; """.format(self.table, where["name"], where["value"]))
            self.connection.commit()
        
        return True

    def __update_row(self, where, set, table=None):
        """

            This method update data from in the table

            Todos:
                - handle exceptions
            
            Args:
                self: accessing global parameters
                where: select specific row field in
                        {
                            "name": table_name,
                            "value": value
                        }
                set: update value
                        {
                            "name": field_name,
                            "value": value
                        }
                table: table name
            
            Returns:
                bool: True if successful, False otherwise 

        """
        flag = False

        # should have only one entity
        self.__select_table(self.table, where)
        data = [dict((self.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in self.cursor.fetchall()]

        if len(data) == 0:
            return False
        else:
            print(set, where, self.table)
            self.cursor.execute("""UPDATE {} SET {}="{}" WHERE {}="{}"; """.format(self.table, set["name"], set["value"], where["name"], where["value"]))
                
        self.connection.commit()

        return True
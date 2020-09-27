"""

    All databse related methods will be here
    Author: Haoyu Xu

"""

import os
import json
import sqlite3
import pathlib

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

        self.connection.close()
        return status

    def delete(self, key, table=None):
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
        is_exists = self.__verify_data("delete", data)



        self.connection.close()
        return status

    def get(self, table=None):
        """

            This method get data from databse table

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters
                table: wheere the data is stored

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
            self.cursor.execute('SELECT * FROM {}'.format(self.table));
            data = [dict((self.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in self.cursor.fetchall()]

        #close the connection
        self.connection.close()

        return data

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

        self.__select_table(name="devices")
        names = [description[0] for description in self.cursor.description]
        if names != ["ip", "port", "zone", "type", "name", "key", "pulse"]:
            # need some clean up here
            return status
        
        self.__select_table(name="users")
        names = [description[0] for description in self.cursor.description]
        if names != ["username", "password", "email", "type"]:
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
        else:
            status = False

        return status

    def __select_table(self, name):
        """

            This method selects table

            Todos:
                - handle exceptions
            
            Args:
                self: accessing global parameters
                name: table name
            
            Returns:
                string: return table data

        """
        self.cursor.execute('SELECT * FROM {};'.format(name))

    def __verify_data(self, mode, data):
        """

            This method verify if data exists in the table

            Todos:
                - handle exceptions
            
            Args:
                self: accessing global parameters
                mode: insert, delete or get
                data: data to be verified
            
            Returns:
                bool: exists => True
                        does not exist => False

        """
        flag = False

        if mode == "insert":
            self.__select_table(name=self.table)
            for row in self.cursor:
                if self.table == "devices":
                    if row["ip"] == data["ip"] and row["port"] == data["port"] and row["zone"] == data["zone"] and row["type"] == data["type"] and row["name"] == data["name"]:
                        flag = True
                        break
                elif self.table == "users":
                    if row["username"] == data["username"]:
                        flag = True
                        break
            
        return flag
"""

    All databse related methods will be here

    TODO:
        - handle exceptions

    Author: Haoyu Xu

"""

import os
import sqlite3
import pathlib

from lib.libconfig import LibConfig
CONFIG = LibConfig().fetch()

TABLES = {
    "devices": {
        "fields": {
            "ip": "text",
            "port": "numeric",
            "zone": "text",
            "type": "text",
            "name": "text",
            "uuid": "text",
            "key": "text",
            "pulse": "numeric"
        },
        "verifications": [
            "uuid"
        ]
    },
    "users": {
        "fields": {
            "uuid": "text",
            "username": "text",
            "password": "text",
            "email": "text",
            "type": "text",
            "otp": "text",
            "otp_time": "numeric",
            "last_login": "numeric"
        },
        "verifications": [
            "username"
        ]
    },
    "events": {
        "fields":{
            "uuid": "text",
            "device": "text",
            "time": "numeric",
            "type": "text",
            "details": "text",
            "hidden": "boolean" # 0 => false, 1 => true
        },
        "verifications": [
            "uuid"
        ]
    # },
    # "logs": {
    #     "fields": { # TODO: not in SYSC 3010 project scope
    #         "time": "numeric", # 1601330980228
    #         "user": "text", # admin
    #         "action": "text", # delete 
    #         "type": "text", # device
    #         "which": "text" # Na5adCHPj7p4X35Od_hQ8oQkDq8uImV_yGfPQ_3--UU
    #     },
    #     "verifications": [
    #         "time",
    #         "user",
    #         "action",
    #         "type",
    #         "which"
    #     ]
    # },
    # "notifications": {
    #     "fields": { # TODO: not in SYSC 3010 project scope
    #         "type": "text", # temperature
    #         "upper": "numeric", # 30
    #         "lower": "numeric", # 20
    #     },
    #     "verifications": [
    #         "type",
    #         "upper",
    #         "lower"
    #     ]
    }
}

class Database:

    def __init__(self, table=None):
        """

            self.database: database filename
            self.table: the table to be access
            self.connection: database connection
            self.path: database path
            self.cursor: databse cursor

        """

        self.database = None
        self.table = table
        self.connection = None
        self.path = None
        self.cursor = None

    def create(self):
        """

            This method creates a database files

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        status = False

        self.__set_db_name()

        self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", self.database)

        status = self.__check_db()

        self.connection.close()

        return status

    def insert(self, data):
        """

            This method inserts data to databse table

            Args:
                self: accessing global parameters
                data: the data

            Returns:
                bool: True if successful, False otherwise

        """
        status = False
        
        self.__connect_db()

        is_exists = self.__verify_data("insert", data)

        if is_exists is False:
            cols = ', '.join('"{}"'.format(col) for col in data.keys())
            values = ', '.join(':{}'.format(col) for col in data.keys())
            command = 'INSERT INTO "{table}" ({cols}) VALUES ({values})'.format(table=self.table, cols=cols, values=values)
            self.cursor.execute(command, data)
            self.connection.commit()
            status = True

        self.connection.close()
        return status

    def remove(self, where):
        """

            This method deletes data in databse table

            Args:
                self: accessing global parameters
                where: where to locate item

            Returns:
                bool: True if successful, False otherwise

        """
        status = False
        
        self.__connect_db()

        status = self.__delete_row(where=where)

        self.connection.close()

        return status

    def get(self, where=None, order=None):
        """

            This method get data from databse table

            Args:
                self: accessing global parameters
                table: wheere the data is stored
                where: select specific row field in
                        {
                            "name": field_name,
                            "value": value
                        }
                order: sort the data by specific field
                        {
                            "name": field_name,
                            "value": value, ASC | DESC
                        }

            Returns:
                list: empty list if the operation failed
                        list with specific table data

        """
        
        status = self.__connect_db()
        data = []

        if status is True:
            self.__select_table(table=self.table, where=where, order=order)
            data = self.__fetch_data()

        #close the connection
        self.connection.close()

        return data

    def update(self, where, set):
        """

            This method update data in databse table

            TODO:
                - use list/dict to update fields

            Args:
                self: accessing global parameters
                where: the field to locate the data in the database
                set:  the field to be updated

            Returns:
                list: empty list if the operation failed
                        list with specific table data

        """
        
        status = self.__connect_db()

        if status is True:
            status = self.__update_row(where, set)

        #close the connection
        self.connection.close()

        return status

    def __check_db(self):
        """

            This method checks database, if verify databse failed
            then backup and create a new db

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
            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """

        for key in TABLES:
            self.__select_table(table=key)
            db_fields = [description[0] for description in self.cursor.description]
            table_fields = [value for value in TABLES[key]["fields"]]
            if db_fields != table_fields:
                return False
        
        return True

    def __create_db(self):
        """

            This helper method creates a database files

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

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        self.__set_db_name()

        if self.path is None:
            self.path = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", self.database)

        self.connection = sqlite3.connect(self.path);
        
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        return True

    def __initiate_table(self):
        """

            This method initiates tables

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """

        status = False

        for table_name, table_fields in TABLES.items():

            fields = ", ".join("{name} {type}".format(name=key, type=value) for key, value in TABLES[table_name]["fields"].items())
        
            template = " CREATE TABLE IF NOT EXISTS {table_name} ({fields}); ".format(table_name=table_name, fields=fields)
            self.cursor.execute(template)
            self.connection.commit()
            status = True
        
        return status

    def __select_table(self, table, where=None, order=None):
        """

            This method selects table
            
            Args:
                self: accessing global parameters
                name: table name
                where: select specific row field in
                        {
                            "name": field_name,
                            "value": value
                        }
                order: sort the data by specific field
                        {
                            "name": field_name,
                            "value": value, ASC | DESC
                        }

        """
        
        if where is None and order is None:
            self.cursor.execute('SELECT * FROM {};'.format(table))
        elif order is None:
            self.cursor.execute('SELECT * FROM {} WHERE {}="{}";'.format(table, where["name"], where["value"]))
        elif where is None:
            self.cursor.execute('SELECT * FROM {} ORDER BY {} {};'.format(table, order["name"], order["value"]))
        else:
            self.cursor.execute('SELECT * FROM {} WHERE {}="{}" ORDER BY {} {};'.format(table, where["name"], where["value"], order["name"], order["value"]))

    def __verify_data(self, mode, data):
        """

            This method verify if data exists in the table
            
            Args:
                self: accessing global parameters
                mode: insert or get
                data: data to be verified
            
            Returns:
                bool: exists => True
                        does not exist => False

        """
        flags = []
        flag = False
        self.__select_table(table=self.table)

        if mode == "insert":
            for row in self.cursor:
                for key in TABLES[self.table]["verifications"]:
                    if row[key] == data[key]:
                        flags.append(True)
                    else:
                        flags.append(False)
                
                if all(flags):
                    flag = True
                    break
                else:
                    flags = []
        elif mode == "update":
            for row in self.cursor:
                for key in TABLES[self.table]["verifications"]:
                    if data["skip"] is False:
                        if row[key] == data["value"] and key == data["name"]:
                            flags.append(True)
                        else:
                            flags.append(False)
                    else:
                        flags.append(False)
                
                if all(flags):
                    flag = True
                    break
                else:
                    flags = []

        return flag

    def __delete_row(self, where):
        """

            This method delete data from in the table
            
            Args:
                self: accessing global parameters
                where: select specific row field in
                        {
                            "name": table_name,
                            "value": value
                        }
            
            Returns:
                bool: True if successful, False otherwise 

        """

        # should have only one entity
        self.__select_table(table=self.table, where=where)
        data = self.__fetch_data()

        if len(data) == 0:
            return False
        else:
            self.cursor.execute("""DELETE FROM {} WHERE {}="{}"; """.format(self.table, where["name"], where["value"]))
            self.connection.commit()
        
        return True

    def __update_row(self, where, set):
        """

            This method update data from in the table
            
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
            
            Returns:
                bool: True if successful, False otherwise 

        """

        # should have only one entity
        self.__select_table(table=self.table, where=where)
        data = self.__fetch_data()

        if len(data) == 0:
            return False
        else:

            if self.__verify_data("update", set) is False:
                self.cursor.execute("""UPDATE {} SET {}="{}" WHERE {}="{}"; """.format(self.table, set["name"], set["value"], where["name"], where["value"]))
            else:
                return False
                
        self.connection.commit()

        return True

    def __set_db_name(self):
        """

            This method sets the database name

            Args:
                self: accessing global parameters

        """

        if CONFIG["database"]["name"].endswith(".db") is False:
            self.database = CONFIG["database"]["name"] + ".db"
        else:
            self.database = CONFIG["database"]["name"]

    def __fetch_data(self):
        """

            This method fetches data from a specific table

            Args:
                self: accessing global parameters

            Returns:
                list: a list of data

        """

        return [dict((self.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in self.cursor.fetchall()]
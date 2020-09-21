"""

    All databse related methods will be here
    Author: Haoyu Xu

"""

import os
import json
import sqlite3

class Database:

    def __init__(self, database, path=None,table=None):
        self.database = database # database filename
        self.table = table # the table to be access
        self.connection = None # database connection
        self.path = None # database path
        self.cursor = None

    def create(self, path):
        """

            This method creates a database files
            By default, the db is connected after
            this operation

            Todos:
                - handle exceptions
                - if database exists, verify tables

            Args:
                self: accessing global parameters
                path: path of the database

            Returns:
                bool: True if successful, False otherwise

        """
        if self.database.endwith(".db") is False:
            self.database += ".db"

        self.path = os.path.join(path, self.database)

        with open(self.path, 'w') as fp: 
            pass

        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        return True

    def connect(self, path=None):
        """

            This method connects to a database

            Todos:
                - handle exceptions

            Args:
                self: accessing global parameters

            Returns:
                bool: True if successful, False otherwise

        """
        if self.path is None and path is None:
            return False
        elif path is None:
            self.connection = sqlite3.connect(self.path)
        else:
            self.connection = sqlite3.connect(path)
        
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
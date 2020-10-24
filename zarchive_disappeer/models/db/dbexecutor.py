"""
dbexecutor.py

Module for DBExecutor class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import sqlite3


class DBExecutor:

    def __init__(self, db_file_path):
        self.database = db_file_path

    def execute(self, *args):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(*args)
        connection.commit()
        connection.close()

    def fetch_all(self, *args):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(*args)
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        return result

    def fetch_one(self, *args):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(*args)
        result = cursor.fetchone()
        connection.commit()
        connection.close()
        return result

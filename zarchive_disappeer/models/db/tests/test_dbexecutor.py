"""
test_dbexecutor.py

Test suite for DBExecutor class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
import models.db.dbexecutor as dbexecutor
import sqlite3
import os


class TestImports(unittest.TestCase):

    def test_sqlite(self):
        self.assertEqual(sqlite3, dbexecutor.sqlite3)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.table_name = 'WTF'
        self.create_table = '''create table {} 
                            (   id integer primary key autoincrement,
                                col1 TEXT,
                                col2 TEXT
                            );
                            '''.format(self.table_name)
        self.db_file_path = 'models/db/tests/testdb.sqlite'
        self.x = dbexecutor.DBExecutor(self.db_file_path)

    def tearDown(self):
        if os.path.isfile(self.db_file_path):
            os.remove(self.db_file_path)

    def test_instance(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_path_attribute(self):
        self.assertEqual(self.db_file_path, self.x.database)

    def test_execute_method_executes_string(self):
        self.x.execute(self.create_table)
        connection = sqlite3.connect(self.db_file_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA table_info({})'.format(self.table_name))
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        self.assertTrue(len(result) > 0)

    def test_execute_method_executes_with_input(self):
        self.x.execute(self.create_table)
        command = 'INSERT INTO {} VALUES(null, ?, ?)'.format(self.table_name)
        self.x.execute(command, [1, 2])

        connection = sqlite3.connect(self.db_file_path)
        cursor = connection.cursor()
        cursor.execute('select * from {}'.format(self.table_name))
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        self.assertTrue(len(result) > 0)

    def test_fetch_all_method_returns_results(self):
        self.x.execute(self.create_table)
        command = 'INSERT INTO {} VALUES(null, ?, ?)'.format(self.table_name)
        self.x.execute(command, [1, 2])
        exec_string = "select * from {};".format(self.table_name)
        self.x.execute(exec_string)
        result = self.x.fetch_all(exec_string)
        self.assertTrue(len(result) > 0)

    def test_fetch_one_method_fetches_one(self):
        self.x.execute(self.create_table)
        command = 'INSERT INTO {} VALUES(null, ?, ?)'.format(self.table_name)
        self.x.execute(command, ['1', '2'])
        self.x.execute(command, ['3', '4'])
        exec_string = "select * from {} where col1=1;".format(self.table_name)
        self.x.execute(exec_string)
        result = self.x.fetch_one(exec_string)
        self.assertTrue(result == (1, '1', '2'))



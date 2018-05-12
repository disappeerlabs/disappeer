"""
test_dbserversynctable.py

Test module for the DBServerSyncTable module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.models.db import dbserversynctable
from disappeer.models.db.bases import abstractdbtable
from disappeer.models.db import dbexecutor
import os
import sqlite3


class TestImports(unittest.TestCase):

    def test_abstractdbtable(self):
        self.assertEqual(abstractdbtable, dbserversynctable.abstractdbtable)

    def test_sqlite3(self):
        self.assertEqual(sqlite3, dbserversynctable.sqlite3)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.db_test_file = 'models/db/tests/dbserversynctest.sqlite'
        self.x = dbserversynctable.DBServerSyncTable(self.db_test_file)

    def tearDown(self):
        if os.path.isfile(self.db_test_file):
            os.remove(self.db_test_file)

    def test_instance(self):
        self.assertIsInstance(self.x, dbserversynctable.DBServerSyncTable)

    def test_instance_executor(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_instance_abstract_table(self):
        self.assertIsInstance(self.x, abstractdbtable.AbstractDBTable)

    def test_db_executor_database_path_attribute_set(self):
        self.assertEqual(self.x.database, self.db_test_file)

    def test_table_name_class_attribute(self):
        target = 'PendingContactResponseNoncesTable'
        self.assertEqual(self.x.table_name, target)
        with self.assertRaises(AttributeError):
            self.x.table_name = 'hello'

    def test_data_row_name_class_attribute(self):
        target = 'PendingContactResponseNoncesTableRow'
        self.assertEqual(self.x.data_row_name, target)
        with self.assertRaises(AttributeError):
            self.x.data_row_name = 'hello'

    def test_table_column_names_tuple_class_attribute(self):
        target = ('value', )

        self.assertEqual(self.x.column_names_tuple, target)
        with self.assertRaises(AttributeError):
            self.x.column_names_tuple = 'hello'

    def test_insert_new_vals_inserts_new_vals(self):
        target = [('val1',), ('val2',), ('val3',)]
        self.x.insert_new_vals(target)
        result = self.x.fetch_all('select value from {}'.format(self.x.table_name))
        self.assertEqual(target, result)

    def test_fetch_all_nonces_returns_all_nonces(self):
        begin = [('val1',), ('val2',), ('val3',)]
        self.x.insert_new_vals(begin)
        target = ['val1', 'val2', 'val3']
        result = self.x.fetch_all_nonces()
        self.assertEqual(target, result)

    def test_delete_all_nonces(self):
        begin = [('val1',), ('val2',), ('val3',)]
        self.x.insert_new_vals(begin)
        self.x.insert_new_vals(begin)
        result_1 = self.x.fetch_all('select value from {}'.format(self.x.table_name))
        self.assertEqual(6, len(result_1))
        self.x.delete_all_nonces()
        result_2 = self.x.fetch_all('select value from {}'.format(self.x.table_name))
        self.assertEqual(0, len(result_2))

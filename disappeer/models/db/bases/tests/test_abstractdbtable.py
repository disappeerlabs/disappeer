"""
test_abstractdbtable.py

Test suite for the AbstractDBTable class object and module, interface for all DB table classes

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.models.db.bases import abstractdbtable
import abc
from disappeer.models.db import dbexecutor
import collections
import os


class TestImports(unittest.TestCase):

    def test_abc(self):
        self.assertEqual(abc, abstractdbtable.abc)

    def test_dbexecutor(self):
        self.assertEqual(dbexecutor, abstractdbtable.dbexecutor)

    def test_collections(self):
        self.assertEqual(collections, abstractdbtable.collections)


class MockDBTableInstance(abstractdbtable.AbstractDBTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'test_table_name'

    @property
    def data_row_name(self):
        return 'test_data_row_name'

    @property
    def column_names_tuple(self):
        return 'col_1', 'col_2', 'col_3'


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.db_test_file_path = 'models/db/bases/tests/testdb.sqlite'
        self.x = MockDBTableInstance(self.db_test_file_path)
        self.executor = dbexecutor.DBExecutor(self.db_test_file_path)

    def tearDown(self):
        if os.path.isfile(self.db_test_file_path):
            os.remove(self.db_test_file_path)

    def test_instance_executor(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_instance(self):
        self.assertIsInstance(self.x, abstractdbtable.AbstractDBTable)

    def test_metaclass_attribute(self):
        check = hasattr(self.x, '_abc_registry')
        self.assertTrue(check)

    def test_db_file_path_attribute_set(self):
        self.assertEqual(self.x.database, self.db_test_file_path)

    def test_db_table_name_property(self):
        name = 'table_name'
        check = hasattr(self.x, name)
        self.assertTrue(check)
        with self.assertRaises(AttributeError):
            self.x.table_name = 'hello'

    def test_data_row_name_property(self):
        name = 'data_row_name'
        check = hasattr(self.x, name)
        self.assertTrue(check)
        with self.assertRaises(AttributeError):
            self.x.data_row_name = 'hello'

    def test_column_names_tuple_property(self):
        name = 'column_names_tuple'
        check = hasattr(self.x, name)
        self.assertTrue(check)
        with self.assertRaises(AttributeError):
            self.x.column_names_tuple = 'hello'

    def test_create_table_string_property(self):
        name = 'create_table_string'
        check = hasattr(self.x, name)
        self.assertTrue(check)
        with self.assertRaises(AttributeError):
            self.x.create_table_string = 'hello'

    def test_create_table_string_property_returns_default_string(self):
        target = 'create table if not exists test_table_name (id integer primary key autoincrement, col_1 TEXT, col_2 TEXT, col_3 TEXT);'
        result = self.x.create_table_string
        self.assertEqual(result, target)

    def test_col_def_string(self):
        col_name_string_list = [x + ' TEXT' for x in self.x.column_names_tuple]
        target = ", ".join(col_name_string_list)
        result = self.x.col_def_string
        self.assertEqual(result, target)

    def test_create_table_method_creates_table_from_create_table_string_property(self):
        self.x.create_table()
        check_command = 'PRAGMA table_info({})'.format(self.x.table_name)
        result = self.executor.fetch_all(check_command)
        self.assertTrue(len(result) > 0)

    def test_init_method_calls_create_table(self):
        result = self.executor.fetch_all('PRAGMA table_info({})'.format(self.x.table_name))
        self.assertTrue(len(result) > 0)

    def test_create_empty_named_tuple(self):
        result = self.x.create_empty_named_tuple()
        self.assertEqual(self.x.column_names_tuple, result._fields)

    def test_build_named_tuple_method_builds_row_tuple(self):
        data_row = (1, 2, 3)
        result = self.x.build_named_tuple(data_row)
        self.assertEqual(self.x.data_row_name, type(result).__name__)
        try:
            for item in self.x.column_names_tuple:
                result.__getattribute__(item)
        except:
            self.assertTrue(False)

    def test_insert_command_string_property_returns_correct_string(self):
        target = 'insert into {} values(null, ?, ?, ?)'.format(self.x.table_name)
        result = self.x.insert_command_string
        self.assertEqual(result, target)

    def test_insert_data_row_inserts_data_row(self):
        data = ('1', '2', '3')
        self.x.insert_data_row(data)
        result = self.executor.fetch_one('select * from {};'.format(self.x.table_name))
        self.assertEqual(result[1:], data)

    def test_fetch_last_record_returns_last_record(self):
        data_row = ('1', '2', '3')
        self.x.insert_data_row(data_row)
        result = self.x.fetch_last_record()
        self.assertEqual(result, data_row)

    def test_delete_record_where_x_is_y(self):
        data_row = ('1', '2', '3')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        self.x.delete_record_where_x_equals_y('col_2', named.col_2)
        result = self.executor.fetch_all('select * from {}'.format(self.x.table_name))
        self.assertEqual(len(result), 0)

    def test_update_record_col_to_val_updates(self):
        data_row = ('1', '2', '3')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result_before = self.x.fetch_last_record()
        self.x.update_record_col_to_val_where_x_equals_y('col_1', 'xxx', 'col_3', '3')
        result_after = self.x.fetch_last_record()
        self.assertEqual(result_before.col_1, '1')
        self.assertEqual(result_after.col_1, 'xxx')



"""
test_dbcontactrequesttable.py

Test suite for the DBContactRequestTable class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.models.db import dbcontactrequesttable
from disappeer.models.db import dbexecutor
import os
import sqlite3
from disappeer.models.db.bases import abstractdbtable


class TestImports(unittest.TestCase):

    def test_abstractdbtable(self):
        self.assertEqual(abstractdbtable, dbcontactrequesttable.abstractdbtable)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.class_object = dbcontactrequesttable.DBContactRequestTable
        self.db_file_path = 'models/db/tests/testdb.sqlite'
        self.x = dbcontactrequesttable.DBContactRequestTable(self.db_file_path)

    def tearDown(self):
        if os.path.isfile(self.db_file_path):
            os.remove(self.db_file_path)

    def test_instance(self):
        self.assertIsInstance(self.x, dbcontactrequesttable.DBContactRequestTable)

    def test_instance_executor(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_instance_abstract_table(self):
        self.assertIsInstance(self.x, abstractdbtable.AbstractDBTable)

    def test_db_executor_database_path_attribute_set(self):
        self.assertEqual(self.x.database, self.db_file_path)

    def test_table_name_class_attribute(self):
        target = 'ContactRequests'
        self.assertEqual(self.x.table_name, target)
        with self.assertRaises(AttributeError):
            self.x.table_name = 'hello'

    def test_table_column_names_tuple_class_attribute(self):
        target = ('status', 'nonce', 'gpg_pub_key', 'address_host', 'address_port', 'sig', 'data')
        self.assertEqual(self.x.column_names_tuple, target)
        with self.assertRaises(AttributeError):
            self.x.column_names_tuple = 'hello'

    def test_data_row_name_class_attribute(self):
        target = 'ContactRequestTableRow'
        self.assertEqual(self.x.data_row_name, target)
        with self.assertRaises(AttributeError):
            self.x.data_row_name = 'hello'

    def test_create_table_string_attribute(self):
        target = 'create table if not exists ContactRequests (id integer primary key autoincrement, status TEXT, nonce TEXT, gpg_pub_key TEXT, address_host TEXT, address_port TEXT, sig TEXT, data TEXT);'

        result = self.x.create_table_string
        self.assertEqual(result, target)

    def test_create_table_method(self):
        self.x.create_table()
        connection = sqlite3.connect(self.db_file_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA table_info({})'.format(self.x.table_name))
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        self.assertTrue(len(result) > 0)

    def test_insert_data_row(self):
        self.x.create_table()
        data_row = (1, 2, 3, 4, 5, 6, 7)
        self.x.insert_data_row(data_row)
        connection = sqlite3.connect(self.db_file_path)
        cursor = connection.cursor()
        cursor.execute('select * from {};'.format(self.x.table_name))
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        self.assertTrue(len(result) > 0)

    def test_build_named_tuple_method_builds_row_tuple(self):
        data_row = (1, 2, 3, 4, 5, 6, 7)
        result = self.x.build_named_tuple(data_row)
        self.assertEqual(self.x.data_row_name, type(result).__name__)
        try:
            for item in self.x.column_names_tuple:
                result.__getattribute__(item)
        except:
            self.assertTrue(False)

    def test_create_empty_named_tuple(self):
        result = self.x.create_empty_named_tuple()
        self.assertEqual(self.x.column_names_tuple, result._fields)

    def test_init_method_calls_create_table(self):
        connection = sqlite3.connect(self.db_file_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA table_info({})'.format(self.x.table_name))
        result = cursor.fetchall()
        connection.commit()
        connection.close()
        self.assertTrue(len(result) > 0)

    def test_build_input_from_payload_method(self):
        # dict_keys(['contact_req_dict', 'desc', 'nonce', 'data_dict'])
        mock_contact_req_dict = dict(sig='sig', data='data')

        mock_data_dict = {'address_host': 'addr_host',
                          'address_port':'addr_port',
                          'gpg_pub_key': 'gpg_pub_key',
                          'nonce': 'nonce'}
        mock_input = dict(contact_req_dict=mock_contact_req_dict, data_dict=mock_data_dict)
        target = ('unread',
                  mock_input['data_dict']['nonce'],
                  mock_input['data_dict']['gpg_pub_key'],
                  mock_input['data_dict']['address_host'],
                  mock_input['data_dict']['address_port'],
                  mock_input['contact_req_dict']['sig'],
                  mock_input['contact_req_dict']['data']
                  )
        result = self.x.build_input_from_payload(mock_input)
        try:
            for item in self.x.column_names_tuple:
                result.__getattribute__(item)
        except:
            self.assertTrue(False)
        self.assertEqual(result, target)

    def test_handle_new_payload(self):
        payload = dict()
        val = (1,2,3)
        target_1 = self.x.build_input_from_payload = MagicMock(return_value=val)
        target_2 = self.x.insert_data_row = MagicMock()
        self.x.handle_new_payload(payload)
        target_1.assert_called_with(payload)
        target_2.assert_called_with(target_1.return_value)

    def test_get_last_record_returns_last_record(self):
        data_row = ('1', '2', '3', '4', '5', '6', '7')
        self.x.insert_data_row(data_row)
        result = self.x.fetch_last_record()
        self.assertEqual(result, data_row)

    def test_fetch_all_address_and_nonce_fetch(self):
        data_row = ('1', '2', '3', '4', '5', '6', '7')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_all_address_and_nonce()
        target = (named.address_host, named.nonce)
        self.assertIn(target, result)

    def test_fetch_all_address_and_nonce_with_status(self):
        data_row = ('1', '2', '3', '4', '5', '6', '7')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_all_address_and_nonce_with_status()
        target = (named.address_host, named.nonce, named.status)
        self.assertIn(target, result)

    def test_fetch_one_by_nonce(self):
        data_row = ('1', '2', '3', '4', '5', '6', '7')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_one_by_nonce('2')
        self.assertEqual(data_row, result)

    def test_delete_record_where(self):
        data_row = ('1', '2', '3', '4', '5', '6', '7')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        self.x.delete_record_where_x_equals_y('nonce', named.nonce)
        result = self.x.fetch_all_address_and_nonce()
        self.assertEqual(len(result), 0)

    def test_fetch_gpg_pub_key_by_nonce(self):
        data_row = ('1', '2', '3', '4', '5', '6', '7')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_gpg_pub_key_by_nonce('2')
        self.assertEqual(result, '3')

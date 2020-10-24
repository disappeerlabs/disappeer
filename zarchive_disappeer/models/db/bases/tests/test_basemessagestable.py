"""
test_basemessagestable.py

Test suite for module BaseMessagesTable, superclass to hold code common to both sent and received messages tables.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.models.db.bases import basemessagestable
from disappeer.models.db.bases import abstractdbtable
from disappeer.models.db import dbexecutor
import os
import hashlib
import random
import sys


class TestImports(unittest.TestCase):

    def test_abstracttable(self):
        self.assertEqual(abstractdbtable, basemessagestable.abstractdbtable)

    def test_hashlib(self):
        self.assertEqual(hashlib, basemessagestable.hashlib)

    def test_random(self):
        self.assertEqual(random, basemessagestable.random)

    def test_sys(self):
        self.assertEqual(sys, basemessagestable.sys)


db_file_path = 'models/db/tests/testdb.sqlite'


class MockMessagesTable(basemessagestable.BaseMessagesTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'MockMessages'

    @property
    def data_row_name(self):
        return 'MockMessagesTableRow'


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.hello = 'hello'
        self.example_payload_valid = dict(nonce='nonce_string', ciphertext='ciphertext_string')
        self.x = MockMessagesTable(db_file_path)

    def tearDown(self):
        if os.path.isfile(db_file_path):
            os.remove(db_file_path)

    def test_instance_base(self):
        self.assertIsInstance(self.x, basemessagestable.BaseMessagesTable)

    def test_instance_executor(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_instance_abstract_table(self):
        self.assertIsInstance(self.x, abstractdbtable.AbstractDBTable)

    def test_db_executor_database_path_attribute_set(self):
        self.assertEqual(self.x.database, db_file_path)

    def test_table_column_names_tuple_class_attribute(self):
        target = ('nonce', 'ciphertext', 'status')
        self.assertEqual(self.x.column_names_tuple, target)
        with self.assertRaises(AttributeError):
            self.x.column_names_tuple = 'hello'

    def test_build_input_from_payload(self):
        nonce_val = 'random_nonce'
        sub = self.x.random_hash = MagicMock(return_value=nonce_val)
        target_data_row = (sub.return_value,
                           self.example_payload_valid['ciphertext'],
                           'unread')
        target = self.x.build_named_tuple(target_data_row)
        result = self.x.build_input_from_payload(self.example_payload_valid)
        self.assertEqual(result, target)

    def test_handle_new_payload_calls_build_and_insert(self):
        payload = dict()
        val = MagicMock()
        target_1 = self.x.build_input_from_payload = MagicMock(return_value=val)
        target_2 = self.x.insert_data_row = MagicMock()
        self.x.handle_new_payload(payload)
        target_1.assert_called_with(payload)
        target_2.assert_called_with(target_1.return_value)

    def test_fetch_all_nonces(self):
        nonce_val = 'random_nonce'
        sub = self.x.random_hash = MagicMock(return_value=nonce_val)
        payload = dict(nonce='nonce_string', ciphertext='ciphertext_string')
        payload_1 = dict(nonce='nonce_string_1', ciphertext='ciphertext_string')
        self.x.handle_new_payload(payload)
        self.x.handle_new_payload(payload_1)
        result = self.x.fetch_all_nonces()
        self.assertEqual(result[0][0], nonce_val)
        self.assertEqual(result[1][0], nonce_val)

    def test_fetch_all_nonces_with_status(self):
        payload = dict(nonce='nonce_string', ciphertext='ciphertext_string')
        payload_1 = dict(nonce='nonce_string_1', ciphertext='ciphertext_string')
        self.x.handle_new_payload(payload)
        self.x.handle_new_payload(payload_1)
        result = self.x.fetch_all_nonces_with_status()
        target = 'unread'
        self.assertEqual(result[0][1], target)
        self.assertEqual(result[1][1], target)

    def test_fetch_record_by_nonce(self):
        nonce_val = 'random_nonce'
        sub = self.x.random_hash = MagicMock(return_value=nonce_val)
        payload = dict(nonce=nonce_val, ciphertext='ciphertext_string')
        self.x.handle_new_payload(payload)
        result = self.x.fetch_named_tuple_by_nonce(nonce_val)
        self.assertEqual(nonce_val, result[0])

    def test_delete_record_by_nonce(self):
        target = self.x.delete_record_where_x_equals_y = MagicMock()
        nonce_string = 'nonce_string'
        self.x.delete_record_by_nonce(nonce_string)
        target.assert_called_with('nonce', nonce_string)

    def test_update_record_status_to_read_by_nonce(self):
        nonce_val = 'random_nonce'
        sub = self.x.random_hash = MagicMock(return_value=nonce_val)
        nonce_1 = 'nonce_string_1'
        payload = dict(nonce=nonce_1, ciphertext='ciphertext_string')
        self.x.handle_new_payload(payload)
        target_val = 'read'
        self.x.update_record_status_to_read(sub.return_value)
        result = self.x.fetch_named_tuple_by_nonce(sub.return_value)
        self.assertEqual(result.status, target_val)

    def test_hash_message_method_returns_hash(self):
        check = 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
        result = self.x.hash_message(self.hello)
        self.assertEqual(result, check)

    @patch('disappeer.models.db.bases.basemessagestable.random')
    def test_random_hash_method_calls_randint(self, patched):
        check = 'b1d5781111d84f7b3fe45a0852e59758cd7a87e5'
        val = str(10)
        patched.randint.return_value = val
        result = self.x.random_hash()
        patched.randint.assert_called_with(0, sys.maxsize)
        self.assertEqual(result, check)
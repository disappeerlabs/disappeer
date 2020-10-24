"""
test_dbpeercontactstable.py

Test suite for the DBPeerContactsTable class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.models.db import dbpeercontactstable
from disappeer.models.db.bases import abstractdbtable
from disappeer.models.db import dbexecutor
import os


class TestImports(unittest.TestCase):

    def test_abstracttable(self):
        self.assertEqual(abstractdbtable, dbpeercontactstable.abstractdbtable)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.example_payload_valid = dict(gpg_pub_key='gpg_pub_key_string',
                                          gpg_uid='gpg_uid_string',
                                          gpg_fingerprint='gpg_fingerprint_val',
                                          address_host='address string',
                                          address_port='port_string')
        self.db_file_path = 'models/db/tests/testdb.sqlite'
        self.x = dbpeercontactstable.DBPPeerContactsTable(self.db_file_path)

    def tearDown(self):
        if os.path.isfile(self.db_file_path):
            os.remove(self.db_file_path)

    def test_instance(self):
        self.assertIsInstance(self.x, dbpeercontactstable.DBPPeerContactsTable)

    def test_instance_executor(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_instance_abstract_table(self):
        self.assertIsInstance(self.x, abstractdbtable.AbstractDBTable)

    def test_db_executor_database_path_attribute_set(self):
        self.assertEqual(self.x.database, self.db_file_path)

    def test_table_name_class_attribute(self):
        target = 'PeerContacts'
        self.assertEqual(self.x.table_name, target)
        with self.assertRaises(AttributeError):
            self.x.table_name = 'hello'

    def test_data_row_name_class_attribute(self):
        target = 'PeerContactsTableRow'
        self.assertEqual(self.x.data_row_name, target)
        with self.assertRaises(AttributeError):
            self.x.data_row_name = 'hello'

    def test_table_column_names_tuple_class_attribute(self):
        target = ('gpg_pub_key', 'gpg_uid', 'gpg_fingerprint', 'address_host', 'address_port', 'status')

        self.assertEqual(self.x.column_names_tuple, target)
        with self.assertRaises(AttributeError):
            self.x.column_names_tuple = 'hello'

    def test_build_input_from_payload(self):
        target_data_row = (self.example_payload_valid['gpg_pub_key'],
                           self.example_payload_valid['gpg_uid'],
                           self.example_payload_valid['gpg_fingerprint'],
                           self.example_payload_valid['address_host'],
                           self.example_payload_valid['address_port'],
                           'unread')
        target = self.x.build_named_tuple(target_data_row)
        result = self.x.build_input_from_payload(self.example_payload_valid)
        self.assertEqual(result, target)

    def test_handle_new_payload_calls_build_and_insert(self):
        payload = dict()
        val = MagicMock()
        sub = self.x.fetch_all_by_fingerprint = MagicMock()
        target_1 = self.x.build_input_from_payload = MagicMock(return_value=val)
        target_2 = self.x.insert_data_row = MagicMock()
        self.x.handle_new_payload(payload)
        target_1.assert_called_with(payload)
        target_2.assert_called_with(target_1.return_value)

    def test_handle_new_payload_deletes_old_fingerprint_rows_with_new_fingerprint_payload(self):
        self.x.handle_new_payload(self.example_payload_valid)
        first = self.x.fetch_all_by_fingerprint(self.example_payload_valid['gpg_fingerprint'])
        self.assertEqual(1, len(first))
        self.x.handle_new_payload(self.example_payload_valid)
        second = self.x.fetch_all_by_fingerprint(self.example_payload_valid['gpg_fingerprint'])
        self.assertEqual(1, len(second))

    def test_fetch_all_uid_and_fingerprint(self):
        data_row = ('1', '2', '3', '4', '5', '6')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_all_uids_and_fingerprints()
        target = (named.gpg_uid, named.gpg_fingerprint)
        self.assertIn(target, result)

    def test_fetch_all_by_fingerprint(self):
        data_row = ('1', '2', '3', '4', '5', '6')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_all_by_fingerprint(named.gpg_fingerprint)
        self.assertEqual(1, len(result))

    def test_delete_by_id(self):
        data_row = ('1', '2', '3', '4', '5', '6')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        inter = self.x.fetch_all_by_fingerprint(named.gpg_fingerprint)
        id_target = inter[0][0]
        delete_result = self.x.delete_record_where_x_equals_y('id', id_target)
        final = self.x.fetch_all_by_fingerprint(named.gpg_fingerprint)
        self.assertEqual(0, len(final))

    def test_fetch_named_tuple_row_by_fingerprint_fetches_and_returns(self):
        data_row = ('1', '2', '3', '4', '5', '6')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_named_tuple_row_by_fingerprint(named.gpg_fingerprint)
        self.assertEqual(result, data_row)
        self.assertEqual(named.gpg_fingerprint, result.gpg_fingerprint)

    def test_fetch_named_tuple_row_by_fingerprint_with_failed_fingerprint(self):
        data_row = ('1', '2', '3', '4', '5', '6')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_named_tuple_row_by_fingerprint('xxxx')
        self.assertEqual(len(result), 0)

    def test_update_record_status_to_read_by_nonce(self):
        data_row = ('1', '2', '3', '4', '5', '6')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        target_val = 'read'
        self.x.update_record_status_to_read_by_fingerprint(named.gpg_fingerprint)
        result = self.x.fetch_named_tuple_row_by_fingerprint(named.gpg_fingerprint)
        self.assertEqual(result.status, target_val)

    def test_fetch_all_uid_and_fingerprint_and_status(self):
        data_row = ('1', '2', '3', '4', '5', '6')
        named = self.x.build_named_tuple(data_row)
        self.x.insert_data_row(named)
        result = self.x.fetch_all_uids_and_fingerprints_and_status()
        target = (named.gpg_uid, named.gpg_fingerprint, named.status)
        self.assertIn(target, result)

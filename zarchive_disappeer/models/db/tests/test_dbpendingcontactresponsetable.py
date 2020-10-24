"""
test_pendingcontactresponsetable.py

Test suite for DBPendingContactResponseTable class object and module.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.models.db import dbpendingcontactresponsetable
from disappeer.models.db.bases import abstractdbtable
from disappeer.models.db import dbexecutor
import os


class TestImports(unittest.TestCase):

    def test_abstractdbtable(self):
        self.assertEqual(abstractdbtable, dbpendingcontactresponsetable.abstractdbtable)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.example_payload_NOT_valid = {'nonce': '6c4b060de315f72ab205deb19145132772fb5d44', 'result': {'desc': 'ACK', 'nonce': '6c4b060de315f72ab205deb19145132772fb5d44', 'gpg_pub_key': '-----BEGIN PGP PUBLIC KEY BLOCK-----\nVersion: GnuPG v1\n\n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\n=IF8v\n-----END PGP PUBLIC KEY BLOCK-----\n'}, 'nonce_valid': False, 'desc': 'New_Contact_Req_Client_Res'}
        self.example_payload_valid = {'nonce': '6c4b060de315f72ab205deb19145132772fb5d44',
                                      'result': {'desc': 'ACK',
                                                 'nonce': '6c4b060de315f72ab205deb19145132772fb5d44',
                                                 'gpg_pub_key': '-----BEGIN PGP PUBLIC KEY BLOCK-----\nVersion: GnuPG v1\n\n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\n=IF8v\n-----END PGP PUBLIC KEY BLOCK-----\n'},
                                      'nonce_valid': True,
                                      'host': 'host_string',
                                      'fingerprint': 'fingerprint_string',
                                      'desc': 'New_Contact_Req_Client_Res'}
        self.db_file_path = 'models/db/tests/testdb.sqlite'
        self.x = dbpendingcontactresponsetable.DBPendingContactResponseTable(self.db_file_path)

    def tearDown(self):
        if os.path.isfile(self.db_file_path):
            os.remove(self.db_file_path)

    def test_instance(self):
        self.assertIsInstance(self.x, dbpendingcontactresponsetable.DBPendingContactResponseTable)

    def test_instance_executor(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_instance_abstract_table(self):
        self.assertIsInstance(self.x, abstractdbtable.AbstractDBTable)

    def test_db_executor_database_path_attribute_set(self):
        self.assertEqual(self.x.database, self.db_file_path)

    def test_table_name_class_attribute(self):
        target = 'PendingContactResponses'
        self.assertEqual(self.x.table_name, target)
        with self.assertRaises(AttributeError):
            self.x.table_name = 'hello'

    def test_table_column_names_tuple_class_attribute(self):
        target = ('status', 'nonce', 'gpg_pub_key', 'gpg_fingerprint', 'host')
        self.assertEqual(self.x.column_names_tuple, target)
        with self.assertRaises(AttributeError):
            self.x.column_names_tuple = 'hello'

    def test_data_row_name_class_attribute(self):
        target = 'PendingContactResponseTableRow'
        self.assertEqual(self.x.data_row_name, target)
        with self.assertRaises(AttributeError):
            self.x.data_row_name = 'hello'

    def test_build_input_from_payload(self):
        status = 'new'
        nonce = self.example_payload_valid['result']['nonce']
        gpg_key = self.example_payload_valid['result']['gpg_pub_key']
        fingerprint = self.example_payload_valid['fingerprint']
        host = self.example_payload_valid['host']
        target_data_row = (status, nonce, gpg_key, fingerprint, host)
        target = self.x.build_named_tuple(target_data_row)
        result = self.x.build_input_from_payload(self.example_payload_valid)
        self.assertEqual(result, target)

    def test_handle_new_payload(self):
        payload = dict()
        val = (1,2,3)
        target_1 = self.x.build_input_from_payload = MagicMock(return_value=val)
        target_2 = self.x.insert_data_row = MagicMock()
        self.x.handle_new_payload(payload)
        target_1.assert_called_with(payload)
        target_2.assert_called_with(target_1.return_value)

    def test_fetch_all_nonces_returns_list_of_nonces(self):
        self.x.handle_new_payload(self.example_payload_valid)
        result = self.x.fetch_all_nonces()
        target = [self.example_payload_valid['nonce']]
        self.assertEqual(result, target)

    def test_fetch_pubkey_by_nonce_returns_pubkey(self):
        self.x.handle_new_payload(self.example_payload_valid)
        valid_nonce = self.example_payload_valid['result']['nonce']
        target_key = self.example_payload_valid['result']['gpg_pub_key']
        result = self.x.fetch_gpg_pub_key_by_nonce(valid_nonce)
        self.assertEqual(result, target_key)

    def test_fetch_all_hosts_and_fingerprints(self):
        self.x.handle_new_payload(self.example_payload_valid)
        result = self.x.fetch_all_hosts_and_fingerprints()
        target = (self.example_payload_valid['host'], self.example_payload_valid['fingerprint'])
        self.assertIn(target, result)

    def test_fetch_pubkey_by_fingerprint_returns_pubkey(self):
        self.x.handle_new_payload(self.example_payload_valid)
        valid_fingerprint = self.example_payload_valid['fingerprint']
        target_key = self.example_payload_valid['result']['gpg_pub_key']
        result = self.x.fetch_gpg_pub_key_by_fingerprint(valid_fingerprint)
        self.assertEqual(result, target_key)




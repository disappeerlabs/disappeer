"""
test_contactrequestfactory.py

Test suite for the ContactRequestFactory module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net.contact import contactrequestfactory
import hashlib
import random
import sys
from disappeer import settings
import json
from disappeer.gpg.agents import signer


class TestImports(unittest.TestCase):

    def test_hashlib(self):
        self.assertEqual(hashlib, contactrequestfactory.hashlib)

    def test_random(self):
        self.assertEqual(random, contactrequestfactory.random)

    def test_sys(self):
        self.assertEqual(sys, contactrequestfactory.sys)

    def test_settings(self):
        self.assertEqual(settings, contactrequestfactory.settings)

    def test_json(self):
        self.assertEqual(json, contactrequestfactory.json)

    def test_gpgsigner(self):
        self.assertEqual(signer, contactrequestfactory.signer)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.hello = 'hello'
        self.target_file = settings.gpg_host_pubkey
        self.address_host = '.onion'
        self.address_port = '6666'
        self.key_home_dir = 'tests/data/keys'
        self.passphrase = 'passphrase'
        self.x = contactrequestfactory.ContactRequestFactory(self.address_host, self.key_home_dir, self.passphrase)

    def test_instance(self):
        self.assertIsInstance(self.x, contactrequestfactory.ContactRequestFactory)

    def test_response_server_port_attribute(self):
        self.assertEqual(settings.port_contact_response_server, self.x.contact_response_port)

    def test_response_server_host_address_attribute_set(self):
        self.assertEqual(self.address_host, self.x.contact_response_host)

    def test_key_home_dir_attribute_set(self):
        self.assertEqual(self.x.key_home_dir, self.key_home_dir)

    def test_gpg_signer_attribute_set(self):
        self.assertIsInstance(self.x.gpgsigner, signer.Signer)

    def test_passphrase_attr_set(self):
        self.assertEqual(self.x.passphrase, self.passphrase)

    def test_hash_message_method_returns_hash(self):
        check = 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
        result = self.x.hash_message(self.hello)
        self.assertEqual(result, check)

    @patch('disappeer.net.contact.contactrequestfactory.random')
    def test_random_hash_method_calls_randint(self, patched):
        check = 'b1d5781111d84f7b3fe45a0852e59758cd7a87e5'
        val = str(10)
        patched.randint.return_value = val
        result = self.x.random_hash()
        patched.randint.assert_called_with(0, sys.maxsize)
        self.assertEqual(result, check)

    def test_read_file_method_returns_file_contents(self):
        with open(self.target_file, 'r') as f:
            check = f.read()
        result = self.x.read_file(self.target_file)
        self.assertEqual(result, check)

    def test_construct_data_dict_method(self):
        sub = self.x.random_hash = MagicMock(return_value='12345')

        data_dict = dict(gpg_pub_key=self.x.read_file(settings.gpg_host_pubkey),
                         address_host=self.x.contact_response_host,
                         address_port=self.x.contact_response_port,
                         nonce=self.x.random_hash())
        result = self.x.construct_data_dict()
        self.assertEqual(result, data_dict)

    def test_encode_data_dict(self):
        val_dict = dict(desc='hello')
        sub = self.x.construct_data_dict = MagicMock(return_value=val_dict)
        result = self.x.encode_data_dict()
        check = json.dumps(val_dict)
        self.assertEqual(result, check)

    def test_sign_data_method(self):
        val_return = 'xxxxx'
        val_dict = json.dumps(dict(desc='hello'))
        target = self.x.gpgsigner = MagicMock(return_value=val_return)
        result = self.x.sign_encoded_data(val_dict)
        target.execute.assert_called_with(val_dict, None, self.x.passphrase, detach=True)
        self.assertEqual(result, target.execute.return_value)

    def test_build_method_calls_encode_data_dict(self):
        sub = self.x.sign_encoded_data = MagicMock()
        target = self.x.encode_data_dict = MagicMock()
        self.x.build()
        target.assert_called_with()

    def test_build_method_calls_sign_method_with_encoded_data_dict(self):
        encoded = json.dumps(dict(desc='hell0'))
        sub = self.x.encode_data_dict = MagicMock(return_value=encoded)
        target = self.x.sign_encoded_data = MagicMock()
        self.x.build()
        target.assert_called_with(sub.return_value)

    def test_build_method_returns_proper_dict(self):
        class MockGoodResult:
            data = 'hello'
            stderr = 'Mock Error'
        sub1_return = 'xxx'
        sub2_return = MockGoodResult()
        mocked_data = self.x.encode_data_dict = MagicMock(return_value=sub1_return)
        mocked_dig = self.x.sign_encoded_data = MagicMock(return_value=sub2_return)
        result = self.x.build()
        for item in ['sig', 'data']:
            self.assertTrue(item, result.keys())

    def test_build_method_returns_stderr_on_sign_err(self):
        class MockBadResult:
            data = b''
            stderr = 'Mock Error'
        mocked_result = MockBadResult()
        sub = self.x.sign_encoded_data = MagicMock(return_value=mocked_result)
        result = self.x.build()
        self.assertNotIsInstance(result, dict)

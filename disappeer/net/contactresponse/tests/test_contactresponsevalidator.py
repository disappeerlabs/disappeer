"""
test_contactresponsevalidator.py

Test suite for ContactResponseValidator class object and module:
Validator must:
    - take incoming payload from SSLContactResponseRequestHandler
    - decrypt the ciphertext, resulting in {sig: 'xxx', data: 'xxx'} object
        - this requires a decrypter and passphrase
    - decode that object
        - this requires json decoder
    - check the sig against the data
        - this requires a gpg detached sig verifier
    - json decode the data object
        - this requires json decoder
    - check the nonce in the data object against known outstanding nonces
        - this requires a db call to the pending requests table, to get list of current pending request nonces

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch, call
from disappeer.net.contactresponse import contactresponsevalidator
from disappeer.gpg.agents import encrypter
from disappeer.gpg.agents import decrypter
from disappeer.gpg.helpers import tempdetachedverifier
from disappeer.gpg.agents import keyring
from disappeer import settings
from disappeer.models.db import dbpendingcontactresponsetable
import json


class TestImports(unittest.TestCase):

    def test_decrypter(self):
        self.assertEqual(decrypter, contactresponsevalidator.decrypter)

    def test_dbpendingcontactresponsetable(self):
        self.assertEqual(dbpendingcontactresponsetable, contactresponsevalidator.dbpendingcontactresponsetable)

    def test_settings(self):
        self.assertEqual(settings, contactresponsevalidator.settings)

    def test_json(self):
        self.assertEqual(json, contactresponsevalidator.json)

    def test_tempdetachedverifier(self):
        self.assertEqual(tempdetachedverifier, contactresponsevalidator.tempdetachedverifier)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.message = "Hello world"
        self.key_dir = 'tests/data/keys'
        self.key_ring = keyring.KeyRing(self.key_dir)
        self.encrypt_agent = encrypter.Encrypter(self.key_dir)
        self.encrypted_msg = str(self.encrypt_agent.execute(self.message, '55A45A99FE45E540'))
        self.mock_valid_payload = dict(ciphertext=self.encrypted_msg, request_nonce='req_nonce_string', response_nonce='resp_nonce_string' )
        self.mock_database_table = MagicMock()
        self.passphrase = 'passphrase'
        self.x = contactresponsevalidator.ContactResponseValidator(self.mock_valid_payload, self.key_dir, self.mock_database_table, self.passphrase)

    def test_instance(self):
        self.assertIsInstance(self.x, contactresponsevalidator.ContactResponseValidator)

    def test_target_payload_attribute_set(self):
        self.assertEqual(self.x.payload, self.mock_valid_payload)

    def test_key_dir_attribute_set(self):
        self.assertEqual(self.x.key_dir, self.key_dir)

    # def test_db_pending_contacts_attribute_instance_set_with_maindb(self):
    #     self.assertIsInstance(self.x.db_pending_contacts, dbpendingcontactresponsetable.DBPendingContactResponseTable)
    #     self.assertEqual(settings.main_database, self.x.db_pending_contacts.database)

    def test_db_pending_contacts_attribute_instance_set_from_arg(self):
        self.assertEqual(self.x.db_pending_contacts, self.mock_database_table)

    def test_passphrase_attr_set(self):
        self.assertEqual(self.x.passphrase, self.passphrase)

    def test_error_attribute_set_none(self):
        self.assertIsNone(self.x.error)

    def test_valid_attribute_set_none(self):
        self.assertIsNone(self.x.valid)

    def test_data_dict_attribute_set_none(self):
        self.assertIsNone(self.x.data_dict)

    def test_set_error_method_sets_error_and_valid(self):
        msg = 'Error Message'
        self.x.set_error(msg)
        self.assertEqual(self.x.error, msg)
        self.assertIs(self.x.valid, False)

    def test_check_payload_method_checks_payload_keys_sets_attributes(self):
        result = self.x.check_payload_keys(self.x.payload)
        self.assertIs(result, True)

    def test_check_payload_method_returns_false_on_invalid_dict(self):
        bad_dict = dict()
        result = self.x.check_payload_keys(bad_dict)
        self.assertIs(result, False)

    def test_check_payload_method_returns_false_on_bad_data(self):
        bad_data = 'xxx'
        result = self.x.check_payload_keys(bad_data)
        self.assertIs(result, False)

    def test_request_nonce_is_valid_returns_true_on_valid_input(self):
        nonce_list = ['aaa', 'bbb']
        sub = self.x.db_pending_contacts.fetch_all_nonces = MagicMock(return_value=nonce_list)
        result = self.x.is_request_nonce_valid(nonce_list[0])
        self.assertIs(result, True)

    def test_request_nonce_is_valid_returns_false_on_not_valid(self):
        nonce_list = ['aaa', 'bbb']
        sub = self.x.db_pending_contacts.fetch_all_nonces = MagicMock(return_value=nonce_list)
        result = self.x.is_request_nonce_valid('xxx')
        self.assertIs(result, False)

    @patch('net.contactresponse.contactresponsevalidator.decrypter.Decrypter')
    def test_decrypt_ciphertext_method_calls_decrypter_with_key_dir(self, target):
        mock_ciphertext = 'xxx'
        self.x.decrypt_ciphertext(mock_ciphertext)
        target.assert_called_with(self.x.key_dir)

    @patch.object(contactresponsevalidator.decrypter.Decrypter, 'execute')
    def test_decrypt_ciphertext_calls_execute_with_args(self, target):
        self.x.decrypt_ciphertext(self.encrypted_msg)
        target.assert_called_with(self.encrypted_msg, self.x.passphrase)

    @patch.object(contactresponsevalidator.decrypter.Decrypter, 'execute')
    def test_decrypt_ciphertext_sets_error_returns_false_if_bad_response(self, sub):
        class MockBadResult:
            ok = False
            status = 'status_message'
        sub.return_value = MockBadResult()
        target = self.x.set_error = MagicMock()
        result = self.x.decrypt_ciphertext(self.encrypted_msg)
        target.assert_called_with(MockBadResult.status)
        self.assertIs(result, False)

    @patch.object(contactresponsevalidator.decrypter.Decrypter, 'execute')
    def test_decrypt_ciphertext_returns_plaintext_on_valid_result(self, sub):
        class MockBadResult:
            ok = True
            status = 'status_message'
        sub.return_value = MockBadResult()
        result = self.x.decrypt_ciphertext(self.encrypted_msg)
        self.assertEqual(result, str(sub.return_value))

    def test_decode_json_decodes_returns_valid_json(self):
        msg_dict = dict(msg='hello world')
        encoded = json.dumps(msg_dict)
        result = self.x.decode_json_string(encoded)
        self.assertEqual(result, msg_dict)

    def test_decode_json_returns_false_on_invalid(self):
        msg_dict = dict(msg='hello world')
        result = self.x.decode_json_string(msg_dict)
        self.assertIs(result, False)

    def test_check_sig_dict_keys_returns_true_on_valid(self):
        sig_dict = dict(sig='sig', data='data')
        result = self.x.check_sig_dict_keys(sig_dict)
        self.assertIs(result, True)

    def test_check_sig_dict_keys_returns_false_on_invalid(self):
        sig_dict = dict(xxx='sig', data='data')
        result = self.x.check_sig_dict_keys(sig_dict)
        self.assertIs(result, False)

    def test_check_sig_dict_keys_returns_false_on_bad_input(self):
        bad = 123
        result = self.x.check_sig_dict_keys(bad)
        self.assertIs(result, False)

    def test_fetch_gpg_pub_key_by_nonce_calls_target_with_arg_returns_val(self):
        nonce = 'xxxx'
        val = 'aaaa'
        target = self.x.db_pending_contacts.fetch_gpg_pub_key_by_nonce = MagicMock(return_value=val)
        result = self.x.fetch_gpg_pub_key_by_nonce(nonce)
        target.assert_called_with(nonce)
        self.assertEqual(result, val)

    @patch('net.contactresponse.contactresponsevalidator.tempdetachedverifier.TempDetachedVerifier')
    def test_verify_sig_dict_verifies_sig_dict_with_temp_detached_verifier(self, target):
        key = 'xxx'
        sig_dict = dict()
        self.x.verify_sig_dict_with_key(key, sig_dict)
        target.assert_called_with(key, sig_dict)

    @patch('net.contactresponse.contactresponsevalidator.tempdetachedverifier.TempDetachedVerifier')
    def test_verify_sig_dict_returns_false_if_validator_not_valid(self, sub):
        class MockResult:
            valid = False
        sub.return_value = MockResult()
        key = 'xxx'
        sig_dict = dict()
        result = self.x.verify_sig_dict_with_key(key, sig_dict)
        self.assertIs(result, False)

    @patch('net.contactresponse.contactresponsevalidator.tempdetachedverifier.TempDetachedVerifier')
    def test_verify_sig_dict_returns_true_if_validator_valid(self, sub):
        class MockResult:
            valid = True
        sub.return_value = MockResult()
        key = 'xxx'
        sig_dict = dict()
        result = self.x.verify_sig_dict_with_key(key, sig_dict)
        self.assertTrue(result)

    def test_check_sig_dict_data_dict_returns_true_with_valid_input(self):
        target_keys = ['address_host',
                       'address_port',
                       'response_nonce',
                       'request_nonce']
        target_vals = [1,2,3,4]
        input_dict = dict(zip(target_keys, target_vals))
        result = self.x.check_sig_dict_data_dict_keys(input_dict)
        self.assertIs(result, True)

    def test_check_sig_dict_data_dict_returns_false_with_invalid_input(self):
        target_keys = ['xxxx',
                       'address_port',
                       'response_nonce',
                       'request_nonce']
        target_vals = [1,2,3,4]
        input_dict = dict(zip(target_keys, target_vals))
        result = self.x.check_sig_dict_data_dict_keys(input_dict)
        self.assertIs(result, False)

    def test_check_sig_dict_data_dict_returns_false_with_bad_input(self):
        result = self.x.check_sig_dict_data_dict_keys(123)
        self.assertIs(result, False)

    def test_validate_calls_check_payload_with_payload(self):
        target = self.x.check_payload_keys = MagicMock()
        self.x.validate()
        target.assert_called_with(self.x.payload)

    def test_validate_sets_error_returns_false_with_false_payload(self):
        val = False
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        target = self.x.set_error = MagicMock()
        result = self.x.validate()
        self.assertIs(result, False)
        self.assertTrue(target.called)

    def test_validate_calls_is_nonce_valid_with_request_nonce(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        target = self.x.is_request_nonce_valid = MagicMock()
        self.x.validate()
        target.assert_called_with(self.x.payload['request_nonce'])

    def test_validate_sets_error_returns_false_with_false_nonce(self):
        sub = self.x.check_payload_keys = MagicMock(return_value=True)
        target = self.x.is_request_nonce_valid = MagicMock(return_value=False)
        result = self.x.validate()
        self.assertIsNotNone(self.x.error)
        self.assertIs(result, False)

    def test_validate_calls_decrypt_ciphertext_with_ciphertext(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        target = self.x.decrypt_ciphertext = MagicMock()
        self.x.validate()
        target.assert_called_with(self.x.payload['ciphertext'])

    def test_validate_returns_false_if_decrypt_ciphertext_returns_false(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        target = self.x.decrypt_ciphertext = MagicMock(return_value=False)
        result = self.x.validate()
        self.assertIs(result, False)

    def test_validate_calls_decode_json_with_decrypted_ciphertext(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        target = self.x.decode_json_string = MagicMock()
        self.x.validate()
        target.assert_called_with(sub2.return_value)

    def test_validate_returns_false_if_decode_json_with_decrypted_ciphertext_returns_false(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value=123)
        target = self.x.set_error = MagicMock()
        result = self.x.validate()
        self.assertIs(result, False)
        self.assertTrue(target.called)

    def test_validate_calls_check_sig_dict_keys_with_sig_dict(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value='aaa')
        target = self.x.check_sig_dict_keys = MagicMock(return_value=False)
        self.x.validate()
        target.assert_called_with(sub3.return_value)

    def test_validate_returns_false_if_check_sig_dict_keys_is_false(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value='aaa')
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=False)
        target = self.x.set_error = MagicMock()
        result = self.x.validate()
        self.assertIs(result, False)
        self.assertTrue(target.called)

    @patch('net.contactresponse.contactresponsevalidator.tempdetachedverifier.TempDetachedVerifier')
    def test_validate_calls_fetch_gpg_pub_key_with_nonce(self, verifier):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value=dict(data='xxx'))
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        target = self.x.fetch_gpg_pub_key_by_nonce = MagicMock()
        self.x.validate()
        target.assert_called_with(self.x.payload['request_nonce'])

    def test_validate_returns_false_if_fetch_gpg_pub_key_with_nonce_is_nonce(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value=dict(data='xxx'))
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value=None)
        target = self.x.set_error = MagicMock()
        result = self.x.validate()
        self.assertIs(result, False)
        self.assertTrue(target.called)

    def test_validate_calls_verify_sig_dict_with_args(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value=dict(data='xxx'))
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value='yyy')
        target = self.x.verify_sig_dict_with_key = MagicMock()
        self.x.validate()
        target.assert_called_with(sub5.return_value, sub3.return_value)

    def test_validate_returns_false_if_sig_verify_fails(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value='aaa')
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value='yyy')
        sub6 = self.x.verify_sig_dict_with_key = MagicMock(return_value=False)
        target = self.x.set_error = MagicMock()
        result = self.x.validate()
        self.assertIs(result, False)
        self.assertTrue(target.called)

    def test_validate_calls_decode_json_on_sig_dict_data(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        # sub3 = self.x.decode_json_string = MagicMock(return_value=dict(data='xxx'))
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value='yyy')
        sub6 = self.x.verify_sig_dict_with_key = MagicMock(return_value=True)
        target = self.x.decode_json_string = MagicMock()
        self.x.validate()
        self.assertTrue(target.called)

    def test_validate_returns_false_if_json_decode_false(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value='yyy')
        sub6 = self.x.verify_sig_dict_with_key = MagicMock(return_value=True)
        result = self.x.validate()
        self.assertIs(result, False)

    def test_validate_calls_check_sig_dict_data_dict_keys(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value=dict(data='xxx'))
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value='yyy')
        sub6 = self.x.verify_sig_dict_with_key = MagicMock(return_value=True)
        target = self.x.check_sig_dict_data_dict_keys = MagicMock()
        self.x.validate()
        self.assertTrue(target.called)

    def test_validate_returns_false_if_check_sig_dict_data_dict_keys_is_false(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value=dict(data='xxx'))
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value='yyy')
        sub6 = self.x.verify_sig_dict_with_key = MagicMock(return_value=True)
        sub7 = self.x.check_sig_dict_data_dict_keys = MagicMock(return_value=False)
        target = self.x.set_error = MagicMock()
        result = self.x.validate()
        self.assertIs(result, False)
        self.assertTrue(target.called)

    def test_validate_returns_true_sets_valid_if_all_true(self):
        val = True
        sub = self.x.check_payload_keys = MagicMock(return_value=val)
        sub1 = self.x.is_request_nonce_valid = MagicMock(return_value=val)
        sub2 = self.x.decrypt_ciphertext = MagicMock(return_value='xxxx')
        sub3 = self.x.decode_json_string = MagicMock(return_value=dict(data='xxx'))
        sub4 = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        sub5 = self.x.fetch_gpg_pub_key_by_nonce = MagicMock(return_value='yyy')
        sub6 = self.x.verify_sig_dict_with_key = MagicMock(return_value=True)
        sub7 = self.x.check_sig_dict_data_dict_keys = MagicMock(return_value=True)
        result = self.x.validate()
        self.assertIs(result, True)
        self.assertIs(self.x.valid, True)
        self.assertIsNotNone(self.x.data_dict)



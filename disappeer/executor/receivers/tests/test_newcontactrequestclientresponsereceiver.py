"""
test_newcontactrequestclientresponsereceiver.py

Test suite for NewContactRequestClientResponseReceiver class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.executor.receivers import newcontactrequestclientresponsereceiver
from disappeer.executor.receivers.newcontactrequestclientresponsereceiver import NewContactRequestClientResponseReceiver
from disappeer.gpg.helpers import gpgpubkeyvalidator
import copy


class TestImports(unittest.TestCase):

    def test_abstractreceiver(self):
        self.assertEqual(abstractreceiver, newcontactrequestclientresponsereceiver.abstractreceiver)

    def test_constants(self):
        self.assertEqual(constants, newcontactrequestclientresponsereceiver.constants)

    def test_gpgpubkeyvalidator(self):
        self.assertEqual(gpgpubkeyvalidator, newcontactrequestclientresponsereceiver.gpgpubkeyvalidator)


class TestNewContactRequestClientResponseReceiver(unittest.TestCase):

    def setUp(self):
        self.payload = dict()
        self.kwargs = {'database_facade': MagicMock(),
                       'requests_controller': MagicMock()}
        self.x = newcontactrequestclientresponsereceiver.NewContactRequestClientResponseReceiver(**self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, newcontactrequestclientresponsereceiver.NewContactRequestClientResponseReceiver)
        self.assertIsInstance(self.x, abstractreceiver.AbstractReceiver)

    def test_name_property_set(self):
        name = constants.command_list.New_Contact_Req_Client_Res + '_Receiver'
        self.assertEqual(self.x.name, name)

    def test_valid_kwargs_property_set(self):
        target = {'database_facade',
                  'requests_controller'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_valid_kwargs_class_attr_equals_instance_attr(self):
        self.assertEqual(self.x.valid_kwarg_keys, NewContactRequestClientResponseReceiver.kwarg_keys)

    def test_is_nonce_valid_returns_false_if_payload_nonce_false(self):
        payload = dict(nonce_valid=False)
        result = self.x.is_nonce_valid(payload)
        self.assertIs(result, False)

    def test_is_nonce_valid_returns_true_if_payload_nonce_true(self):
        payload = dict(nonce_valid=True)
        result = self.x.is_nonce_valid(payload)
        self.assertIs(result, True)

    def test_get_gpg_pubkey_from_payload_gets_pubkey(self):
        target_string = 'gpg_pubkey_string'
        result_dict = dict(gpg_pub_key=target_string)
        payload = dict(nonce_valid=True, result=result_dict)
        result = self.x.get_gpg_pubkey_from_payload(payload)
        self.assertEqual(result, target_string)

    @patch('executor.receivers.newcontactrequestclientresponsereceiver.gpgpubkeyvalidator.GPGPubKeyValidator')
    def test_validate_pubkey_calls_validator_with_arg_returns_validator(self, validator):
        class MockValidatorTrue:
            valid = True
            key_dict = dict(fingerprint='fingerprint_string')
        validator.return_value = MockValidatorTrue()
        pubkey_string = 'pubkey_string'
        result = self.x.validate_pubkey(pubkey_string)
        validator.assert_called_with(pubkey_string)
        self.assertEqual(result, validator.return_value)

    def test_execute_calls_is_nonce_valid_returns_false_if_nonce_valid_false(self):
        payload = dict(nonce_valid=False)
        result = self.x.execute(payload)
        self.assertIs(result, False)

    @patch('executor.receivers.newcontactrequestclientresponsereceiver.gpgpubkeyvalidator.GPGPubKeyValidator')
    def test_execute_calls_validate_pubkey_with_correct_args(self, validator):
        class MockValidatorTrue:
            valid = True
            key_dict = dict(fingerprint='fingerprint_string')

        validator.return_value = MockValidatorTrue()
        target_string = 'gpg_pubkey_string'
        result_dict = dict(gpg_pub_key=target_string)
        payload = dict(nonce_valid=True, result=result_dict)
        self.x.execute(payload)
        validator.assert_called_with(target_string)

    def test_executor_returns_false_if_validator_not_valid(self):
        class MockValidatorFalse:
            valid = False
            key_dict = dict(fingerprint='fingerprint_string')

        validator = MockValidatorFalse()
        sub = self.x.validate_pubkey = MagicMock(return_value=validator)
        target_string = 'gpg_pubkey_string'
        result_dict = dict(gpg_pub_key=target_string)
        payload = dict(nonce_valid=True, result=result_dict)
        result = self.x.execute(payload)
        self.assertIs(result, False)

    def test_executor_updates_payload_with_fingerprint_inserts_to_db_and_updates_view_if_validator_valid(self):
        class MockValidatorTrue:
            valid = True
            key_dict = dict(fingerprint='fingerprint_string')

        validator = MockValidatorTrue()
        sub = self.x.validate_pubkey = MagicMock(return_value=validator)
        gpg_string = 'gpg_pubkey_string'
        result_dict = dict(gpg_pub_key=gpg_string)
        payload = dict(nonce_valid=True, result=result_dict)
        result = self.x.execute(payload)

        target_arg = copy.deepcopy(payload)
        target_arg['fingerprint'] = validator.key_dict['fingerprint']
        self.x.database_facade.insert_pending_contact_response.assert_called_with(target_arg)
        self.x.requests_controller.update_sent_requests_treeview.assert_called_with()

    def test_executor_launches_user_alert_if_validator_valid(self):
        class MockValidatorTrue:
            valid = True
            key_dict = dict(fingerprint='fingerprint_string')

        validator = MockValidatorTrue()
        sub = self.x.validate_pubkey = MagicMock(return_value=validator)
        gpg_string = 'gpg_pubkey_string'
        result_dict = dict(gpg_pub_key=gpg_string)
        payload = dict(nonce_valid=True, result=result_dict)
        target = self.x.requests_controller.launch_user_alert = MagicMock()
        result = self.x.execute(payload)
        self.assertTrue(target.called)

"""
test_newcontactresponseclientresponsereceiver.py

Test suite for command pattern receiver module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.executor.receivers import newcontactresponseclientresponsereceiver
from disappeer.executor.receivers.newcontactresponseclientresponsereceiver import NewContactResponseClientResponseReceiver


class TestImports(unittest.TestCase):

    def test_abstractreceiver(self):
        self.assertEqual(abstractreceiver, newcontactresponseclientresponsereceiver.abstractreceiver)

    def test_constants(self):
        self.assertEqual(constants, newcontactresponseclientresponsereceiver.constants)


class TestNewContactResponseClientResponseReceiver(unittest.TestCase):

    def setUp(self):
        self.payload = dict()
        self.kwargs = {'database_facade': MagicMock(),
                       'gpg_datacontext': MagicMock(),
                       'requests_controller': MagicMock()}
        self.x = newcontactresponseclientresponsereceiver.NewContactResponseClientResponseReceiver(**self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, newcontactresponseclientresponsereceiver.NewContactResponseClientResponseReceiver)
        self.assertIsInstance(self.x, abstractreceiver.AbstractReceiver)

    def test_name_property_set(self):
        name = constants.command_list.New_Contact_Res_Client_Res + 'Receiver'
        self.assertEqual(self.x.name, name)

    def test_valid_kwargs_property_set(self):
        target = {'database_facade',
                  'gpg_datacontext',
                  'requests_controller'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_valid_kwargs_class_attr_equals_instance_attr(self):
        self.assertEqual(self.x.valid_kwarg_keys, NewContactResponseClientResponseReceiver.kwarg_keys)

    def test_is_nonce_valid_returns_false_if_payload_nonce_false(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=False,
                       request_nonce='')
        result = self.x.is_nonce_valid(payload)
        self.assertIs(result, False)

    def test_is_nonce_valid_returns_true_if_payload_nonce_true(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=True,
                       request_nonce='')
        result = self.x.is_nonce_valid(payload)
        self.assertIs(result, True)

    def test_fetch_contact_request_pubkey_by_nonce_fetches_pubkey_by_nonce_from_payload(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=True,
                       request_nonce='xxx')
        result = self.x.fetch_contact_request_pubkey_by_nonce(payload)
        self.x.database_facade.fetch_contact_request_pub_key_by_nonce.assert_called_with(payload['request_nonce'])

    def test_import_pubkey_to_keyring_calls_gpg_import_and_set_key_methods(self):
        pub_key_string = 'xxxbbbblllaaaa'
        self.x.import_gpg_pub_key_to_key_ring(pub_key_string)
        self.x.gpg_datacontext.import_gpg_pub_key_to_key_ring.assert_called_with(pub_key_string)
        self.assertTrue(self.x.gpg_datacontext.set_key_list.called)

    def test_delete_contact_request_by_gpg_pubkey_calls_db_method(self):
        pub_key_string = 'xxxbbbblllaaaa'
        self.x.delete_contact_request_by_gpg_pubkey(pub_key_string)
        self.x.database_facade.delete_contact_request_where_x_is_y.assert_called_with('gpg_pub_key', pub_key_string)

    def test_update_received_request_treeview_calls_method_on_requests_controler(self):
        self.x.update_received_requests_treeview()
        self.assertTrue(self.x.requests_controller.update_received_requests_treeview.called)

    def test_execute_calls_is_nonce_valid_returns_false_if_is_nonce_valid_false(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=False,
                       request_nonce='')
        target = self.x.is_nonce_valid = MagicMock(return_value=False)
        result = self.x.execute(payload)
        target.assert_called_with(payload)
        self.assertIs(result, False)

    def test_execute_calls_fetch_pubkey_by_nonce_returns_false_if_result_none(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=True,
                       request_nonce='xxx')
        target = self.x.fetch_contact_request_pubkey_by_nonce = MagicMock(return_value=None)
        result = self.x.execute(payload)
        target.assert_called_with(payload)
        self.assertIs(result, False)

    def test_execute_calls_import_gpg_pub_key_method_if_db_fetch_returns_val(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=True,
                       request_nonce='xxx')
        val = 'gpg_pub_key_string'
        sub = self.x.fetch_contact_request_pubkey_by_nonce = MagicMock(return_value=val)
        target = self.x.import_gpg_pub_key_to_key_ring = MagicMock()
        result = self.x.execute(payload)
        target.assert_called_with(sub.return_value)

    def test_execute_calls_delete_and_update_methods_if_db_fetch_returns_val(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=True,
                       request_nonce='xxx')
        val = 'gpg_pub_key_string'
        sub = self.x.fetch_contact_request_pubkey_by_nonce = MagicMock(return_value=val)
        target_1 = self.x.delete_contact_request_by_gpg_pubkey = MagicMock()
        target_2 = self.x.update_received_requests_treeview = MagicMock()
        result = self.x.execute(payload)
        target_1.assert_called_with(sub.return_value)
        target_2.assert_called_with()

    def test_execute_launches_user_alert_on_success(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=True,
                       request_nonce='xxx')

        target = self.x.requests_controller.launch_user_alert = MagicMock()
        result = self.x.execute(payload)
        self.assertTrue(target.called)
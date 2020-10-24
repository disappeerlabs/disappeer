"""
test_receivednewmessagereceiver.py

Test suite for ReceivedNewMessageReceiver module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.executor.receivers import receivednewmessagereceiver
from disappeer.net.message import messagevalidator
from disappeer.popups import popuplauncher
import types


class TestImports(unittest.TestCase):

    def test_abstractreceiver(self):
        self.assertEqual(abstractreceiver, receivednewmessagereceiver.abstractreceiver)

    def test_constants(self):
        self.assertEqual(constants, receivednewmessagereceiver.constants)

    def test_messagevalidator(self):
        self.assertEqual(messagevalidator, receivednewmessagereceiver.messagevalidator)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, receivednewmessagereceiver.popuplauncher)


class TestReceivedNewMessageReceiver(unittest.TestCase):

    def setUp(self):
        self.payload = dict()
        self.kwargs = {'message_controller': MagicMock(),
                       'gpg_datacontext': MagicMock(),
                       'database_facade': MagicMock(),
                       'root_params': MagicMock()
                       }
        self.x = receivednewmessagereceiver.ReceivedNewMessageReceiver(**self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, receivednewmessagereceiver.ReceivedNewMessageReceiver)
        self.assertIsInstance(self.x, abstractreceiver.AbstractReceiver)

    def test_name_property_set(self):
        name = constants.command_list.Received_New_Message + '_Receiver'
        self.assertEqual(self.x.name, name)

    def test_valid_kwargs_property_set(self):
        target = {'message_controller',
                  'gpg_datacontext',
                  'database_facade',
                  'root_params'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_valid_kwargs_class_attr_equals_instance_attr(self):
        self.assertEqual(self.x.valid_kwarg_keys, receivednewmessagereceiver.ReceivedNewMessageReceiver.kwarg_keys)

    @patch('executor.receivers.receivednewmessagereceiver.messagevalidator.MessageValidator')
    def test_validate_message_inits_validator_with_args_calls_validate_returns_validator(self, validator):
        payload_dict = dict()
        result = self.x.validate_message(payload_dict)
        validator.assert_called_with(payload_dict,
                                     self.x.gpg_datacontext.get_home_dir(),
                                     self.x.root_params.get_session_passphrase_observable())
        validator().validate.assert_called_with()
        self.assertIsNotNone(result)

    def test_message_controller_update_received_message_calls_method_with_arg(self):
        self.x.message_controller_update_received_messages_treeview()
        self.x.message_controller.update_received_messages_treeview.assert_called_with()

    def test_message_controller_update_contacts_treeview_calls_method_with_arg(self):
        self.x.message_controller_update_contacts_treeview()
        self.x.message_controller.update_contacts_treeview.assert_called_with()

    def test_database_facade_fetch_peer_contact_by_fingerprint(self):
        fingerprint = 'xxxx'
        target_result = dict()
        target = self.x.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint = MagicMock(return_value=target_result)
        result = self.x.database_facade_fetch_peer_contact_by_fingerprint(fingerprint)
        target.assert_called_with(fingerprint)
        self.assertEqual(result, target.return_value)

    def test_database_facade_insert_peer_contact(self):
        new_peer_payload = dict()
        self.x.database_facade_insert_peer_contact(new_peer_payload)
        self.x.database_facade.insert_peer_contact.assert_called_with(new_peer_payload)

    def test_database_facade_insert_received_message_calls_method_with_arg(self):
        payload = dict()
        self.x.database_facade_insert_received_message(payload)
        self.x.database_facade.insert_received_message.assert_called_with(payload)

    def test_gpg_datacontext_get_key_dict_by_identifier(self):
        fingerprint = 'fingerprint_string'
        val = 'hello there'
        target = self.x.gpg_datacontext.get_key_dict_by_identifier = MagicMock(return_value=val)
        result = self.x.gpg_datacontext_get_key_dict_by_identifier(fingerprint)
        target.assert_called_with(fingerprint)
        self.assertEqual(result, target.return_value)

    def test_gpg_datacontext_export_pubkey_from_key_ring(self):
        fingerprint = 'fingerprint_string'
        val = 'hello there'
        target = self.x.gpg_datacontext.export_pubkey_from_key_ring = MagicMock(return_value=val)
        result = self.x.gpg_datacontext_export_pubkey_from_key_ring(fingerprint)
        target.assert_called_with(fingerprint)
        self.assertEqual(result, target.return_value)

    def test_update_peer_contact_record_updates_address(self):
        peer_record = types.SimpleNamespace(address_port='xxx', gpg_fingerprint='fingerprint', address_host='xxx')
        data_dict = dict(address_port='address_port', address_host='address_host')
        self.x.update_peer_contact_record(data_dict, peer_record)
        self.x.database_facade.update_peer_contact_address_from_fingerprint.assert_called_with(data_dict['address_host'], peer_record.gpg_fingerprint)

    def test_update_peer_contact_record_updates_port(self):
        peer_record = types.SimpleNamespace(address_port='xxx', gpg_fingerprint='fingerprint', address_host='xxx')
        data_dict = dict(address_port='address_port', address_host='address_host')
        self.x.update_peer_contact_record(data_dict, peer_record)
        self.x.database_facade.update_peer_contact_port_from_fingerprint.assert_called_with(data_dict['address_port'], peer_record.gpg_fingerprint)

    def test_build_peer_contact_payload_from_message_validator_results_returns_correct_dict(self):
        msg_data_dict = dict(address_host='address_host', address_port='address_port')
        verify_result = types.SimpleNamespace(fingerprint='fingerprint')
        sub_key_dict = self.x.gpg_datacontext_get_key_dict_by_identifier = MagicMock(return_value=MagicMock())
        sub_key_export = self.x.gpg_datacontext_export_pubkey_from_key_ring = MagicMock(return_value='pub_key_string')
        result = self.x.build_peer_contact_payload_from_message_validator_results(msg_data_dict, verify_result)
        target_result = dict(gpg_pub_key=sub_key_export.return_value,
                             gpg_uid=sub_key_dict.return_value['uids'][0],
                             gpg_fingerprint=verify_result.fingerprint,
                             address_host=msg_data_dict['address_host'],
                             address_port=msg_data_dict['address_port'])
        self.assertEqual(result, target_result)

    def test_check_peer_contact_from_new_message_calls_update_methods_if_peer_exists(self):
        msg_data_dict = dict(address_host='address_host', address_port='address_port')
        verify_result = types.SimpleNamespace(fingerprint='fingerprint')
        sub = self.x.database_facade_fetch_peer_contact_by_fingerprint = MagicMock(return_value=[1,2])
        target_update_1 = self.x.update_peer_contact_record = MagicMock()
        target_update_2 = self.x.message_controller_update_contacts_treeview = MagicMock()
        result = self.x.check_peer_contact_from_new_message(msg_data_dict, verify_result)
        sub.assert_called_with(verify_result.fingerprint)
        target_update_1.assert_called_with(msg_data_dict, sub.return_value)
        target_update_2.assert_called_with()
        self.assertIsNone(result)

    def test_check_peer_contact_from_new_message_builds_and_inserts_new_peer_msg_if_new_peer(self):
        msg_data_dict = dict(address_host='address_host', address_port='address_port')
        verify_result = types.SimpleNamespace(fingerprint='fingerprint')
        sub = self.x.database_facade_fetch_peer_contact_by_fingerprint = MagicMock(return_value=[])
        peer_payload = 'xxxx'
        target_1 = self.x.build_peer_contact_payload_from_message_validator_results = MagicMock(return_value=peer_payload)
        target_2 = self.x.database_facade_insert_peer_contact = MagicMock()
        target_3 = self.x.message_controller_update_contacts_treeview = MagicMock()
        target_4 = self.x.launch_blink_alert = MagicMock()
        result = self.x.check_peer_contact_from_new_message(msg_data_dict, verify_result)
        target_1.assert_called_with(msg_data_dict, verify_result)
        target_2.assert_called_with(target_1.return_value)
        target_3.assert_called_with()
        self.assertTrue(target_4.called)

    @patch('disappeer.popups.popuplauncher.launch_alert_box_popup')
    def test_launch_alert_box_popup(self, popup_func):
        msg = 'msg'
        self.x.launch_alert_log(msg)
        popup_func.assert_called_with(self.x.root_params.root, msg)

    @patch('disappeer.popups.popuplauncher.launch_blink_alert_popup')
    def test_launch_blink_popup(self, popup_func):
        msg = 'msg'
        self.x.launch_blink_alert(msg)
        popup_func.assert_called_with(self.x.root_params.root, msg)

    def test_execute_calls_validator_with_payload(self):
        incoming_payload = dict(payload=dict())
        target = self.x.validate_message = MagicMock()
        sub = self.x.launch_blink_alert = MagicMock()
        self.x.execute(incoming_payload)
        target.assert_called_with(incoming_payload['payload'])

    def test_execute_calls_correct_methods_if_validator_valid(self):
        class MockValidator:
            valid = True
            data_dict = dict()
            verify_result = dict()
        incoming_payload = dict(payload=dict())
        validator = MockValidator()
        validate_method = self.x.validate_message = MagicMock(return_value=validator)
        target_1 = self.x.database_facade_insert_received_message = MagicMock()
        target_2 = self.x.check_peer_contact_from_new_message = MagicMock()
        target_3 = self.x.message_controller_update_received_messages_treeview = MagicMock()
        self.x.execute(incoming_payload)
        target_1.assert_called_with(incoming_payload['payload'])
        target_2.assert_called_with(validator.data_dict, validator.verify_result)
        target_3.assert_called_with()


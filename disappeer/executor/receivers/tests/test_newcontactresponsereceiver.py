"""
test_newcontactresponsereceiver.py

Test suite for NewContactResponseReceiver object . . .

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.executor.receivers import newcontactresponsereceiver
from disappeer.executor.receivers.newcontactresponsereceiver import NewContactResponseReceiver
from disappeer.net.contactresponse import contactresponsevalidator
from disappeer.gpg.helpers import gpgpubkeyvalidator
from disappeer.popups import popuplauncher


class TestImports(unittest.TestCase):

    def test_abstractreceiver(self):
        self.assertEqual(abstractreceiver, newcontactresponsereceiver.abstractreceiver)

    def test_constants(self):
        self.assertEqual(constants, newcontactresponsereceiver.constants)

    def test_contactresponsevalidator(self):
        self.assertEqual(contactresponsevalidator, newcontactresponsereceiver.contactresponsevalidator)

    def test_gpgpubkeyvalidator(self):
        self.assertEqual(gpgpubkeyvalidator, newcontactresponsereceiver.gpgpubkeyvalidator)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, newcontactresponsereceiver.popuplauncher)


class TestNewContactResponseReceiver(unittest.TestCase):

    def setUp(self):
        self.payload = dict()
        self.kwargs = {'database_facade': MagicMock(),
                       'gpg_datacontext': MagicMock(),
                       'root_params': MagicMock(),
                       'message_controller': MagicMock(),
                       'requests_controller': MagicMock()}
        self.x = newcontactresponsereceiver.NewContactResponseReceiver(**self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, newcontactresponsereceiver.NewContactResponseReceiver)
        self.assertIsInstance(self.x, abstractreceiver.AbstractReceiver)

    def test_name_property_set(self):
        name = constants.command_list.New_Contact_Res + '_Receiver'
        self.assertEqual(self.x.name, name)

    def test_valid_kwargs_property_set(self):
        target = {'database_facade',
                  'gpg_datacontext',
                  'root_params',
                  'message_controller',
                  'requests_controller'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_valid_kwargs_class_attr_equals_instance_attr(self):
        self.assertEqual(self.x.valid_kwarg_keys, NewContactResponseReceiver.kwarg_keys)

    @patch('executor.receivers.newcontactresponsereceiver.contactresponsevalidator.ContactResponseValidator')
    def test_validate_contact_response_method_calls_validator_with_args_calls_validate_returns_validator(self, validator):
        payload = dict()
        result = self.x.validate_contact_response(payload)
        validator.assert_called_with(payload,
                                     self.x.gpg_datacontext.get_home_dir(),
                                     self.x.database_facade.get_pending_contact_response_table(),
                                     self.x.root_params.get_session_passphrase_observable())
        self.assertEqual(result, validator())
        validator().validate.assert_called_with()

    def test_fetch_contact_response_pubkey_by_nonce_fetches_pubkey_by_nonce_from_validator_data_dict(self):
        payload = dict(request_nonce='xxx')
        target_return_val = '12345'
        self.x.database_facade.fetch_contact_response_pub_key_by_nonce.return_value=target_return_val

        result = self.x.fetch_contact_response_pub_key_by_nonce(payload)
        self.x.database_facade.fetch_contact_response_pub_key_by_nonce.assert_called_with(payload['request_nonce'])
        self.assertEqual(result, target_return_val)

    @patch('executor.receivers.newcontactresponsereceiver.gpgpubkeyvalidator.GPGPubKeyValidator')
    def test_validate_pubkey_calls_validator_with_arg_returns_validator(self, validator):
        class MockValidatorTrue:
            valid = True
            key_dict = dict(fingerprint='fingerprint_string')
        validator.return_value = MockValidatorTrue()
        pubkey_string = 'pubkey_string'
        result = self.x.validate_pubkey(pubkey_string)
        validator.assert_called_with(pubkey_string)
        self.assertEqual(result, validator.return_value)

    def test_build_peer_contact_payload_builds_correct_payload(self):
        gpg_pub_key = MagicMock()
        gpg_pub_key_validator = MagicMock()
        contact_response_data_dict = MagicMock()

        # - store necessary info in new PeerMessageServer db table
        target_peer_contact_payload = dict(gpg_pub_key=gpg_pub_key,
                                           gpg_uid=gpg_pub_key_validator.key_dict['uids'][0],
                                           gpg_fingerprint=gpg_pub_key_validator.key_dict['fingerprint'],
                                           address_host=contact_response_data_dict['address_host'],
                                           address_port=contact_response_data_dict['address_port'])

        result = self.x.build_peer_contact_payload(gpg_pub_key,
                                                   gpg_pub_key_validator,
                                                   contact_response_data_dict)
        self.assertEqual(result, target_peer_contact_payload)

    def test_database_facade_insert_peer_contact_calls_method_with_arg(self):
        peer_contact_payload = dict()
        self.x.database_facade_insert_peer_contact(peer_contact_payload)
        self.x.database_facade.insert_peer_contact.assert_called_with(peer_contact_payload)

    def test_import_pubkey_to_keyring_calls_gpg_import_and_set_key_methods(self):
        pub_key_string = 'xxxbbbblllaaaa'
        self.x.import_gpg_pub_key_to_key_ring(pub_key_string)
        self.x.gpg_datacontext.import_gpg_pub_key_to_key_ring.assert_called_with(pub_key_string)
        self.assertTrue(self.x.gpg_datacontext.set_key_list.called)

    def test_message_controller_update_contacts_treeview_calls_method(self):
        self.x.message_controller_update_contacts_treeview()
        self.x.message_controller.update_contacts_treeview.assert_called_with()

    def test_requests_controller_update_sent_requests_treeview(self):
        self.x.requests_controller_update_sent_requests_treeview()
        self.x.requests_controller.update_sent_requests_treeview.assert_called_with()

    def test_database_facade_delete_pending_contact_response_by_gpg_fingerprint(self):
        gpg_pub_key_validator = MagicMock()
        self.x.database_facade_delete_pending_contact_response_by_gpg_fingerprint(gpg_pub_key_validator)
        self.x.database_facade.delete_pending_contact_response_where_x_is_y.assert_called_with('gpg_fingerprint', gpg_pub_key_validator.key_dict['fingerprint'])

    @patch('disappeer.popups.popuplauncher.launch_blink_alert_popup')
    def test_launch_blink_popup(self, popup_func):
        msg = 'msg'
        self.x.launch_blink_alert(msg)
        popup_func.assert_called_with(self.x.root_params.root, msg)

    @patch('disappeer.popups.popuplauncher.launch_alert_box_popup')
    def test_launch_alert_box_popup(self, popup_func):
        msg = 'msg'
        self.x.launch_alert_log(msg)
        popup_func.assert_called_with(self.x.root_params.root, msg)


    def test_execute_method_calls_validate_contact_response_with_payload(self):
        payload = dict()
        sub = self.x.validate_pubkey = MagicMock()
        sub_1 = self.x.launch_blink_alert = MagicMock()
        target = self.x.validate_contact_response = MagicMock()
        self.x.execute(payload)
        target.assert_called_with(payload)

    def test_execute_calls_alert_log_returns_false_if_validator_false(self):
        class MockValidator:
            valid = False
            error = 'err msg'

        validator = MockValidator()
        payload = dict()
        sub = self.x.validate_contact_response = MagicMock(return_value=validator)
        target = self.x.launch_alert_log = MagicMock()
        result = self.x.execute(payload)
        self.assertIs(result, False)
        self.assertTrue(target.called)

    def test_execute_calls_handle_valid_contact_response_with_data_dict_if_validator_true(self):
        class MockValidator:
            valid = True
            error = 'err msg'
            data_dict = MagicMock()

        validator = MockValidator()
        payload = dict()
        sub = self.x.validate_contact_response = MagicMock(return_value=validator)
        target = self.x.handle_valid_contact_response = MagicMock()
        result = self.x.execute(payload)
        target.assert_called_with(validator.data_dict)

    def test_handle_valid_contact_response_gets_pubkey_from_db_if_validator_true(self):
        mock_valid_data_dict = MagicMock()
        sub = self.x.validate_pubkey = MagicMock()
        sub_1 = self.x.launch_blink_alert = MagicMock()
        target = self.x.fetch_contact_response_pub_key_by_nonce = MagicMock()
        result = self.x.handle_valid_contact_response(mock_valid_data_dict)
        target.assert_called_with(mock_valid_data_dict)

    def test_handle_valid_contact_response_calls_gpg_validator_with_key_from_db(self):
        mock_valid_data_dict = MagicMock()
        mock_gpg_key = 'xxxgpgkey'
        sub_1 = self.x.launch_blink_alert = MagicMock()

        sub = self.x.fetch_contact_response_pub_key_by_nonce = MagicMock(return_value=mock_gpg_key)
        target = self.x.validate_pubkey = MagicMock()
        result = self.x.handle_valid_contact_response(mock_valid_data_dict)
        target.assert_called_with(sub.return_value)

    def test_handle_valid_contact_response_returns_false_if_gpg_validator_false(self):
        class MockValidator:
            valid = False
            error = 'err msg'

        mock_valid_data_dict = dict()
        mock_gpg_key = 'xxxgpgkey'
        validator = MockValidator()
        sub = self.x.fetch_contact_response_pub_key_by_nonce = MagicMock(return_value=mock_gpg_key)
        target = self.x.validate_pubkey = MagicMock(return_value=validator)
        result = self.x.handle_valid_contact_response(mock_valid_data_dict)
        self.assertIs(result, False)

    def test_handle_valid_contact_response_calls_remaining_if_gpg_valid(self):
        class MockValidator:
            valid = True
            error = 'err msg'
            key_dict = MagicMock()

        mock_valid_data_dict = dict()
        mock_gpg_key = 'xxxgpgkey'
        validator = MockValidator()
        sub_pubkey = self.x.fetch_contact_response_pub_key_by_nonce = MagicMock(return_value=mock_gpg_key)
        sub_gpg_validator = self.x.validate_pubkey = MagicMock(return_value=validator)
        peer_payload = MagicMock()
        target_1 = self.x.build_peer_contact_payload = MagicMock(return_value=peer_payload)
        target_2 = self.x.database_facade_insert_peer_contact = MagicMock()
        target_3 = self.x.import_gpg_pub_key_to_key_ring = MagicMock()
        target_4 = self.x.message_controller_update_contacts_treeview = MagicMock()
        target_5 = self.x.database_facade_delete_pending_contact_response_by_gpg_fingerprint = MagicMock()
        target_6 = self.x.requests_controller_update_sent_requests_treeview = MagicMock()
        target_7 = self.x.launch_blink_alert = MagicMock()
        result = self.x.handle_valid_contact_response(mock_valid_data_dict)
        target_1.assert_called_with(sub_pubkey.return_value, sub_gpg_validator.return_value, mock_valid_data_dict)
        target_2.assert_called_with(target_1.return_value)
        target_3.assert_called_with(sub_pubkey.return_value)
        target_4.assert_called_with()
        target_5.assert_called_with(sub_gpg_validator.return_value)
        target_6.assert_called_with()
        self.assertTrue(target_7.called)



"""
test_messagescontroller.py

Test suite for the MessagesController class object and module.
Controller for the MessagesFrame notebook tab

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.messages import messagescontroller
import tkinter
from disappeer.models.db import dbreceivedmessagestable
from disappeer import settings
from disappeer.utilities import observable
from disappeer.net.message import messagevalidator
from disappeer.popups import popuplauncher
from disappeer.constants import constants
import types
from disappeer.root import rootparameters
import queue
from disappeer.utilities import logger
from disappeer.utilities.logger import log
from disappeer.models.db import databasefacade
import os


class TestImports(unittest.TestCase):

    def test_settings(self):
        self.assertEqual(settings, messagescontroller.settings)

    def test_messagevalidator(self):
        self.assertEqual(messagevalidator, messagescontroller.messagevalidator)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, messagescontroller.popuplauncher)

    def test_constants(self):
        self.assertEqual(constants, messagescontroller.constants)

    def test_types(self):
        self.assertEqual(types, messagescontroller.types)

    def test_logger(self):
        self.assertEqual(logger, messagescontroller.logger)

    def test_log(self):
        self.assertEqual(logger.log, messagescontroller.log)


class TestMessagesControllerClassBasics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tkinter_root = tkinter.Tk()

    def setUp(self):
        self.command = "<ButtonRelease-1>"
        self.root = self.tkinter_root
        self.root_view = MagicMock()
        self.root_queue = queue.Queue()
        self.database_facade = MagicMock(spec=databasefacade.DatabaseFacade)
        self.mock_observer = MagicMock()
        self.root_params = rootparameters.RootParameters(self.root, self.root_view, self.root_queue, self.database_facade, self.mock_observer)
        mock_view_method = self.root_params.get_messages_frame = MagicMock(return_value=MagicMock())
        self.view = mock_view_method.return_value
        self.gpg_home_dir_observer = observable.Observable()
        self.gpg_home_dir_observer.set("tests/data/msg_ctrlr_keys")
        self.x = messagescontroller.MessagesController(self.root_params,
                                                       self.gpg_home_dir_observer)

    def tearDown(self):
        pass

    def test_instance(self):
        self.assertIsInstance(self.x, messagescontroller.MessagesController)

    def test_root_params_attr_set(self):
        self.assertEqual(self.root_params, self.x.root_params)

    def test_root_attribute_set(self):
        self.assertEqual(self.root, self.x.root)

    def test_view_attribute_set(self):
        self.assertEqual(self.view, self.x.view)

    def test_root_queue_attr_set(self):
        self.assertEqual(self.root_queue, self.x.root_queue)

    def test_database_facade_attr_set(self):
        self.assertEqual(self.x.database_facade, self.x.root_params.database_facade)

    def test_gpg_home_dir_observer_set(self):
        self.assertEqual(self.x.gpg_home_dir_observer, self.gpg_home_dir_observer)

    def test_current_treeview_item_is_none(self):
        self.assertIsNone(self.x.current_treeview_item)

    def test_config_event_bindings_calls_bind_on_message_treeview_item_click(self):
        self.x.config_event_bindings()
        self.view.message_tree_view.bind.assert_called_with(self.command, self.x.message_treeview_clicked)

    def test_config_event_bindings_calls_bind_on_peer_contacts_treeview_item(self):
        self.x.config_event_bindings()
        self.x.view.contacts_tree_view.bind.assert_called_with(self.command, self.x.peer_contacts_treeview_clicked)

    @patch('disappeer.messages.messagescontroller.MessagesController.config_event_bindings')
    def test_constructor_calls_config_event_bindings(self, mocked_method):
        self.x = messagescontroller.MessagesController(self.root_params, self.gpg_home_dir_observer)
        self.assertTrue(mocked_method.called)

    def test_update_received_messages_treeview(self):
        val = 'xxx'
        target_1 = self.x.database_facade.fetch_all_received_message_nonces_with_status = MagicMock(return_value=val)
        target_2 = self.x.view.update_message_tree_view_received = MagicMock()
        self.x.update_received_messages_treeview()
        target_1.assert_called_with()
        target_2.assert_called_with(target_1.return_value)

    def test_update_sent_messages_treeview(self):
        val = 'xxx'
        target_1 = self.x.database_facade.fetch_all_sent_message_nonces = MagicMock(return_value=val)
        target_2 = self.x.view.update_message_tree_view_sent = MagicMock()
        self.x.update_sent_messages_treeview()
        target_1.assert_called_with()
        target_2.assert_called_with(target_1.return_value)

    def test_update_all_treeviews_updates_all_treeviews(self):
        target_1 = self.x.update_sent_messages_treeview = MagicMock()
        target_2 = self.x.update_received_messages_treeview = MagicMock()
        target_3 = self.x.update_contacts_treeview = MagicMock()
        self.x.update_all_treeviews()
        target_1.assert_called_with()
        target_2.assert_called_with()
        target_3.assert_called_with()

    @patch('disappeer.messages.messagescontroller.MessagesController.update_all_treeviews')
    def test_constructor_calls_update_all_treeviews_method(self, mocked_method):
        self.x = messagescontroller.MessagesController(self.root_params, self.gpg_home_dir_observer)
        self.assertTrue(mocked_method.called)

    def test_message_treeview_clicked_calls_view_get_clicked_treeview_item(self):
        self.x.message_treeview_clicked(None)
        self.x.view.get_clicked_treeview_item_parent_nonce_and_iid.assert_called_with()

    def test_message_treeview_clicked_returns_none_if_treeview_returns_none(self):
        target_method = self.x.view.get_clicked_treeview_item_parent_nonce_and_iid
        target_method.return_value = None
        result = self.x.message_treeview_clicked(None)
        self.assertIsNone(result)

    def test_message_treeview_clicked_fetches_received_record_if_treeview_returns_received(self):
        sub = self.x.view.get_clicked_treeview_item_parent_nonce_and_iid
        val = ('Received', 'nonceval')
        sub.return_value = val
        target = self.x.database_facade.fetch_one_received_message_named_tuple_by_nonce = MagicMock()
        result = self.x.message_treeview_clicked(None)
        target.assert_called_with(val[1])

    def test_message_treeview_clicked_fetches_sent_record_if_treeview_returns_sent(self):
        sub = self.x.view.get_clicked_treeview_item_parent_nonce_and_iid
        val = ('Sent', 'nonceval')
        sub.return_value = val
        target = self.x.database_facade.fetch_one_sent_message_named_tuple_by_nonce = MagicMock()
        result = self.x.message_treeview_clicked(None)
        target.assert_called_with(val[1])

    def test_message_treeview_clicked_returns_none_if_invalid_parent(self):
        sub = self.x.view.get_clicked_treeview_item_parent_nonce_and_iid
        val = ('sssss', 'nonceval')
        sub.return_value = val
        target = self.x.database_facade.fetch_one_sent_message_named_tuple_by_nonce = MagicMock()
        result = self.x.message_treeview_clicked(None)
        self.assertIsNone(result)

    def test_message_treeview_clicked_calls_validate_and_view_record_with_valid_record(self):
        sub = self.x.view.get_clicked_treeview_item_parent_nonce_and_iid
        val = ('Sent', 'nonceval')
        sub.return_value = val
        val_1 = ('nonce', 'ciphertext')
        sub_1 = self.x.database_facade.fetch_one_sent_message_named_tuple_by_nonce = MagicMock(return_value=val_1)
        target = self.x.validate_and_view_record = MagicMock()
        result = self.x.message_treeview_clicked(None)
        target.assert_called_with(sub_1.return_value)

    def test_message_treeview_clicked_sets_current_treeview_item_attr(self):
        sub = self.x.view.get_clicked_treeview_item_parent_nonce_and_iid
        val = ('Sent', 'nonceval')
        sub.return_value = val
        val_1 = ('nonce', 'ciphertext')
        sub_1 = self.x.database_facade.fetch_one_sent_message_named_tuple_by_nonce = MagicMock(return_value=val_1)
        target = self.x.validate_and_view_record = MagicMock()
        result = self.x.message_treeview_clicked(None)
        self.assertEqual(sub.return_value, self.x.current_treeview_item)

    @patch('disappeer.net.message.messagevalidator.MessageValidator')
    def test_validate_and_view_record_inits_validator_with_record_payload(self, validator):
        nonce_1 = 'nonce_string_1'
        payload = dict(nonce=nonce_1, ciphertext='ciphertext_string')
        stub = self.x.display_record = MagicMock()
        self.change_source_db()
        nonce_val = 'random_nonce'
        sub = self.x.database_facade.received_messages_table.random_hash = MagicMock(return_value=nonce_val)
        self.x.database_facade.received_messages_table.handle_new_payload(payload)
        result = self.x.database_facade.received_messages_table.fetch_named_tuple_by_nonce(sub.return_value)
        self.x.validate_and_view_record(result)
        validator.assert_called_with(result._asdict(), self.x.gpg_home_dir_observer.get(), self.x.root_params.get_session_passphrase_observable())

    @patch.object(messagescontroller.messagevalidator.MessageValidator, 'validate')
    def test_validate_and_view_record_validates_received_record_payload(self, method):
        nonce_1 = 'nonce_string_1'
        payload = dict(nonce=nonce_1, ciphertext='ciphertext_string')
        stub = self.x.display_record = MagicMock()
        self.change_source_db()
        nonce_val = 'random_nonce'
        sub = self.x.database_facade.received_messages_table.random_hash = MagicMock(return_value=nonce_val)
        self.x.database_facade.received_messages_table.handle_new_payload(payload)
        result = self.x.database_facade.received_messages_table.fetch_named_tuple_by_nonce(sub.return_value)
        self.x.validate_and_view_record(result)
        self.assertTrue(method.called)

    @patch('disappeer.net.message.messagevalidator.MessageValidator')
    def test_validate_and_view_record_calls_display_record_with_validator_if_valid(self, validator):
        class MockValid(MagicMock):
            valid = True

        stub = self.x.display_record = MagicMock()
        validator.return_value = MockValid()
        nonce_1 = 'nonce_string_1'
        payload = dict(nonce=nonce_1, ciphertext='ciphertext_string')
        self.change_source_db()
        nonce_val = 'random_nonce'
        sub = self.x.database_facade.received_messages_table.random_hash = MagicMock(return_value=nonce_val)
        self.x.database_facade.received_messages_table.handle_new_payload(payload)
        result = self.x.database_facade.received_messages_table.fetch_named_tuple_by_nonce(sub.return_value)
        target = self.x.display_record = MagicMock()
        self.x.validate_and_view_record(result)
        target.assert_called_with(validator.return_value)

    @patch('net.message.messagevalidator.MessageValidator')
    def test_validate_and_view_record_does_not_call_display_record_on_NOT_valid(self, validator):
        class MockValid(MagicMock):
            valid = False

        validator.return_value = MockValid()
        nonce_1 = 'nonce_string_1'
        payload = dict(nonce=nonce_1, ciphertext='ciphertext_string')
        self.change_source_db()
        nonce_val = 'random_nonce'
        sub = self.x.database_facade.received_messages_table.random_hash = MagicMock(return_value=nonce_val)
        self.x.database_facade.received_messages_table.handle_new_payload(payload)
        result = self.x.database_facade.received_messages_table.fetch_named_tuple_by_nonce(sub.return_value)
        target = self.x.display_record = MagicMock()
        self.x.validate_and_view_record(result)
        self.assertFalse(target.called)

    @patch.object(messagescontroller.popuplauncher, 'DisplayMessageController')
    @patch.object(messagescontroller.popuplauncher, 'launch_displaymessage_popup')
    def test_display_record_launches_display_message_popup(self, pop, controller):
        mock_validator = MagicMock()
        from_user = mock_validator.verify_result.username
        fingerprint = mock_validator.verify_result.fingerprint
        message = mock_validator.data_dict['message'].strip()
        sent_from = mock_validator.data_dict['sent_from'].strip()
        sent_to = mock_validator.data_dict['sent_to'].strip()
        msg_type = self.x.current_treeview_item = (1,2)
        mock_namespace = types.SimpleNamespace()
        mock_namespace.message_type = msg_type[0]
        mock_namespace.message_to = sent_to
        mock_namespace.message_from = sent_from
        mock_namespace.message_text = message
        target = self.x.handle_display_record_result = MagicMock()
        self.x.display_record(mock_validator)
        pop.assert_called_with(self.x.root, mock_namespace)

    @patch.object(messagescontroller.popuplauncher, 'DisplayMessageController')
    @patch.object(messagescontroller.popuplauncher, 'launch_displaymessage_popup')
    def test_display_record_calls_handle_display_record_result_with_result_and_argspace(self, pop, controller):
        mock_validator = MagicMock()
        from_user = mock_validator.verify_result.username
        fingerprint = mock_validator.verify_result.fingerprint
        message = mock_validator.data_dict['message'].strip()
        sent_from = mock_validator.data_dict['sent_from'].strip()
        sent_to = mock_validator.data_dict['sent_to'].strip()
        msg_type = self.x.current_treeview_item = (1,2)
        mock_namespace = types.SimpleNamespace()
        mock_namespace.message_type = msg_type[0]
        mock_namespace.message_to = sent_to
        mock_namespace.message_from = sent_from
        mock_namespace.message_text = message
        pop.return_value = 'val'
        target = self.x.handle_display_record_result = MagicMock()
        self.x.display_record(mock_validator)
        target.assert_called_with(pop.return_value, mock_namespace)

    def test_handle_display_record_result_updates_message_treeview_and_received_msg_db_if_result_none(self):
        target_1 = self.x.view.update_message_tree_view_received_item_as_read = MagicMock()
        target_2 = self.x.database_facade.update_received_message_to_read = MagicMock()
        vals = (1,2,3)
        self.x.current_treeview_item = vals
        mock_namespace = types.SimpleNamespace()
        self.x.handle_display_record_result(None, mock_namespace)
        target_1.assert_called_with(self.x.current_treeview_item[-1])
        target_2.assert_called_with(self.x.current_treeview_item[1])

    def test_handle_display_record_result_deletes_received_message_treeview_and_received_msg_db_on_delete(self):
        target_1 = self.x.view.delete_message_treeview_item_by_iid = MagicMock()
        target_2 = self.x.database_facade.delete_received_message_where_x_is_y = MagicMock()
        vals = ('Received', 2,3)
        self.x.current_treeview_item = vals
        mock_namespace = types.SimpleNamespace()
        self.x.handle_display_record_result('delete', mock_namespace)
        target_1.assert_called_with(self.x.current_treeview_item[-1])
        target_2.assert_called_with('nonce', self.x.current_treeview_item[1])

    def test_handle_display_record_result_deletes_received_message_treeview_and_received_msg_db_on_delete(self):
        target_1 = self.x.view.delete_message_treeview_item_by_iid = MagicMock()
        target_2 = self.x.database_facade.delete_sent_message_where_x_is_y = MagicMock()
        vals = ('Sent', 2, 3)
        self.x.current_treeview_item = vals
        mock_namespace = types.SimpleNamespace()
        self.x.handle_display_record_result('delete', mock_namespace)
        target_1.assert_called_with(self.x.current_treeview_item[-1])
        target_2.assert_called_with('nonce', self.x.current_treeview_item[1])

    def test_handle_display_record_result_calls_put_inspect_message_to_queue_on_inspect(self):
        vals = ('Sent', 2, 3)
        self.x.current_treeview_item = vals
        mock_namespace = types.SimpleNamespace()
        target = self.x.put_inspect_message_to_queue = MagicMock()
        self.x.handle_display_record_result('inspect', mock_namespace)
        target.assert_called_with(mock_namespace)

    def change_source_db(self):
        path = 'tests/data/testdb.sqlite'
        if os.path.isfile(path):
            os.remove(path)
        self.x.database_facade.received_messages_table = dbreceivedmessagestable.DBPReceivedMessagesTable(path)

    def test_update_contacts_treeview_calls_fetch_uids_and_fingerprints_with_status(self):
        target = self.x.database_facade.fetch_all_peer_contact_uids_and_fingerprints_with_status = MagicMock()
        self.x.update_contacts_treeview()
        target.assert_called_with()

    def test_update_contacts_treeview_calls_append_all_method_on_view(self):
        val = [(1), (2)]
        sub = self.x.database_facade.fetch_all_peer_contact_uids_and_fingerprints_with_status = MagicMock()
        self.x.update_contacts_treeview()
        self.x.view.append_all_to_peer_contacts.assert_called_with(sub.return_value)

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_gets_clicked_item_nonce_from_view(self, pop, controller):
        target = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock()
        self.x.peer_contacts_treeview_clicked(None)
        target.assert_called_with()

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_returns_none_if_treeview_returns_none(self, pop, controller):
        target = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock(return_value=None)
        result = self.x.peer_contacts_treeview_clicked(None)
        self.assertIsNone(result)

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_calls_db_method_with_treeview_id(self, pop, controller):
        val = 'xxx'
        sub = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock(return_value=val)
        target = self.x.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint = MagicMock()
        self.x.peer_contacts_treeview_clicked(None)
        target.assert_called_with(sub.return_value)

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_launches_popup_with_data_record(self, pop, controller):
        val = 'xxx'
        data_record = ('xxxx')
        sub = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock(return_value=val)
        sub_1 = self.x.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint = MagicMock(return_value=data_record)
        self.x.peer_contacts_treeview_clicked(None)
        pop.assert_called_with(self.x.root, sub_1.return_value)

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_calls_db_method_to_update_record_status_to_read_calls_update_treeview(self, pop, controller):
        val = 'xxx'
        data_record = ('xxxx')
        sub = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock(return_value=val)
        sub_1 = self.x.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint = MagicMock(return_value=data_record)
        target_db = self.x.database_facade.update_peer_contact_status_to_read = MagicMock()
        target_view_method = self.x.update_contacts_treeview = MagicMock()
        self.x.peer_contacts_treeview_clicked(None)
        target_db.assert_called_with(sub.return_value)
        target_view_method.assert_called_with()

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_returns_none_if_popup_returns_none(self, pop, controller):
        val = 'xxx'
        data_record = ('xxxx')
        sub = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock(return_value=val)
        sub_1 = self.x.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint = MagicMock(return_value=data_record)
        pop.return_value = None
        result = self.x.peer_contacts_treeview_clicked(None)
        self.assertIsNone(result)

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_calls_send_to_queue_if_popup_returns_send(self, pop, controller):
        val = 'xxx'
        data_record = ('xxxxxxxx')
        sub = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock(return_value=val)
        sub_1 = self.x.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint = MagicMock(return_value=data_record)
        target = self.x.put_send_new_message_data_record_to_queue = MagicMock()
        pop.return_value = 'send'
        result = self.x.peer_contacts_treeview_clicked(None)
        target.assert_called_with(sub_1.return_value)

    @patch.object(messagescontroller.popuplauncher, 'PeerContactController')
    @patch.object(messagescontroller.popuplauncher, 'launch_peercontact_popup')
    def test_peer_contacts_treeview_clicked_calls_db_delete_method_updates_view_if_popup_returns_delete(self, pop, controller):
        val = 'xxx'
        data_record = ('xxxx')
        sub = self.x.view.get_clicked_contacts_treeview_contact_id = MagicMock(return_value=val)
        sub_1 = self.x.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint = MagicMock(return_value=data_record)
        target = self.x.database_facade.delete_peer_contact_by_fingerprint = MagicMock()
        target_2 = self.x.update_contacts_treeview = MagicMock()
        pop.return_value = 'delete'
        result = self.x.peer_contacts_treeview_clicked(None)
        target.assert_called_with(sub.return_value)
        target_2.assert_called_with()

    def test_put_send_new_message_to_queue_prepares_payload_and_calls_put_to_queue(self):
        data_record = ()
        target_data_dict = dict(desc=constants.command_list.Send_New_Message,
                                data_record=data_record)
        target_method = self.x.root_queue = MagicMock()
        self.x.put_send_new_message_data_record_to_queue(data_record)
        target_method.put.assert_called_with(target_data_dict)

    def test_put_inspect_message_to_queue_prepares_payload_and_calls_put_to_queue(self):
        data_record = types.SimpleNamespace()
        target_data_dict = dict(desc=constants.command_list.Inspect_Message,
                                payload=data_record)
        target_method = self.x.root_queue = MagicMock()
        self.x.put_inspect_message_to_queue(data_record)
        target_method.put.assert_called_with(target_data_dict)

    @patch.object(messagescontroller.popuplauncher, 'launch_alert_box_popup')
    def test_launch_user_alert_launches_alert_with_msg(self, alertbox):
        msg = 'hello'
        self.x.launch_user_alert(msg)
        alertbox.assert_called_with(self.x.root, msg)
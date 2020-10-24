"""
test_sendnewmessageclientresponsereceiver.py

Test suite for HandleSendNewMessageClientResponseReceiver

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.executor.receivers import sendnewmessageclientresponsereceiver as receiver
import types


class TestImports(unittest.TestCase):

    def test_abstractreceiver(self):
        self.assertEqual(abstractreceiver, receiver.abstractreceiver)

    def test_constants(self):
        self.assertEqual(constants, receiver.constants)


class TestSendNewMessageClientResponseReceiver(unittest.TestCase):

    def setUp(self):
        self.payload = dict()
        self.kwargs = {'database_facade': MagicMock(),
                       'message_controller': MagicMock()}
        self.x = receiver.SendNewMessageClientResponseReceiver(**self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, receiver.SendNewMessageClientResponseReceiver)
        self.assertIsInstance(self.x, abstractreceiver.AbstractReceiver)

    def test_name_property_set(self):
        name = constants.command_list.Send_New_Message_Client_Res + '_Receiver'
        self.assertEqual(self.x.name, name)

    def test_valid_kwargs_property_set(self):
        target = {'database_facade',
                  'message_controller'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_valid_kwargs_class_attr_equals_instant_attr(self):
        self.assertEqual(self.x.valid_kwarg_keys, receiver.SendNewMessageClientResponseReceiver.kwarg_keys)

    def test_is_nonce_valid_returns_false_if_payload_nonce_false(self):
        payload = dict(nonce_valid=False)
        result = self.x.is_nonce_valid(payload)
        self.assertIs(result, False)

    def test_is_nonce_valid_returns_true_if_payload_nonce_true(self):
        payload = dict(nonce_valid=True)
        result = self.x.is_nonce_valid(payload)
        self.assertIs(result, True)

    def test_database_facade_insert_sent_message_from_argspace_payload_dict(self):
        target_payload_dict = dict()
        argspace = types.SimpleNamespace(payload_dict=target_payload_dict)
        payload = dict(nonce_valid=True,
                       argnamespace=argspace)
        self.x.insert_sent_message_from_payload_argspace_payload_dict(payload)
        self.x.database_facade.insert_sent_message.assert_called_with(target_payload_dict)

    def test_update_sent_messages_treeview_updates_method_on_messages_controller(self):
        self.x.update_sent_messages_treeview()
        self.x.message_controller.update_sent_messages_treeview.assert_called_with()

    def test_execute_calls_is_nonce_valid_returns_false_if_is_nonce_valid_false(self):
        payload = dict(nonce_valid=True)
        target = self.x.is_nonce_valid = MagicMock(return_value=False)
        result = self.x.execute(payload)
        target.assert_called_with(payload)
        self.assertIs(result, False)

    def test_execute_calls_insert_message_with_payload_if_nonce_valid(self):
        target_payload_dict = dict()
        argspace = types.SimpleNamespace(payload_dict=target_payload_dict)
        payload = dict(nonce_valid=True,
                       argnamespace=argspace)
        target = self.x.insert_sent_message_from_payload_argspace_payload_dict = MagicMock()
        result = self.x.execute(payload)
        target.assert_called_with(payload)

    def test_execute_calls_update_treeview_if_nonce_valid(self):
        target_payload_dict = dict()
        argspace = types.SimpleNamespace(payload_dict=target_payload_dict)
        payload = dict(nonce_valid=True,
                       argnamespace=argspace)
        target = self.x.update_sent_messages_treeview = MagicMock()
        result = self.x.execute(payload)
        target.assert_called_with()

    def test_execute_launches_user_alert_on_success(self):
        target_payload_dict = dict()
        argspace = types.SimpleNamespace(payload_dict=target_payload_dict)
        payload = dict(nonce_valid=True,
                       argnamespace=argspace)

        target = self.x.message_controller.launch_user_alert = MagicMock()
        result = self.x.execute(payload)
        self.assertTrue(target.called)
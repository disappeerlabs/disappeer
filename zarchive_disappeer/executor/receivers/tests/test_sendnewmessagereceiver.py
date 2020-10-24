"""
sendnewmessagereceiver.py

Test suite for SendNewMessageReceiver class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.executor.receivers import sendnewmessagereceiver
from disappeer.popups import popuplauncher
from disappeer.net.message import messagefactory
from disappeer.net.bases import clientcontroller
import types


class TestImports(unittest.TestCase):

    def test_abstractreceiver(self):
        self.assertEqual(abstractreceiver, sendnewmessagereceiver.abstractreceiver)

    def test_constants(self):
        self.assertEqual(constants, sendnewmessagereceiver.constants)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, sendnewmessagereceiver.popuplauncher)

    def test_messagefactory(self):
        self.assertEqual(messagefactory, sendnewmessagereceiver.messagefactory)

    def test_clientcontroller(self):
        self.assertEqual(clientcontroller, sendnewmessagereceiver.clientcontroller)

    def test_types(self):
        self.assertEqual(types, sendnewmessagereceiver.types)


class TestSendNewMessageReceiver(unittest.TestCase):

    def setUp(self):
        self.payload = dict()
        self.kwargs = {'console_controller': MagicMock(),
                       'tor_datacontext': MagicMock(),
                       'gpg_datacontext': MagicMock(),
                       'root_params': MagicMock()}
        self.x = sendnewmessagereceiver.SendNewMessageReceiver(**self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, sendnewmessagereceiver.SendNewMessageReceiver)
        self.assertIsInstance(self.x, abstractreceiver.AbstractReceiver)

    def test_name_property_set(self):
        name = constants.command_list.Send_New_Message + '_Receiver'
        self.assertEqual(self.x.name, name)

    def test_valid_kwargs_property_set(self):
        target = {'console_controller',
                  'tor_datacontext',
                  'gpg_datacontext',
                  'root_params'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_valid_kwargs_class_attr_equals_instance_attr(self):
        self.assertEqual(self.x.valid_kwarg_keys, sendnewmessagereceiver.SendNewMessageReceiver.kwarg_keys)

    def test_console_controller_get_console_text_calls_method_gets_result(self):
        msg = 'hello world'
        target = self.x.console_controller.get_console_text = MagicMock(return_value=msg)
        result = self.x.console_controller_get_console_text()
        self.assertTrue(target.called)
        self.assertEqual(result, msg)

    @patch('disappeer.popups.popuplauncher.launch_sendmessage_popup')
    def test_launch_send_message_popup(self, popup_func):
        popup_result = 'result'
        popup_func.return_value = popup_result
        data_record = MagicMock()
        console_text = MagicMock()
        result = self.x.launch_send_message_popup(data_record, console_text)
        popup_func.assert_called_with(self.x.root_params.root, data_record, console_text)
        self.assertEqual(result, popup_func.return_value)

    def test_tor_datacontext_get_tor_message_proxy_address_returns_onion_address(self):
        addr = 'xxx.onion'
        target = self.x.tor_datacontext.get_tor_message_proxy_addr = MagicMock(return_value=addr)
        result = self.x.tor_datacontext_get_tor_message_proxy_addr()
        self.assertTrue(target.called)
        self.assertEqual(result, target.return_value)

    def test_tor_datacontext_get_tor_message_proxy_address_returns_false_with_no_onion_address(self):
        addr = 'xxx'
        target = self.x.tor_datacontext.get_tor_message_proxy_addr = MagicMock(return_value=addr)
        result = self.x.tor_datacontext_get_tor_message_proxy_addr()
        self.assertTrue(target.called)
        self.assertIs(result, False)

    @patch('executor.receivers.sendnewmessagereceiver.messagefactory.MessageFactory')
    def test_build_new_message_payload_calls_msg_factory_with_args_calls_build(self, mock_msg_factory):
        tor_addr = 'xxx.onion'
        sub_tor_addr = self.x.tor_datacontext_get_tor_message_proxy_addr = MagicMock(return_value=tor_addr)
        msg = 'hello'
        gpg_pub_key = MagicMock()
        result = self.x.build_new_message_payload_dict(gpg_pub_key, msg)
        mock_msg_factory.assert_called_with(sub_tor_addr.return_value,
                                            self.x.gpg_datacontext.get_home_dir(),
                                            gpg_pub_key,
                                            self.x.gpg_datacontext.get_host_key_fingerprint(),
                                            msg,
                                            self.x.root_params.get_session_passphrase_observable())
        mock_msg_factory().build.assert_called_with()

    @patch('executor.receivers.sendnewmessagereceiver.messagefactory.MessageFactory')
    def test_build_new_message_payload_returns_false_if_tor_onion_address_is_false(self, mock_msg_factory):
        sub_tor_addr = self.x.tor_datacontext_get_tor_message_proxy_addr = MagicMock(return_value=False)
        gpg_pub_key = MagicMock()
        msg = 'hello'
        result = self.x.build_new_message_payload_dict(gpg_pub_key, msg)
        self.assertIs(result, False)

    @patch('executor.receivers.sendnewmessagereceiver.messagefactory.MessageFactory')
    def test_build_new_message_payload_returns_build_result_if_factory_valid(self, mock_msg_factory):
        build_result = dict()
        class MockFactoryValid:
            valid = True
            def build(self):
                return build_result
        mock_msg_factory.return_value = MockFactoryValid()
        tor_addr = 'xxx.onion'
        sub_tor_addr = self.x.tor_datacontext_get_tor_message_proxy_addr = MagicMock(return_value=tor_addr)
        gpg_pub_key = MagicMock()
        msg = 'hello'
        result = self.x.build_new_message_payload_dict(gpg_pub_key, msg)
        self.assertEqual(result, build_result)

    @patch('executor.receivers.sendnewmessagereceiver.messagefactory.MessageFactory')
    def test_build_new_message_payload_returns_false_if_factory_build_false(self, mock_msg_factory):
        build_result = dict()
        class MockFactoryValid:
            valid = False
            error = 'msg'
            def build(self):
                return build_result
        mock_msg_factory.return_value = MockFactoryValid()
        tor_addr = 'xxx.onion'
        sub_tor_addr = self.x.tor_datacontext_get_tor_message_proxy_addr = MagicMock(return_value=tor_addr)
        gpg_pub_key = MagicMock()
        msg = 'hello'
        result = self.x.build_new_message_payload_dict(gpg_pub_key, msg)
        self.assertIs(result, False)

    @patch('executor.receivers.sendnewmessagereceiver.clientcontroller.ClientController')
    def test_start_client_controller_calls_controller_with_args_starts_controller(self, client_controller):
        args = 'xxxxx'
        self.x.start_client_controller(args)
        client_controller.assert_called_with('send_message', args)
        client_controller().start.assert_called_with()

    def test_construct_arg_namespace_returns_namespace(self):
        data_record = MagicMock()
        payload_dict = MagicMock()
        message_text = MagicMock()
        result = self.x.construct_arg_namespace(data_record, payload_dict, message_text)
        argnamespace = types.SimpleNamespace(host=data_record.address_host,
                                             port=int(data_record.address_port),
                                             queue=self.x.root_params.root_queue,
                                             payload_dict=payload_dict,
                                             nonce=payload_dict['nonce'],
                                             command='MSG',
                                             data_record=data_record,
                                             plaintext=message_text)
        self.assertEqual(result, argnamespace)

    @patch('disappeer.popups.popuplauncher.launch_alert_box_popup')
    def test_launch_alert_box_popup(self, popup_func):
        msg = 'msg'
        self.x.launch_alert_log(msg)
        popup_func.assert_called_with(self.x.root_params.root, msg)

    def test_execute_calls_launch_send_message_popup_with_args(self):
        payload = dict(data_record=MagicMock())
        msg = 'hello'
        sub_msg = self.x.console_controller_get_console_text = MagicMock(return_value=msg)
        sub_build = self.x.build_new_message_payload_dict = MagicMock()
        sub_client_controller = self.x.start_client_controller = MagicMock()
        target = self.x.launch_send_message_popup = MagicMock()
        self.x.execute(payload)
        target.assert_called_with(payload['data_record'], sub_msg.return_value)

    def test_execute_returns_false_if_send_message_popup_returns_none(self):
        payload = dict(data_record=MagicMock())
        msg = 'hello'
        sub = self.x.launch_send_message_popup = MagicMock(return_value=None)
        result = self.x.execute(payload)
        self.assertIs(result, False)

    def test_execute_calls_build_payload_with_args(self):
        payload = dict(data_record=MagicMock())
        msg = 'hello'
        sub_msg = self.x.console_controller_get_console_text = MagicMock(return_value=msg)
        popup_mock = self.x.launch_send_message_popup = MagicMock()
        sub_client_controller = self.x.start_client_controller = MagicMock()
        target = self.x.build_new_message_payload_dict = MagicMock()
        self.x.execute(payload)
        target.assert_called_with(payload['data_record'].gpg_pub_key, sub_msg.return_value)

    def test_execute_calls_launch_alert_returns_false_if_build_payload_returns_false(self):
        payload = dict(data_record=MagicMock())
        msg = 'hello'
        sub_msg = self.x.console_controller_get_console_text = MagicMock(return_value=msg)
        popup_mock = self.x.launch_send_message_popup = MagicMock()
        sub_build = self.x.build_new_message_payload_dict = MagicMock(return_value=False)
        target_alert = self.x.launch_alert_log = MagicMock()
        result = self.x.execute(payload)
        self.assertIs(result, False)
        self.assertTrue(target_alert.called)

    def test_execute_calls_construct_arg_namespace_with_args(self):
        payload = dict(data_record=MagicMock())
        msg = 'hello'
        sub_msg = self.x.console_controller_get_console_text = MagicMock(return_value=msg)
        popup_mock = self.x.launch_send_message_popup = MagicMock()
        sub_build = self.x.build_new_message_payload_dict = MagicMock(return_value=dict())
        sub_client_controller = self.x.start_client_controller = MagicMock()
        target = self.x.construct_arg_namespace = MagicMock()
        result = self.x.execute(payload)
        target.assert_called_with(payload['data_record'], sub_build.return_value, sub_msg.return_value)

    def test_execute_calls_start_client_controller_with_argspace(self):
        payload = dict(data_record=MagicMock())
        msg = 'hello'
        sub_msg = self.x.console_controller_get_console_text = MagicMock(return_value=msg)
        popup_mock = self.x.launch_send_message_popup = MagicMock()
        sub_build = self.x.build_new_message_payload_dict = MagicMock(return_value=dict())
        sub_argspace = self.x.construct_arg_namespace = MagicMock(return_value='argspace')
        target = self.x.start_client_controller = MagicMock()
        result = self.x.execute(payload)
        target.assert_called_with(sub_argspace.return_value)




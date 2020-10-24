"""
test_messageserver.py

Test suite for message server module . . .

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net.message import messageserver
import socketserver
import ssl
from disappeer import settings
from disappeer.net.bases import abstractserverfactory
from disappeer.net.contact import contactprotocol
from disappeer.constants import constants


class TestImports(unittest.TestCase):

    def test_socketserver(self):
        self.assertEqual(socketserver, messageserver.socketserver)

    def test_ssl(self):
        self.assertEqual(ssl, messageserver.ssl)

    def test_settings(self):
        self.assertEqual(settings, messageserver.settings)

    def test_abstractserverfactory(self):
        self.assertEqual(abstractserverfactory, messageserver.abstractserverfactory)

    def test_contactprotocol(self):
        self.assertEqual(contactprotocol, messageserver.contactprotocol)

    def test_constants(self):
        self.assertEqual(constants, messageserver.constants)


class TestSSLMessageTCPServer(unittest.TestCase):

    def setUp(self):
        self.server_address = MagicMock()
        self.req_handler_class = MagicMock()
        self.x_class = messageserver.SSLThreadedMessageTCPServer
        self.base_list = self.x_class.__bases__
        messageserver.SSLThreadedMessageTCPServer.server_bind = MagicMock()
        messageserver.SSLThreadedMessageTCPServer.process_request = MagicMock()
        self.x = messageserver.SSLThreadedMessageTCPServer(self.server_address,
                                                           self.req_handler_class)

    def tearDown(self):
        self.x.socket.close()

    def test_class_self(self):
        self.assertEqual(self.x_class, messageserver.SSLThreadedMessageTCPServer)

    def test_threading_mixin_base(self):
        self.assertIn(socketserver.ThreadingMixIn, self.base_list)

    def test_tcpserver_base(self):
        self.assertIn(socketserver.TCPServer, self.base_list)

    def test_allow_reuse_address_true(self):
        self.assertTrue(self.x.allow_reuse_address)

    def test_bind_and_activate_true(self):
        self.assertTrue(self.x.server_bind.called)

    @patch.object(messageserver.ssl, 'wrap_socket')
    @patch.object(messageserver.socketserver.socket.socket, 'accept')
    def test_get_request_method_calls_socket_accept(self, accept, wrap):
        accept.return_value = (0, 1)
        result = self.x.get_request()
        self.assertTrue(accept.called)


class TestSSLMessageRequestHandler(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.client_address = MagicMock()
        self.server = MagicMock()
        self.mocked_contact_protocol = messageserver.contactprotocol.ContactProtocol = MagicMock(spec=contactprotocol.ContactProtocol(self.request))
        self.x = messageserver.SSLMessageRequestHandler(self.request, self.client_address, self.server)

    def test_instance(self):
        self.assertIsInstance(self.x, messageserver.SSLMessageRequestHandler)

    def test_parent_instance(self):
        self.assertIsInstance(self.x, socketserver.BaseRequestHandler)

    def test_handle_method(self):
        check = hasattr(self.x, 'handle')
        self.assertTrue(check)

    def test_setup_method(self):
        check = hasattr(self.x, 'setup')
        self.assertTrue(check)

    def test_setup_sets_protocol(self):
        self.x.setup()
        self.assertIsNotNone(self.x.protocol)

    def test_handle_method_calls_process_incoming(self):
        sub = self.x.set_protocol = MagicMock()
        target = self.x.protocol = MagicMock()
        self.x.protocol.message_string = 'MSG'
        self.x.handle()
        self.assertTrue(target.process_incoming.called)
        target.process_incoming.assert_called_with('MSG')

    def test_handle_method_returns_false_if_process_incoming_returns_false(self):
        sub = self.x.protocol.process_incoming = MagicMock(return_value=False)
        result = self.x.handle()
        self.assertIs(result, False)

    def test_check_dict_keys_returns_true_on_valid_input(self):
        target_list = ['ciphertext', 'nonce']
        valid_dict = dict(ciphertext='',
                          nonce='')
        result = self.x.dict_keys_are_valid(valid_dict)
        self.assertIs(result, True)

    def test_check_dict_keys_returns_false_on_invalid_input(self):
        invalid_dict = dict(xxx='',
                          request_nonce='',
                          response_nonce='')
        result = self.x.dict_keys_are_valid(invalid_dict)
        self.assertIs(result, False)

    def test_check_dict_keys_returns_false_on_bad_input(self):
        bad = 'xxx'
        result = self.x.dict_keys_are_valid(bad)
        self.assertIs(result, False)

    def test_handle_calls_handle_valid_result_if_dict_keys_are_valid_returns_true(self):
        target = self.x.handle_valid_result = MagicMock()
        sub = self.x.dict_keys_are_valid = MagicMock(return_value=True)
        sub1 = self.x.protocol.process_incoming = MagicMock(return_value=dict())
        self.x.handle()
        target.assert_called_with(sub1.return_value)

    def test_handle_valid_result_calls_send_response(self):
        mock_result = dict()
        target = self.x.send_response = MagicMock()
        self.x.handle_valid_result(mock_result)
        target.assert_called_with(mock_result)

    def test_handle_valid_result_calls_put_to_queue(self):
        mock_result = dict()
        target = self.x.put_to_queue = MagicMock()
        sub = self.x.send_response = MagicMock()
        self.x.handle_valid_result(mock_result)
        target.assert_called_with(mock_result)

    def test_build_response_dict_builds_dict(self):
        mock_input = dict(nonce='xxx')
        target = dict(nonce=mock_input['nonce'],
                      desc='ACK')
        result = self.x.build_response_dict(mock_input)
        self.assertEqual(result, target)

    def test_send_response_calls_protocol_send_ack_with_response_dict(self):
        mock_input = dict(nonce='xxx')
        response_dict = self.x.build_response_dict(mock_input)
        target = self.x.protocol = MagicMock()
        self.x.send_response(mock_input)
        target.send_ack.assert_called_with(response_dict)

    def test_put_to_queue_method_adds_desc_with_result_dict_as_payload_for_queue(self):
        payload = dict(one=1)
        target = dict(desc=constants.command_list.Received_New_Message, payload=payload)
        server = self.x.server = MagicMock()
        self.x.put_to_queue(payload)
        server.queue.put.assert_called_with(target)


class TestMessageServerFactory(unittest.TestCase):

    def setUp(self):
        self.queue = MagicMock()
        self.x = messageserver.MessageServerFactory(self.queue)

    def test_instance(self):
        self.assertIsInstance(self.x, messageserver.MessageServerFactory)

    def test_instance_abstractserverfactory(self):
        self.assertIsInstance(self.x, abstractserverfactory.AbstractServerFactory)

    def test_queue_attribute_set(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_name_property(self):
        target = 'Message_Server'
        self.assertEqual(target, self.x.name)
        with self.assertRaises(AttributeError):
            self.x.name = 'ssss'

    def test_host_property(self):
        target = 'localhost'
        self.assertEqual(target, self.x.host)

    def test_port_property(self):
        target = settings.port_message_server
        self.assertEqual(target, self.x.port)

    def test_request_handler_obj_property(self):
        target = messageserver.SSLMessageRequestHandler
        self.assertEqual(target, self.x.request_handler_obj)

    def test_server_obj_property(self):
        target = messageserver.SSLThreadedMessageTCPServer
        self.assertEqual(target, self.x.server_obj)
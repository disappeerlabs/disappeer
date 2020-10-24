"""
test_abstractclient.py

Test suite for the AbstractClient class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
import net.bases.abstractclient as abstractclient
import abc
import types
import socket
import socks


class TestImports(unittest.TestCase):

    def test_abc(self):
        self.assertEqual(abc, abstractclient.abc)

    def test_socket(self):
        self.assertEqual(socket, abstractclient.socket)

    def test_socks(self):
        self.assertEqual(socks, abstractclient.socks)


class MockConcreateAbstractClient(abstractclient.AbstractClient):

    def send(self):
        raise NotImplementedError

    def handle_response(self):
        raise NotImplementedError

    def set_protocol(self):
        raise NotImplementedError

    def wrap_socket(self):
        pass


class TestAbstractClientClassBasics(unittest.TestCase):

    def setUp(self):
        self.name_space_obj = types.SimpleNamespace()
        self.name_space_obj.host = 'host'
        self.name_space_obj.port = 'port'
        self.name_space_obj.payload_dict = dict()
        self.name_space_obj.command = 'command'
        self.name_space_obj.queue = 'queue'
        self.name_space_obj.nonce = 'nonce'
        self.x = MockConcreateAbstractClient(self.name_space_obj)

    def test_instance(self):
        self.assertIsInstance(self.x, abstractclient.AbstractClient)

    def test_metaclass_attribute(self):
        check = hasattr(self.x, '_abc_registry')
        self.assertTrue(check)

    def test_sock_attribute_is_none(self):
        self.assertIsNone(self.x.sock)

    def test_protocol_attribute_is_none(self):
        self.assertIsNone(self.x.protocol)

    def test_error_attribute_is_none(self):
        self.assertIsNone(self.x.error)

    def test_arg_namespace(self):
        self.assertEqual(self.x.argnamespace, self.name_space_obj)

    def test_host_property(self):
        result = self.x.host
        self.assertEqual(result, self.name_space_obj.host)

    def test_port_property(self):
        result = self.x.port
        self.assertEqual(result, self.name_space_obj.port)

    def test_interface_property(self):
        check = (self.x.host, self.x.port)
        result = self.x.interface
        self.assertEqual(check, result)

    def test_queue_property(self):
        self.assertEqual(self.x.queue, self.name_space_obj.queue)

    def test_nonce_property(self):
        self.assertEqual(self.x.nonce, self.name_space_obj.nonce)

    def test_payload_dict_property(self):
        self.assertEqual(self.x.payload_dict, self.name_space_obj.payload_dict)

    def test_command_property(self):
        result = self.x.command
        self.assertEqual(result, self.name_space_obj.command)

    def test_set_protocol_method_raises_notimplemented(self):
        with self.assertRaises(NotImplementedError):
            result = self.x.set_protocol()

    def test_wrap_socket_method_returns_none(self):
        result = self.x.wrap_socket()
        self.assertIsNone(result)

    def test_create_socket_method_returns_socket(self):
        result = self.x.create_socket()
        result.close()
        self.assertIsInstance(result, socket.socket)

    def test_create_socket_family_inet(self):
        result = self.x.create_socket()
        result.close()
        self.assertEqual(result.family, socket.AF_INET)

    @unittest.skip("Must test manually with socks proxy")
    def test_create_socket_sets_reuse_address(self):
        result = self.x.create_socket()
        check = result.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        result.close()
        self.assertEqual(check, 1)

    @unittest.skip("Must test manually with socks proxy")
    def test_create_socket_sets_timeout(self):
        target = 10.0
        result = self.x.create_socket()
        result.close()
        self.assertEqual(result.timeout, target)

    def test_create_socket_sets_sock_attribute(self):
        result = self.x.create_socket()
        self.assertEqual(self.x.sock, result)
        result.close()

    def test_create_socket_is_socks_proxy_socket(self):
        result = self.x.create_socket()
        self.assertIsInstance(result, socks.socksocket)
        target_proxy_args = (2, '127.0.0.1', 9050, True, None, None)
        self.assertEqual(target_proxy_args, result.proxy)
        result.close()

    def test_connect_method_calls_connect(self):
        target = self.x.sock = MagicMock()
        self.x.connect()
        target.connect.assert_called_with(self.x.interface)

    def test_handle_response_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.x.handle_response()

    def test_stop_method_calls_close(self):
        sub = self.x.sock = MagicMock()
        target = self.x.sock.close = MagicMock()
        self.x.stop()
        self.assertTrue(target.called)

    def test_send_method_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.x.send()

    def test_configure_transport_method_calls_create_socket(self):
        sub2 = self.x.set_protocol = MagicMock()
        sub = self.x.connect = MagicMock()
        target = self.x.create_socket = MagicMock()
        self.x.configure_transport()
        target.assert_called_with()

    def test_configure_transport_method_calls_wrap_socket(self):
        sub2 = self.x.set_protocol = MagicMock()
        sub = self.x.connect = MagicMock()
        sub3 = self.x.create_socket = MagicMock()
        target = self.x.wrap_socket = MagicMock()
        self.x.configure_transport()
        target.assert_called_with()

    def test_configure_transport_method_calls_connect(self):
        sub2 = self.x.set_protocol = MagicMock()
        sub1 = self.x.sock = MagicMock()
        sub = self.x.create_socket = MagicMock()
        target = self.x.connect = MagicMock()
        self.x.configure_transport()
        target.assert_called_with()

    def test_configure_transport_method_calls_set_protocol(self):
        sub1 = self.x.sock = MagicMock()
        sub = self.x.create_socket = MagicMock()
        sub2 = self.x.connect = MagicMock()
        target = self.x.set_protocol = MagicMock()
        self.x.configure_transport()
        target.assert_called_with()

    @patch('socks.socksocket')
    def test_configure_transport_method_with_create_socket_error_sets_and_returns_error(self, patched):
        patched.side_effect = socket.error
        sub1 = self.x.connect = MagicMock()
        sub2 = self.x.set_protocol = MagicMock()
        result = self.x.configure_transport()
        sub1.assert_not_called()
        self.assertIsInstance(result, socket.error)
        self.assertIsInstance(self.x.error, socket.error)

    def test_configure_transport_method_with_connect_error_sets_and_returns_error(self):
        sub = self.x.create_socket = MagicMock()
        sub2 = self.x.set_protocol = MagicMock()
        target = self.x.sock = MagicMock()
        final = target.connect.side_effect = ConnectionRefusedError
        result = self.x.configure_transport()
        self.assertIsInstance(result, ConnectionRefusedError)
        self.assertIsInstance(self.x.error, ConnectionRefusedError)
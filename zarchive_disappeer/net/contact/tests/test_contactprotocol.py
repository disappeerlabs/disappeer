"""
test_contactprotocol.py

Test suite for the ContactProtocol class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.net.contact import contactprotocol
from disappeer.net.bases import baseprotocol


class FakeSocket(MagicMock):

    def __init__(self, payload_data):
        super().__init__()
        self.msg = bytes(payload_data, 'utf-8')

    def recv(self, num_bytes):
        target = self.msg[:num_bytes]
        self.msg = self.msg[num_bytes:]
        return target


class TestImports(unittest.TestCase):

    def test_baseprotocol(self):
        self.assertEqual(baseprotocol, contactprotocol.baseprotocol)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.req = 'REQ'
        self.payload = 'Hello World'
        self.socket = FakeSocket(self.payload)
        self.x = contactprotocol.ContactProtocol(self.socket)

    def test_instance(self):
        self.assertIsInstance(self.x, contactprotocol.ContactProtocol)

    def test_baseprotocol_instance(self):
        self.assertIsInstance(self.x, baseprotocol.BaseProtocol)

    def test_sock_attribute_set_on_base_class(self):
        self.assertEqual(self.socket, self.x.sock)

    def test_send_request_method_calls_build_packet(self):
        target = self.x.build_packet = MagicMock(return_value=self.payload)
        sub = self.x.sock = MagicMock()
        sub = self.x.handle_response = MagicMock()
        self.x.send_request(self.payload, self.req)
        target.assert_called_with(self.payload, self.req)

    def test_send_request_method_calls_sendall_on_sock(self):
        sub = self.x.build_packet = MagicMock(return_value=self.payload)
        sub_1 = self.x.handle_response = MagicMock()
        target = self.x.sock = MagicMock()
        self.x.send_request(self.payload, self.req)
        target.sendall.assert_called_with(sub.return_value)

    def test_handle_response_calls_process_incoming_ack(self):
        target = self.x.process_incoming = MagicMock()
        sub = self.x.sock = MagicMock()
        self.x.handle_response()
        target.assert_called_with(self.x.ack_string)

    def test_handle_response_calls_close_on_sock(self):
        sub = self.x.process_incoming = MagicMock()
        target = self.x.sock = MagicMock()
        self.x.handle_response()
        target.close.assert_called_with()

    def test_handle_response_returns_incoming_payload(self):
        sub = self.x.process_incoming = MagicMock(return_value=self.payload)
        sub1 = self.x.sock = MagicMock()
        result = self.x.handle_response()
        self.assertEqual(result, sub.return_value)

    def test_send_ack_method_builds_packet_with_ack_string(self):
        payload_dict = dict()
        target = self.x.build_packet = MagicMock()
        sub = self.x.sock = MagicMock()
        result = self.x.send_ack(payload_dict)
        target.assert_called_with(payload_dict, self.x.ack_string)

    def test_send_ack_method_calls_sock_sendall_with_packet(self):
        sub = self.x.build_packet = MagicMock(return_value=self.payload)
        target = self.x.sock = MagicMock()
        self.x.send_ack(dict())
        target.sendall.assert_called_with(sub.return_value)

    def test_send_ack_method_calls_sock_close(self):
        sub = self.x.build_packet = MagicMock(return_value=self.payload)
        target = self.x.sock = MagicMock()
        self.x.send_ack(dict())
        target.close.assert_called_with()

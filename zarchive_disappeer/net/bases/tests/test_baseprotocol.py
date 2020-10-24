"""
test_baseprotocol.py

Test suite for AbstractProtocol class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.net.bases import baseprotocol
from disappeer.net.bases import packet
import struct


class TestImports(unittest.TestCase):

    def test_packet(self):
        self.assertEqual(packet, baseprotocol.packet)

    def test_struct(self):
        self.assertEqual(struct, baseprotocol.struct)


class FakeSocket(MagicMock):

    def __init__(self, payload_data):
        super().__init__()
        self.msg = bytes(payload_data, 'utf-8')

    def recv(self, num_bytes):
        target = self.msg[:num_bytes]
        self.msg = self.msg[num_bytes:]
        return target


class MockProtocolInstance(baseprotocol.BaseProtocol):
    pass


class SetUpClass(unittest.TestCase):

    def setUp(self):
        self.payload = 'Hello World'
        self.mock_sock = FakeSocket(self.payload)
        self.x = baseprotocol.BaseProtocol(self.mock_sock)


class TestBaseProtocolClassBasics(SetUpClass):

    def test_instance(self):
        self.assertIsInstance(self.x, baseprotocol.BaseProtocol)

    def test_max_message_length_attribute(self):
        target = 65535
        self.assertEqual(baseprotocol.BaseProtocol.max_message_length, target)

    def test_header_attribute(self):
        self.assertEqual(baseprotocol.BaseProtocol.header, packet.Header)

    def test_header_length_attribute(self):
        self.assertEqual(self.x.header_length, packet.Header.length)

    def test_payload_attribute(self):
        self.assertEqual(self.x.payload, packet.Payload)

    def test_sock_attribute(self):
        self.assertEqual(self.x.sock, self.mock_sock)

    def test_ack_attribute(self):
        target = 'ACK'
        self.assertEqual(self.x.ack_string, target)

    def test_request_attribute(self):
        target = 'REQ'
        self.assertEqual(self.x.request_string, target)

    def test_response_attribute(self):
        target = 'RES'
        self.assertEqual(self.x.response_string, target)

    def test_message_attribute(self):
        target = 'MSG'
        self.assertEqual(self.x.message_string, target)

    def test_build_packet_creates_payload_from_dict(self):
        payload_dict = dict(msg='hello world')
        payload = packet.Payload(payload_dict)
        request = 'HEL'
        hard_target = b'\x16\x00\x00\x00HEL{"msg": "hello world"}'
        result = self.x.build_packet(payload_dict, request)
        self.assertEqual(hard_target, result)

    def test_recv_all_method(self):
        input_string = 'hello'
        sock = FakeSocket(input_string)
        result = self.x._recvall(sock, 4)
        self.assertEqual(b'hell', result)

    def test_recv_header_method(self):
        val = '6666'
        sub = self.x._recvall = MagicMock(return_value=val)
        result = self.x.recv_header()
        sub.assert_called_with(self.x.sock, self.x.header_length)
        self.assertEqual(result, val)

    def test_recv_payload_method(self):
        val = '6666'
        sub = self.x._recvall = MagicMock(return_value=val)
        payload_length = 10
        result = self.x.recv_payload(payload_length)
        sub.assert_called_with(self.x.sock, payload_length)
        self.assertEqual(result, val)

    def test_validate_header_valid(self):
        payload_dict = dict(msg='hello')
        output = self.x.build_packet(payload_dict, self.x.request_string)
        check = b'\x10\x00\x00\x00REQ{"msg": "hello"}'
        header_data = b'\x10\x00\x00\x00REQ'
        request_type = 'REQ'
        check = packet.Header.unpack(header_data)
        result = self.x.validate_header(header_data, request_type)
        self.assertEqual(result, check)

    def test_validate_header_BAD_header_data(self):
        header_data = b'efwefwefwef'
        request_type = 'REQ'
        result = self.x.validate_header(header_data, request_type)
        self.assertFalse(result)

    def test_validate_header_not_valid_command_string(self):
        header_data = b'\x10\x00\x00\x00RES'
        request_type = 'REQ'
        result = self.x.validate_header(header_data, request_type)
        self.assertFalse(result)

    def test_validate_header_not_valid_length_val(self):
        header_data = packet.Header.pack(66666, 'REQ')
        request_type = 'REQ'
        result = self.x.validate_header(header_data, request_type)
        self.assertFalse(result)

    def test_process_request_method_calls_header_methods(self):
        target = 'REQ'
        header_return_val = 'rrrr'
        sub1 = self.x.recv_header = MagicMock(return_value=header_return_val)
        sub2 = self.x.validate_header = MagicMock()
        sub3 = self.x._recvall = MagicMock()
        mock_payload = self.x.payload = MagicMock()
        mock_payload_decode_method = self.x.payload.decode = MagicMock()
        result = self.x.process_incoming(target)
        sub1.assert_called_with()
        sub2.assert_called_with(header_return_val, target)

    def test_process_request_method_returns_false_if_header_false(self):
        target = 'REQ'
        header_return_val = False
        sub1 = self.x.recv_header = MagicMock(return_value=header_return_val)
        sub2 = self.x.validate_header = MagicMock(return_value=header_return_val)
        mock_payload = self.x.payload = MagicMock()
        mock_payload_decode_method = self.x.payload.decode = MagicMock()
        result = self.x.process_incoming(target)
        self.assertFalse(result)

    def test_process_request_method_calls_recv_payload_with_header_len(self):
        req_string = 'REQ'
        header_return_val = (10, req_string)
        sub1 = self.x.recv_header = MagicMock(return_value=header_return_val)
        sub2 = self.x.validate_header = MagicMock(return_value=header_return_val)
        sub3 = self.x._recvall = MagicMock()
        mock_payload = self.x.payload = MagicMock()
        mock_payload_decode_method = self.x.payload.decode = MagicMock()
        target = self.x.recv_payload = MagicMock()
        result = self.x.process_incoming(target)
        target.assert_called_with(header_return_val[0])

    def test_process_request_method_calls_payload_decode(self):
        req_string = 'REQ'
        header_return_val = (10, req_string)
        sub1 = self.x.recv_header = MagicMock(return_value=header_return_val)
        sub2 = self.x.validate_header = MagicMock(return_value=header_return_val)
        sub3 = self.x._recvall = MagicMock()
        sub4 = self.x.recv_payload = MagicMock()
        target = self.x.payload = MagicMock()
        final = 'xxx'
        target_decode_method = self.x.payload.decode = MagicMock(return_value=final)
        result = self.x.process_incoming(req_string)
        self.assertEqual(final, target_decode_method.return_value)




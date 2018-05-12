"""
test_packet.py

Test suite for the Packet module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
import net.bases.packet as packet
import struct
import json


class TestImports(unittest.TestCase):

    def test_struct(self):
        self.assertEqual(struct, packet.struct)

    def test_json(self):
        self.assertEqual(json, packet.json)


class TestHeaderClass(unittest.TestCase):

    def setUp(self):
        self.msg_len_val = 456
        self.msg_command_val = 'HEL'
        self.hard_target_bytes_string = b'\xc8\x01\x00\x00HEL'
        self.payload = 'hello world'
        self.target_format_constant = 'I 3s'
        self.class_obj = packet.Header
        self.x = packet.Header()

    def test_instance(self):
        self.assertIsInstance(self.x, packet.Header)

    def test_struct_format_attribute_string_constant(self):
        self.assertEqual(self.target_format_constant, self.class_obj.format_constant)

    def test_length_attribute(self):
        target = 7
        self.assertEqual(target, self.class_obj.length)

    def test_header_struct_attribute(self):
        self.assertIsInstance(self.class_obj.header_struct, struct.Struct)

    def test_pack_class_method_packs_bytes(self):
        result = self.class_obj.pack(self.msg_len_val, self.msg_command_val)
        self.assertEqual(result, self.hard_target_bytes_string)
        self.assertEqual(len(result), len(self.hard_target_bytes_string))

    def test_unpack_class_method_unpacks_bytes(self):
        result = self.class_obj.unpack(self.hard_target_bytes_string)
        result_int = result[0]
        result_string = result[1]
        self.assertEqual(result_int, self.msg_len_val)
        self.assertEqual(result_string, self.msg_command_val)

    def test_build_method_packs_header(self):
        result = self.class_obj.build(self.payload, self.msg_command_val)
        hard_target = b'\x0b\x00\x00\x00HEL'
        self.assertEqual(result, hard_target)


class TestPayloadClass(unittest.TestCase):

    def setUp(self):
        self.data = ['Hello World']
        self.x = packet.Payload(self.data)

    def test_data_attribute(self):
        self.assertEqual(self.data, self.x.data)

    def test_encode_method_encodes_data_as_json_string_bytes(self):
        result = self.x.encode()
        hard_target = b'["Hello World"]'
        self.assertIsNotNone(result)
        self.assertEqual(result, hard_target)

    def test_decode_method_decodes_data_from_bytes_and_json(self):
        hard_target = b'["Hello World"]'
        encoded_payload = packet.Payload(hard_target)
        result = encoded_payload.decode()
        self.assertEqual(result, self.data)


class TestPacketFactoryClass(unittest.TestCase):

    def setUp(self):
        self.data = {'msg': 'Hello World'}
        self.cmd = 'HEL'
        self.payload = packet.Payload(self.data)
        self.x = packet.PacketFactory(self.payload)

    def test_header_attribute(self):
        self.assertEqual(self.x.header, packet.Header)

    def test_payload_attribute(self):
        self.assertEqual(self.x.payload, self.payload)

    def test_build_method(self):
        result = self.x.build(self.cmd)
        hard_target = b'\x16\x00\x00\x00HEL{"msg": "Hello World"}'
        self.assertEqual(result, hard_target)


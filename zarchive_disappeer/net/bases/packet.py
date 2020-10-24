"""
packet.py

Module for packet-related networking classes: Header, Payload, PacketFactory

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import struct
import json


class Header:
    length = 7
    format_constant = 'I 3s'
    header_struct = struct.Struct(format_constant)

    @classmethod
    def pack(cls, msg_len_int, msg_cmd_string):
        msg_cmd_bytes = bytes(msg_cmd_string, 'utf-8')
        packed = cls.header_struct.pack(msg_len_int, msg_cmd_bytes)
        return packed

    @classmethod
    def unpack(cls, packed_bytes):
        unpacked = cls.header_struct.unpack(packed_bytes)
        final = (unpacked[0], unpacked[1].decode('utf-8'))
        return final

    @classmethod
    def build(cls, payload, command_string):
        length_payload = len(payload)
        header = cls.pack(length_payload, command_string)
        return header


class Payload:

    def __init__(self, data):
        self.data = data

    def encode(self):
        encoded = bytes(json.dumps(self.data), 'utf-8')
        return encoded

    def decode(self):
        decoded = self.data.decode('utf-8')
        result = json.loads(decoded)
        return result


class PacketFactory:

    def __init__(self, payload):
        self.header = Header
        self.payload = payload

    def build(self, command_string):
        encoded_payload = self.payload.encode()
        header = self.header.build(encoded_payload, command_string)
        return header + encoded_payload

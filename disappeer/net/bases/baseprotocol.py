"""
baseprotocol.py

BaseProtocol class object to encapsulate protocol networking code . . . 

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.net.bases import packet
import struct


class BaseProtocol:

    max_message_length = 65535
    header = packet.Header
    header_length = header.length
    payload = packet.Payload

    def __init__(self, sock):
        self.sock = sock
        self.ack_string = 'ACK'
        self.request_string = 'REQ'
        self.response_string = 'RES'
        self.message_string = 'MSG'

    def build_packet(self, payload_dict, command_string):
        payload = packet.Payload(payload_dict)
        result = packet.PacketFactory(payload).build(command_string)
        return result

    def _recvall(self, sock, num):
        fragments = []
        while len(b"".join(fragments)) < num:
            current = sock.recv(num - len(b"".join(fragments)))
            if not current:
                break
            fragments.append(current)
        return b"".join(fragments)

    def recv_header(self):
        header_data = self._recvall(self.sock, self.header_length)
        return header_data

    def recv_payload(self, payload_length):
        result = self._recvall(self.sock, payload_length)
        return result

    def validate_header(self, header_data, command_string):
        try:
            unpacked = self.header.unpack(header_data)
        except struct.error:
            return False

        length_val = unpacked[0]
        command_val = unpacked[1]
        if command_val != command_string:
            return False
        elif length_val > self.max_message_length:
            return False
        else:
            return unpacked

    def process_incoming(self, command_string):
        header_data = self.recv_header()
        header = self.validate_header(header_data, command_string)
        if not header:
            return False

        payload_data = self.recv_payload(header[0])
        decoded = self.payload(payload_data).decode()
        return decoded
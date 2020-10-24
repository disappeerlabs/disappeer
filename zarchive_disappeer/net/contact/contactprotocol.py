"""
contactprotocol.py

Module for the ContactProtocol class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.net.bases import baseprotocol


class ContactProtocol(baseprotocol.BaseProtocol):

    def __init__(self, sock):
        super().__init__(sock)

    def send_request(self, payload_dict, command_string):
        packet = self.build_packet(payload_dict, command_string)
        self.sock.sendall(packet)

    def handle_response(self):
        payload = self.process_incoming(self.ack_string)
        self.sock.close()
        return payload

    def send_ack(self, payload_dict):
        packet = self.build_packet(payload_dict, self.ack_string)
        self.sock.sendall(packet)
        self.sock.close()

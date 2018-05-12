"""
messageserver.py

Module for message server related class objects

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import socketserver
import ssl
from disappeer import settings
from disappeer.net.bases import abstractserverfactory
from disappeer.net.contact import contactprotocol
from disappeer.constants import constants


class MessageServerFactory(abstractserverfactory.AbstractServerFactory):

    def __init__(self, queue):
        super().__init__(queue)

    @property
    def name(self):
        return 'Message_Server'

    @property
    def host(self):
        return 'localhost'

    @property
    def port(self):
        return settings.port_message_server

    @property
    def request_handler_obj(self):
        return SSLMessageRequestHandler

    @property
    def server_obj(self):
        return SSLThreadedMessageTCPServer


class SSLMessageRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.protocol = contactprotocol.ContactProtocol(self.request)

    def handle(self):
        result = self.protocol.process_incoming(self.protocol.message_string)
        if result is False:
            return False
        elif self.dict_keys_are_valid(result):
            self.handle_valid_result(result)

    def handle_valid_result(self, result_dict):
        self.send_response(result_dict)
        self.put_to_queue(result_dict)

    def send_response(self, result_dict):
        response_dict = self.build_response_dict(result_dict)
        self.protocol.send_ack(response_dict)

    def put_to_queue(self, result_dict):
        target = dict(desc=constants.command_list.Received_New_Message,
                      payload=result_dict)
        self.server.queue.put(target)

    def build_response_dict(self, result_dict):
        target = dict(nonce=result_dict['nonce'],
                      desc='ACK')
        return target

    def dict_keys_are_valid(self, result_dict):
        target_list = ['ciphertext', 'nonce']
        if all(name in target_list for name in result_dict):
            return True
        else:
            return False


class SSLThreadedMessageTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True



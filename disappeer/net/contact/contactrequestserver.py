"""
contactrequestserver.py

Module for classes related to contact request server

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import socketserver
from disappeer.net.bases import abstractserverfactory
from disappeer.net.contact import contactprotocol
from disappeer.net.contact import contactrequestvalidator
from disappeer import settings
from disappeer.constants import constants
command_list = constants.command_list


class ContactRequestServerFactory(abstractserverfactory.AbstractServerFactory):

    def __init__(self, queue):
        super().__init__(queue)

    @property
    def name(self):
        return 'Contact_Request_Server'

    @property
    def host(self):
        return 'localhost'

    @property
    def port(self):
        return settings.port_contact_request_server

    @property
    def request_handler_obj(self):
        return ContactRequestServerRequestHandler

    @property
    def server_obj(self):
        return ThreadedTCPServer


class ContactRequestServerRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.protocol = contactprotocol.ContactProtocol(self.request)

    def handle(self):
        result = self.protocol.process_incoming(self.protocol.request_string)
        if result is False:
            return False
        else:
            self.validate_result(result)

    def validate_result(self, result_dict):
        check = contactrequestvalidator.ContactRequestValidator(result_dict)
        if check.valid:
            self.handle_valid_result(check.result_dict)

    def handle_valid_result(self, result_dict):
        self.send_response(result_dict)
        self.put_to_queue(result_dict)

    def send_response(self, result_dict):
        response_dict = self.build_response_dict(result_dict)
        self.protocol.send_ack(response_dict)

    def put_to_queue(self, result_dict):
        result_dict['desc'] = command_list.New_Contact_Req
        self.server.queue.put(result_dict)

    def build_response_dict(self, result_dict):
        target = dict(gpg_pub_key=self.read_file(settings.gpg_host_pubkey),
                      nonce=result_dict['nonce'],
                      desc='ACK')
        return target

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            result = f.read()
        return result


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

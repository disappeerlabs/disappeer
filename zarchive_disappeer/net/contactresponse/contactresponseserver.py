"""
contactresponseserver.py

Module for class objects related to the ContactRequestServer

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import socketserver
import ssl
from disappeer import settings
from disappeer.net.bases import abstractserverfactory
from disappeer.net.contact import contactprotocol
from disappeer.models.db import dbpendingcontactresponsetable
from disappeer.models.db import dbserversynctable
from disappeer.constants import constants
command_list = constants.command_list


class ContactResponseServerFactory(abstractserverfactory.AbstractServerFactory):

    def __init__(self, queue):
        super().__init__(queue)

    @property
    def name(self):
        return 'Contact_Response_Server'

    @property
    def host(self):
        return 'localhost'

    @property
    def port(self):
        return settings.port_contact_response_server

    @property
    def request_handler_obj(self):
        return SSLContactResponseRequestHandler

    @property
    def server_obj(self):
        return SSLThreadedContactResponseTCPServer


class SSLContactResponseRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.protocol = contactprotocol.ContactProtocol(self.request)
        server_sync_path = self.server.get_sync_db_path()
        self.db_server_sync_table = dbserversynctable.DBServerSyncTable(server_sync_path)

    def handle(self):
        result = self.protocol.process_incoming(self.protocol.response_string)
        if result is False:
            return False
        elif self.is_result_valid(result):
            self.handle_valid_result(result)

    def handle_valid_result(self, result_dict):
        self.send_response(result_dict)
        self.put_to_queue(result_dict)

    def send_response(self, result_dict):
        response_dict = self.build_response_dict(result_dict)
        self.protocol.send_ack(response_dict)

    def put_to_queue(self, result_dict):
        result_dict['desc'] = command_list.New_Contact_Res
        self.server.queue.put(result_dict)

    def build_response_dict(self, result_dict):
        target = dict(nonce=result_dict['response_nonce'],
                      desc='ACK')
        return target

    def is_result_valid(self, result_dict):
        key_check = self.dict_keys_are_valid(result_dict)
        nonce_check = self.is_nonce_valid(result_dict)
        if all([key_check, nonce_check]):
            return True
        else:
            return False

    def dict_keys_are_valid(self, result_dict):
        target_list = ['ciphertext', 'request_nonce', 'response_nonce']
        if all(name in target_list for name in result_dict):
            return True
        else:
            return False

    def is_nonce_valid(self, result_dict):
        try:
            target = result_dict['request_nonce']
        except (KeyError, TypeError) as err:
            return False
        nonce_list = self.db_server_sync_table.fetch_all_nonces()
        if target in nonce_list:
            return True
        else:
            return False


class SSLThreadedContactResponseTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

    @classmethod
    def get_sync_db_path(cls):
        """
        This method must be overridden by caller, and patched with the proper method to get the current sync db path
        """
        raise NotImplementedError



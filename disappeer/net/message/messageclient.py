"""
messageclient.py

Module for MessageClient class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.net.bases import abstractclient
from disappeer.net.contact import contactprotocol
import tempfile
import ssl
from disappeer.constants import constants


class MessageClient(abstractclient.AbstractClient):

    def __init__(self, argnamespace):
        super().__init__(argnamespace)

    def send(self):
        self.configure_transport()
        if self.error:
            self.report_error()
            return self.error
        else:
            self.protocol.send_request(self.payload_dict, self.command)
            self.handle_response()

    def handle_response(self):
        result = self.protocol.handle_response()
        self.report_result(result)

    def report_result(self, result):
        result_dict = self.build_result_dict(result)
        self.queue.put(result_dict)

    def build_result_dict(self, result):
        try:
            if result['nonce'] == self.nonce:
                nonce_check = True
            else:
                nonce_check = False
        except KeyError:
            nonce_check = False

        # TODO: Is the whole argnamespace required here? Just need datarecord and plaintext, no?
        #   - keeping whole argnamespace might make it easier to resend the message on failure
        result_dict = dict(desc=constants.command_list.Send_New_Message_Client_Res,
                           result=result,
                           nonce=self.nonce,
                           nonce_valid=nonce_check,
                           host=self.host,
                           port=self.port,
                           argnamespace=self.argnamespace)
        return result_dict

    def report_error(self):
        error_dict = self.build_error_dict()
        self.queue.put(error_dict)

    def build_error_dict(self):
        error_dict = dict(desc=constants.command_list.Send_New_Message_Client_Err,
                          error=self.error,
                          host=self.host,
                          port=self.port,
                          nonce=self.nonce,
                          argnamespace=self.argnamespace)
        return error_dict

    def set_protocol(self):
        self.protocol = contactprotocol.ContactProtocol(self.sock)

    def wrap_socket(self):
        pass


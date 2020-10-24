"""
sendnewmessageclientresponsereceiver.py

Module for HandleSendNewMessageClientResponseReceiver class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.utilities.logger import log

command_list = constants.command_list


class SendNewMessageClientResponseReceiver(abstractreceiver.AbstractReceiver):

    kwarg_keys = {'database_facade',
                  'message_controller'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        suffix = '_Receiver'
        return command_list.Send_New_Message_Client_Res + suffix

    @property
    def valid_kwarg_keys(self):
        return self.kwarg_keys

    def execute(self, payload):
        if not self.is_nonce_valid(payload):
            # TODO: alert user with popup?
            msg = "Major error, client found nonce error, but did not return as error"
            log.error(msg)
            return False

        self.insert_sent_message_from_payload_argspace_payload_dict(payload)
        self.update_sent_messages_treeview()

        success_message = 'Message successfully received by peer.'
        self.message_controller.launch_user_alert(success_message)

    def is_nonce_valid(self, payload):
        if payload['nonce_valid']:
            return True
        else:
            return False

    def insert_sent_message_from_payload_argspace_payload_dict(self, payload):
        argnamespace = payload['argnamespace']
        payload_dict = argnamespace.payload_dict
        self.database_facade.insert_sent_message(payload_dict)

    def update_sent_messages_treeview(self):
        self.message_controller.update_sent_messages_treeview()

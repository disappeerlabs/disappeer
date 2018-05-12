"""
newcontactresponseclientresreceiver.py

Module for command pattern receiver object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.utilities.logger import log

command_list = constants.command_list


class NewContactResponseClientResponseReceiver(abstractreceiver.AbstractReceiver):

    kwarg_keys = {'database_facade',
                  'gpg_datacontext',
                  'requests_controller'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        suffix = 'Receiver'
        return command_list.New_Contact_Res_Client_Res + suffix

    @property
    def valid_kwarg_keys(self):
        return self.kwarg_keys

    def execute(self, payload):
        if not self.is_nonce_valid(payload):
            # TODO: alert user with popup?
            log.warning("Invalid contact request response nonce from remote peer.")
            return False

        gpg_pub_key = self.fetch_contact_request_pubkey_by_nonce(payload)
        if gpg_pub_key is None:
            # TODO: alert user with popup?
            log.warning("GPG Pubkey Not found in database for request response nonce")
            return False

        self.import_gpg_pub_key_to_key_ring(gpg_pub_key)
        self.delete_contact_request_by_gpg_pubkey(gpg_pub_key)
        self.update_received_requests_treeview()

        success_msg = 'Contact Response was received by peer.'
        self.requests_controller.launch_user_alert(success_msg)

    def is_nonce_valid(self, payload):
        if payload['nonce_valid']:
            return True
        else:
            return False

    def fetch_contact_request_pubkey_by_nonce(self, payload):
        nonce = payload['request_nonce']
        result = self.database_facade.fetch_contact_request_pub_key_by_nonce(nonce)
        return result

    def import_gpg_pub_key_to_key_ring(self, pub_key_string):
        self.gpg_datacontext.import_gpg_pub_key_to_key_ring(pub_key_string)
        self.gpg_datacontext.set_key_list()

    def delete_contact_request_by_gpg_pubkey(self, pub_key_string):
        self.database_facade.delete_contact_request_where_x_is_y('gpg_pub_key', pub_key_string)

    def update_received_requests_treeview(self):
        self.requests_controller.update_received_requests_treeview()


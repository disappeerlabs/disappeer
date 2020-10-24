"""
newcontactrequestclientresponsereceiver.py

Module for NewContactRequestClientResponseReceiver class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.gpg.helpers import gpgpubkeyvalidator

from disappeer.utilities.logger import log

command_list = constants.command_list


class NewContactRequestClientResponseReceiver(abstractreceiver.AbstractReceiver):

    kwarg_keys = {'database_facade',
                  'requests_controller'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        suffix = '_Receiver'
        return command_list.New_Contact_Req_Client_Res + suffix

    @property
    def valid_kwarg_keys(self):
        return self.kwarg_keys

    def execute(self, payload):
        if not self.is_nonce_valid(payload):
            # TODO: Should we also alert user with popup?
            log.warning("Invalid contact request response nonce from remote peer.")
            return False

        gpg_pub_key = self.get_gpg_pubkey_from_payload(payload)
        validator = self.validate_pubkey(gpg_pub_key)
        if not validator.valid:
            # TODO: Should we also alert user with popup?
            log.warning("Invalid contact request response pub_key from remote peer.")
            return False
        else:
            payload['fingerprint'] = validator.key_dict['fingerprint']
            self.database_facade.insert_pending_contact_response(payload)
            self.requests_controller.update_sent_requests_treeview()

            success_msg = 'Contact Request was received by peer.'
            self.requests_controller.launch_user_alert(success_msg)

    def is_nonce_valid(self, payload):
        if payload['nonce_valid']:
            return True
        else:
            return False

    def get_gpg_pubkey_from_payload(self, payload):
        pubkey = payload['result']['gpg_pub_key']
        return pubkey

    def validate_pubkey(self, pubkey_string):
        validator = gpgpubkeyvalidator.GPGPubKeyValidator(pubkey_string)
        return validator


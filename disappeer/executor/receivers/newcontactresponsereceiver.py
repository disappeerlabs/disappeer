"""
newcontactresponsereceiver.py

Module for NewContactResponseReceiver class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.net.contactresponse import contactresponsevalidator
from disappeer.gpg.helpers import gpgpubkeyvalidator
from disappeer.popups import popuplauncher
from disappeer.utilities.logger import log
command_list = constants.command_list


class NewContactResponseReceiver(abstractreceiver.AbstractReceiver):

    kwarg_keys = {'database_facade',
                  'gpg_datacontext',
                  'root_params',
                  'message_controller',
                  'requests_controller'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        suffix = '_Receiver'
        return command_list.New_Contact_Res + suffix

    @property
    def valid_kwarg_keys(self):
        return self.kwarg_keys

    def execute(self, payload):
        validator = self.validate_contact_response(payload)
        if not validator.valid:
            msg = "Contact Response Validator returned FALSE: {}".format(validator.error)
            self.launch_alert_log(msg)
            return False
        else:
            self.handle_valid_contact_response(validator.data_dict)

    def handle_valid_contact_response(self, validator_data_dict):
        gpg_pub_key = self.fetch_contact_response_pub_key_by_nonce(validator_data_dict)
        gpg_pub_key_validator = self.validate_pubkey(gpg_pub_key)
        if gpg_pub_key_validator.valid is False:
            # TODO: alert user?
            log.error("Handle Valid Contact Response: SEVERE ERROR, pub key not valid")
            return False

        peer_contact_payload = self.build_peer_contact_payload(gpg_pub_key, gpg_pub_key_validator, validator_data_dict)
        self.database_facade_insert_peer_contact(peer_contact_payload)
        self.import_gpg_pub_key_to_key_ring(gpg_pub_key)
        self.message_controller_update_contacts_treeview()
        self.database_facade_delete_pending_contact_response_by_gpg_fingerprint(gpg_pub_key_validator)
        self.requests_controller_update_sent_requests_treeview()
        self.launch_blink_alert("New Peer Contact")

    def validate_contact_response(self, payload):
        validator = contactresponsevalidator.ContactResponseValidator(payload,
                                                                      self.gpg_datacontext.get_home_dir(),
                                                                      self.database_facade.get_pending_contact_response_table(),
                                                                      self.root_params.get_session_passphrase_observable())
        validator.validate()
        return validator

    def fetch_contact_response_pub_key_by_nonce(self, validator_data_dict):
        request_nonce = validator_data_dict['request_nonce']
        gpg_pub_key = self.database_facade.fetch_contact_response_pub_key_by_nonce(request_nonce)
        return gpg_pub_key

    def validate_pubkey(self, pubkey_string):
        validator = gpgpubkeyvalidator.GPGPubKeyValidator(pubkey_string)
        return validator

    def build_peer_contact_payload(self, gpg_pub_key, gpg_pub_key_validator, contact_response_data_dict):
        target_peer_contact_payload = dict(gpg_pub_key=gpg_pub_key,
                                           gpg_uid=gpg_pub_key_validator.key_dict['uids'][0],
                                           gpg_fingerprint=gpg_pub_key_validator.key_dict['fingerprint'],
                                           address_host=contact_response_data_dict['address_host'],
                                           address_port=contact_response_data_dict['address_port'])
        return target_peer_contact_payload

    def database_facade_insert_peer_contact(self, peer_contact_payload):
        self.database_facade.insert_peer_contact(peer_contact_payload)

    def import_gpg_pub_key_to_key_ring(self, pub_key_string):
        self.gpg_datacontext.import_gpg_pub_key_to_key_ring(pub_key_string)
        self.gpg_datacontext.set_key_list()

    def message_controller_update_contacts_treeview(self):
        self.message_controller.update_contacts_treeview()

    def requests_controller_update_sent_requests_treeview(self):
        self.requests_controller.update_sent_requests_treeview()

    def database_facade_delete_pending_contact_response_by_gpg_fingerprint(self, gpg_pubkey_validator):
        self.database_facade.delete_pending_contact_response_where_x_is_y('gpg_fingerprint', gpg_pubkey_validator.key_dict['fingerprint'])

    def launch_blink_alert(self, msg):
        popuplauncher.launch_blink_alert_popup(self.root_params.root, msg)

    def launch_alert_log(self, msg):
        popuplauncher.launch_alert_box_popup(self.root_params.root, msg)


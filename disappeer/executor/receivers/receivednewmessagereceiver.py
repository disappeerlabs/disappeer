"""
receivednewmessagereceiver.py

Module for ReceivedNewMessageReceiver class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.executor.receivers import abstractreceiver
from disappeer.constants import constants
from disappeer.net.message import messagevalidator
from disappeer.popups import popuplauncher
from disappeer.utilities.logger import log

command_list = constants.command_list


class ReceivedNewMessageReceiver(abstractreceiver.AbstractReceiver):

    kwarg_keys = {'message_controller',
                  'gpg_datacontext',
                  'database_facade',
                  'root_params'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        suffix = '_Receiver'
        return command_list.Received_New_Message + suffix

    @property
    def valid_kwarg_keys(self):
        return self.kwarg_keys

    def execute(self, incoming_payload):
        payload_dict = incoming_payload['payload']
        validator = self.validate_message(payload_dict)
        if validator.valid:
            self.database_facade_insert_received_message(payload_dict)
            self.check_peer_contact_from_new_message(validator.data_dict, validator.verify_result)
            self.message_controller_update_received_messages_treeview()
        else:
            # TODO: decide how to handle this case
            # We fall into this path when:
            #     - remote peer makes contact request
            #     - we accept
            #     - they send us a message and they are added to our peer contacts
            #     - then we delete their peer contact
            #     - and we delete their key from the key ring
            # - alert user
            log.error("Handle received new message payload is NOT valid.")

    def validate_message(self, payload_dict):
        validator = messagevalidator.MessageValidator(payload_dict,
                                                      self.gpg_datacontext.get_home_dir(),
                                                      self.root_params.get_session_passphrase_observable())
        validator.validate()
        return validator

    def database_facade_insert_received_message(self, payload):
        self.database_facade.insert_received_message(payload)

    def database_facade_fetch_peer_contact_by_fingerprint(self, fingerprint):
        peer_result = self.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint(fingerprint)
        return peer_result

    def database_facade_insert_peer_contact(self, new_peer_payload):
        self.database_facade.insert_peer_contact(new_peer_payload)

    def message_controller_update_received_messages_treeview(self):
        self.message_controller.update_received_messages_treeview()

    def message_controller_update_contacts_treeview(self):
        self.message_controller.update_contacts_treeview()

    def gpg_datacontext_get_key_dict_by_identifier(self, fingerprint):
        result = self.gpg_datacontext.get_key_dict_by_identifier(fingerprint)
        return result

    def gpg_datacontext_export_pubkey_from_key_ring(self, fingerprint):
        result = self.gpg_datacontext.export_pubkey_from_key_ring(fingerprint)
        return result

    def build_peer_contact_payload_from_message_validator_results(self, msg_data_dict, verify_result):
        fingerprint = verify_result.fingerprint
        key_dict = self.gpg_datacontext_get_key_dict_by_identifier(fingerprint)
        pub_key = self.gpg_datacontext_export_pubkey_from_key_ring(fingerprint)

        payload = dict(gpg_pub_key=pub_key,
                       gpg_uid=key_dict['uids'][0],
                       gpg_fingerprint=fingerprint,
                       address_host=msg_data_dict['address_host'],
                       address_port=msg_data_dict['address_port'])
        return payload

    def update_peer_contact_record(self, data_dict, peer_record):
        """
        If peer data dict address or port is different from current record, update it
        """
        if data_dict['address_host'] != peer_record.address_host:
            self.database_facade.update_peer_contact_address_from_fingerprint(data_dict['address_host'], peer_record.gpg_fingerprint)
        if data_dict['address_port'] != peer_record.address_port:
            self.database_facade.update_peer_contact_port_from_fingerprint(data_dict['address_port'], peer_record.gpg_fingerprint)

    def check_peer_contact_from_new_message(self, msg_data_dict, msg_verify_result):
        # get fingerprint, check if peer is already saved
        fingerprint = msg_verify_result.fingerprint

        peer_result = self.database_facade_fetch_peer_contact_by_fingerprint(fingerprint)

        if len(peer_result) > 0:
            self.update_peer_contact_record(msg_data_dict, peer_result)
            self.message_controller_update_contacts_treeview()
            return None

        new_peer_payload = self.build_peer_contact_payload_from_message_validator_results(msg_data_dict, msg_verify_result)

        self.database_facade_insert_peer_contact(new_peer_payload)
        self.message_controller_update_contacts_treeview()
        self.launch_blink_alert("New Peer Contact")

    def launch_alert_log(self, msg):
        popuplauncher.launch_alert_box_popup(self.root_params.root, msg)

    def launch_blink_alert(self, msg):
        popuplauncher.launch_blink_alert_popup(self.root_params.root, msg)


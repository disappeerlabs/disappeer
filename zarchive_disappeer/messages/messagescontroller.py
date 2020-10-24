"""
messagescontroller.py

Module for MessagesController class object, controller for MessagesFrame notebook tab GUI view.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.net.message import messagevalidator
from disappeer.popups import popuplauncher
from disappeer.constants import constants
import types
from disappeer.utilities import logger
from disappeer import settings
from disappeer.utilities.logger import log


class MessagesController:

    def __init__(self, root_params, gpg_home_dir_observer):
        self.root_params = root_params
        self.root = self.root_params.root
        self.view = self.root_params.get_messages_frame()
        self.root_queue = self.root_params.root_queue
        self.database_facade = self.root_params.database_facade
        self.gpg_home_dir_observer = gpg_home_dir_observer
        self.config_event_bindings()
        self.update_all_treeviews()
        self.current_treeview_item = None

    def config_event_bindings(self):
        command_button_release_1 = "<ButtonRelease-1>"
        self.view.message_tree_view.bind(command_button_release_1, self.message_treeview_clicked)
        self.view.contacts_tree_view.bind(command_button_release_1, self.peer_contacts_treeview_clicked)

    def update_received_messages_treeview(self):
        results = self.database_facade.fetch_all_received_message_nonces_with_status()
        self.view.update_message_tree_view_received(results)

    def update_sent_messages_treeview(self):
        results = self.database_facade.fetch_all_sent_message_nonces()
        self.view.update_message_tree_view_sent(results)

    def update_all_treeviews(self):
        self.update_received_messages_treeview()
        self.update_sent_messages_treeview()
        self.update_contacts_treeview()

    def message_treeview_clicked(self, event):
        result = self.view.get_clicked_treeview_item_parent_nonce_and_iid()

        if result is None:
            return None
        self.current_treeview_item = result
        parent = result[0]
        nonce = result[1]
        if parent == 'Received':
            record = self.database_facade.fetch_one_received_message_named_tuple_by_nonce(nonce)
        elif parent == 'Sent':
            record = self.database_facade.fetch_one_sent_message_named_tuple_by_nonce(nonce)
        else:
            log.error("Major ERROR: DB parent is not sent or received: {}".format(parent))
            return None
        self.validate_and_view_record(record)

    def validate_and_view_record(self, record_named_tuple):
        payload_dict = record_named_tuple._asdict()
        validator = messagevalidator.MessageValidator(payload_dict, self.gpg_home_dir_observer.get(), self.root_params.get_session_passphrase_observable())
        result = validator.validate()
        if validator.valid:
            from_user = validator.verify_result.username
            fingerprint = validator.verify_result.fingerprint
            message = validator.data_dict['message'].strip()
            final_str = "From: {}\nFingerprint: {}\n**********\n{}".format(from_user, fingerprint, message)
            self.display_record(validator)
        else:
            # TODO: alert User: Can end up in this path if the user does not have passphrase set.
            # - Can end up in this path when the user has deleted the gpg pubkey for the peer who sent this message
            # - Can end up in this path when the key has expired
            # - Change error to warning?
            # Maybe create another popup viewer, to display the gpg warning output:
            #   - a delete button that deletes the record
            #   - a view button that lets you view it
            # Change error to warning?
            log.error("Serious Error: DB message not valid: {}, {}".format(payload_dict['nonce'], validator.error))

    def display_record(self, validator):
        # TODO: add uid FROM and TO info for both SENT and RECEIVED msgs, currently only have fingerprints
        argspace = types.SimpleNamespace()
        argspace.message_type = self.current_treeview_item[0]  # Get this val from the self.current_treeview_item ???
        argspace.message_to = validator.data_dict['sent_to'].strip()
        argspace.message_from = validator.data_dict['sent_from'].strip() # validator.verify_result.username
        argspace.message_text = validator.data_dict['message'].strip()
        result = popuplauncher.launch_displaymessage_popup(self.root, argspace)
        self.handle_display_record_result(result, argspace)

    def handle_display_record_result(self, display_record_result, argspace):
        if display_record_result == 'delete':
            self.view.delete_message_treeview_item_by_iid(self.current_treeview_item[-1])
            if self.current_treeview_item[0] == 'Sent':
                self.database_facade.delete_sent_message_where_x_is_y('nonce', self.current_treeview_item[1])
            else:
                self.database_facade.delete_received_message_where_x_is_y('nonce', self.current_treeview_item[1])
            return None

        if display_record_result == 'inspect':
            self.put_inspect_message_to_queue(argspace)

        # NOTE: THIS IS ONLY UPDATING RECEIVED MESSAGE RECORDS, SINCE THERE IS NO INDICATOR FOR SENT MSGS
        self.view.update_message_tree_view_received_item_as_read(self.current_treeview_item[-1])
        self.database_facade.update_received_message_to_read(self.current_treeview_item[1])

    def update_contacts_treeview(self):
        data_rows = self.database_facade.fetch_all_peer_contact_uids_and_fingerprints_with_status()
        self.view.append_all_to_peer_contacts(data_rows)

    def peer_contacts_treeview_clicked(self, event):
        # Get fingerprint for clicked item
        item_val = self.view.get_clicked_contacts_treeview_contact_id()
        if item_val is None:
            return None

        # Get db record by fingerprint for clicked item
        data_record = self.database_facade.fetch_one_peer_contact_named_tuple_row_by_fingerprint(item_val)
        # Launch popup, display record info
        result = popuplauncher.launch_peercontact_popup(self.root, data_record)

        # update db contact record status to read
        self.database_facade.update_peer_contact_status_to_read(item_val)
        # update the treeview to toggle indicators
        self.update_contacts_treeview()

        if result is None:
            return None
        elif result == 'send':
            self.put_send_new_message_data_record_to_queue(data_record)
        elif result == 'delete':
            self.database_facade.delete_peer_contact_by_fingerprint(item_val)
            self.update_contacts_treeview()
        # TODO: Handle 'invalid' result


    def put_send_new_message_data_record_to_queue(self, data_record):
        data_dict = dict(desc=constants.command_list.Send_New_Message,
                         data_record=data_record)
        self.root_queue.put(data_dict)

    def put_inspect_message_to_queue(self, msg_argspace):
        data_dict = dict(desc=constants.command_list.Inspect_Message,
                         payload=msg_argspace)
        self.root_queue.put(data_dict)

    def launch_user_alert(self, msg):
        popuplauncher.launch_alert_box_popup(self.root, msg)



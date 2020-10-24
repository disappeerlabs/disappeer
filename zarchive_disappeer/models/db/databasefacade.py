"""
databasefacade.py

Module for the DatabaseFacade class object, to hold refs to db tables

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import observable
from disappeer.models.db import dbcontactrequesttable
from disappeer.models.db import dbpendingcontactresponsetable
from disappeer.models.db import dbpeercontactstable
from disappeer.models.db import dbsentmessagestable
from disappeer.models.db import dbreceivedmessagestable
from disappeer.models.db import dbserversynctable
from disappeer import settings


class DatabaseFacade:

    def __init__(self, host_key_observer, get_user_database_dir_method):
        self.host_key_observer = host_key_observer
        self.get_user_database_dir_method = get_user_database_dir_method
        self.contact_request_table = None
        self.pending_contact_response_table = None
        self.peer_contacts_table = None
        self.sent_messages_table = None
        self.received_messages_table = None
        self.server_sync_table = None
        self.config_data_context()
        self.set_db_tables(None)

    ####################
    #  Update Methods  #
    ####################

    def update_contact_request_col_to_val_where_x_is_y(self, target_col, new_val, where_col, where_val):
        self.contact_request_table.update_record_col_to_val_where_x_equals_y(target_col, new_val, where_col, where_val)

    def update_received_message_to_read(self, nonce):
        self.received_messages_table.update_record_status_to_read(nonce)

    def update_peer_contact_address_from_fingerprint(self, new_addr, fingerprint):
        self.peer_contacts_table.update_record_col_to_val_where_x_equals_y('address_host', new_addr, 'gpg_fingerprint', fingerprint)

    def update_peer_contact_port_from_fingerprint(self, new_port, fingerprint):
        self.peer_contacts_table.update_record_col_to_val_where_x_equals_y('address_port', new_port, 'gpg_fingerprint', fingerprint)

    def update_peer_contact_status_to_read(self, fingerprint):
        self.peer_contacts_table.update_record_status_to_read_by_fingerprint(fingerprint)

    ###################
    #  Fetch Methods  #
    ###################

    def fetch_contact_request_pub_key_by_nonce(self, nonce):
        result = self.contact_request_table.fetch_gpg_pub_key_by_nonce(nonce)
        return result

    def fetch_all_contact_request_address_and_nonce(self):
        result = self.contact_request_table.fetch_all_address_and_nonce()
        return result

    def fetch_all_contact_request_address_and_nonce_with_status(self):
        result = self.contact_request_table.fetch_all_address_and_nonce_with_status()
        return result

    def fetch_one_contact_request_by_nonce(self, nonce):
        result = self.contact_request_table.fetch_one_by_nonce(nonce)
        return result

    def fetch_contact_response_pub_key_by_nonce(self, nonce):
        result = self.pending_contact_response_table.fetch_gpg_pub_key_by_nonce(nonce)
        return result

    def fetch_contact_response_pub_key_by_fingerprint(self, fingerprint):
        result = self.pending_contact_response_table.fetch_gpg_pub_key_by_fingerprint(fingerprint)
        return result

    def fetch_all_pending_contact_response_hosts_and_fingerprints(self):
        result = self.pending_contact_response_table.fetch_all_hosts_and_fingerprints()
        return result

    def fetch_peer_contact_tuple_row_by_fingerprint(self, fingerprint):
        result = self.peer_contacts_table.fetch_named_tuple_row_by_fingerprint(fingerprint)
        return result

    def fetch_all_peer_contact_uids_and_fingerprints(self):
        result = self.peer_contacts_table.fetch_all_uids_and_fingerprints()
        return result

    def fetch_all_peer_contact_uids_and_fingerprints_with_status(self):
        result = self.peer_contacts_table.fetch_all_uids_and_fingerprints_and_status()
        return result

    def fetch_one_peer_contact_named_tuple_row_by_fingerprint(self, fingerprint):
        result = self.peer_contacts_table.fetch_named_tuple_row_by_fingerprint(fingerprint)
        return result

    def fetch_all_sent_message_nonces(self):
        result = self.sent_messages_table.fetch_all_nonces()
        return result

    def fetch_one_sent_message_named_tuple_by_nonce(self, nonce):
        result = self.sent_messages_table.fetch_named_tuple_by_nonce(nonce)
        return result

    def fetch_all_received_message_nonces(self):
        result = self.received_messages_table.fetch_all_nonces()
        return result

    def fetch_all_received_message_nonces_with_status(self):
        result = self.received_messages_table.fetch_all_nonces_with_status()
        return result

    def fetch_one_received_message_named_tuple_by_nonce(self, nonce):
        result = self.received_messages_table.fetch_named_tuple_by_nonce(nonce)
        return result

    ###################
    #  Delete Methods #
    ###################

    def delete_contact_request_where_x_is_y(self, x, y):
        self.contact_request_table.delete_record_where_x_equals_y(x, y)

    def delete_pending_contact_response_where_x_is_y(self, x, y):
        self.pending_contact_response_table.delete_record_where_x_equals_y(x, y)
        self.update_server_sync_db()

    def delete_peer_contact_where_x_is_y(self, x, y):
        self.peer_contacts_table.delete_record_where_x_equals_y(x, y)

    def delete_peer_contact_by_fingerprint(self, fingerprint_val):
        self.peer_contacts_table.delete_record_where_x_equals_y('gpg_fingerprint', fingerprint_val)

    def delete_sent_message_where_x_is_y(self, x, y):
        self.sent_messages_table.delete_record_where_x_equals_y(x, y)

    def delete_received_message_where_x_is_y(self, x, y):
        self.received_messages_table.delete_record_where_x_equals_y(x, y)

    ###################
    #  Insert Methods #
    ###################

    def insert_contact_request(self, payload):
        self.contact_request_table.handle_new_payload(payload)

    def insert_pending_contact_response(self, payload):
        self.pending_contact_response_table.handle_new_payload(payload)
        self.update_server_sync_db()

    def insert_peer_contact(self, payload):
        self.peer_contacts_table.handle_new_payload(payload)

    def insert_sent_message(self, payload):
        self.sent_messages_table.handle_new_payload(payload)

    def insert_received_message(self, payload):
        self.received_messages_table.handle_new_payload(payload)

    ###################
    #  CONFIG Methods #
    ###################

    def get_database_dir(self, keyid_name):
        result = self.get_user_database_dir_method(keyid_name)
        return result

    def config_data_context(self):
        self.host_key_observer.add_callback(self.set_db_tables)

    def set_db_tables(self, obs_obj):
        # TODO: if the observer returns the empty key val (i.e. 'No Private Key in Ring'), do not create db tables
        current_path = self.get_full_db_file_path()
        self.contact_request_table = dbcontactrequesttable.DBContactRequestTable(current_path)
        self.pending_contact_response_table = dbpendingcontactresponsetable.DBPendingContactResponseTable(current_path)
        self.peer_contacts_table = dbpeercontactstable.DBPPeerContactsTable(current_path)
        self.sent_messages_table = dbsentmessagestable.DBPSentMessagesTable(current_path)
        self.received_messages_table = dbreceivedmessagestable.DBPReceivedMessagesTable(current_path)
        self.set_server_sync_db_table()

    def get_full_db_file_path(self):
        key_vals = self.host_key_observer.get()
        split = key_vals.split(',')
        key_id = split.pop().strip()
        suffix = '.sqlite'
        file_name = key_id + suffix
        target = self.get_database_dir(key_id) + file_name
        return target

    ###########################
    #  Get Table Ref Methods  #
    ###########################

    def get_pending_contact_response_table(self):
        return self.pending_contact_response_table

    ###########################
    #  Server Sync DB Methods #
    ###########################

    def get_server_sync_db_path(self):
        name = 'server_sync.sqlite'
        key_vals = self.host_key_observer.get()
        split = key_vals.split(',')
        key_id = split.pop().strip()
        target = self.get_database_dir(key_id) + name
        return target

    def set_server_sync_db_table(self):
        self.server_sync_table = dbserversynctable.DBServerSyncTable(self.get_server_sync_db_path())
        self.update_server_sync_db()

    def update_server_sync_db(self):
        self.server_sync_table.delete_all_nonces()
        raw_vals = self.pending_contact_response_table.fetch_all_nonces()
        massaged = [(x,) for x in raw_vals]
        self.server_sync_table.insert_new_vals(massaged)



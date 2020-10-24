"""
dbpeercontactstable.py

Module for DBPeerContactsTable class object, for storing data on successful peer contacts.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.models.db.bases import abstractdbtable


class DBPPeerContactsTable(abstractdbtable.AbstractDBTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'PeerContacts'

    @property
    def data_row_name(self):
        return 'PeerContactsTableRow'

    @property
    def column_names_tuple(self):
        cols = ('gpg_pub_key', 'gpg_uid', 'gpg_fingerprint', 'address_host', 'address_port', 'status')
        return cols

    def build_input_from_payload(self, payload):
        status_val = 'unread'
        target_data_row = (payload['gpg_pub_key'],
                           payload['gpg_uid'],
                           payload['gpg_fingerprint'],
                           payload['address_host'],
                           payload['address_port'],
                           status_val)
        final = self.build_named_tuple(target_data_row)
        return final

    def handle_new_payload(self, payload):
        data_row = self.build_input_from_payload(payload)
        check_for_existing = self.fetch_all_by_fingerprint(data_row.gpg_fingerprint)
        if len(check_for_existing) > 0:
            for row in check_for_existing:
                target_id = row[0]
                self.delete_record_where_x_equals_y('id', target_id)
        self.insert_data_row(data_row)

    def fetch_all_uids_and_fingerprints(self):
        command = 'select {}, {} from {}'.format(self.column_names_tuple[1],
                                                 self.column_names_tuple[2],
                                                 self.table_name)
        result = self.fetch_all(command)
        return result

    def fetch_all_by_fingerprint(self, fingerprint):
        command = "select * from {} where gpg_fingerprint='{}'".format(self.table_name, fingerprint)
        result = self.fetch_all(command)
        return result

    def fetch_named_tuple_row_by_fingerprint(self, fingerprint):
        raw_row = self.fetch_all_by_fingerprint(fingerprint)
        if len(raw_row) == 0:
            return raw_row
        else:
            final = self.build_named_tuple(raw_row[0][1:])
            return final

    def update_record_status_to_read_by_fingerprint(self, fingerprint):
        new_status_val = 'read'
        self.update_record_col_to_val_where_x_equals_y('status', new_status_val, 'gpg_fingerprint', fingerprint)

    def fetch_all_uids_and_fingerprints_and_status(self):
        command = 'select {}, {}, {} from {}'.format(self.column_names_tuple[1],
                                                     self.column_names_tuple[2],
                                                     self.column_names_tuple[5],
                                                     self.table_name)
        result = self.fetch_all(command)
        return result


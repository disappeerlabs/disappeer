"""
dbpendingcontactresponsetable.py

Module for the DBPendingContactResponseTable.

Stores nonce and gpg_pub_key records that are sent in response to contact requests

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.models.db.bases import abstractdbtable


class DBPendingContactResponseTable(abstractdbtable.AbstractDBTable):
    """
    This table stores data from remote peer responses to ContactRequestClient SENT contact requests.
    """

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'PendingContactResponses'

    @property
    def data_row_name(self):
        return 'PendingContactResponseTableRow'

    @property
    def column_names_tuple(self):
        cols = ('status', 'nonce', 'gpg_pub_key', 'gpg_fingerprint', 'host')
        return cols

    def build_input_from_payload(self, payload):
        status = 'new'
        nonce = payload['result']['nonce']
        gpg_key = payload['result']['gpg_pub_key']
        fingerprint = payload['fingerprint']
        host = payload['host']
        target_data_row = (status, nonce, gpg_key, fingerprint, host)
        final = self.build_named_tuple(target_data_row)
        return final

    def handle_new_payload(self, payload):
        data_row = self.build_input_from_payload(payload)
        self.insert_data_row(data_row)

    def fetch_all_nonces(self):
        command = 'select nonce from {}'.format(self.table_name)
        result = self.fetch_all(command)
        final = [x[0] for x in result]
        return final

    def fetch_gpg_pub_key_by_nonce(self, nonce):
        command = "select gpg_pub_key from {} where nonce='{}'".format(self.table_name, nonce)
        result = self.fetch_one(command)
        if result is None:
            return None
        else:
            final = result[0]
            return final

    def fetch_gpg_pub_key_by_fingerprint(self, fingerprint):
        command = "select gpg_pub_key from {} where gpg_fingerprint='{}'".format(self.table_name, fingerprint)
        result = self.fetch_one(command)
        if result is None:
            return None
        else:
            final = result[0]
            return final

    def fetch_all_hosts_and_fingerprints(self):
        command = "select {}, {} from {}".format(self.column_names_tuple[4],
                                                 self.column_names_tuple[3],
                                                 self.table_name)
        result = self.fetch_all(command)
        return result

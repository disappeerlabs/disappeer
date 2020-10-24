"""
dbcontactrequesttable.py

Module for DBContactRequestTable class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.models.db.bases import abstractdbtable


class DBContactRequestTable(abstractdbtable.AbstractDBTable):
    """
    This table stores data from ContactRequestServer's INCOMING contact requests from remote peers.
    """

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'ContactRequests'

    @property
    def column_names_tuple(self):
        cols = ('status', 'nonce', 'gpg_pub_key', 'address_host', 'address_port', 'sig', 'data')
        return cols

    @property
    def data_row_name(self):
        return 'ContactRequestTableRow'

    def build_input_from_payload(self, payload):
        status = 'unread'
        nonce = payload['data_dict']['nonce']
        gpg_pub_key = payload['data_dict']['gpg_pub_key']
        address_host = payload['data_dict']['address_host']
        address_port = payload['data_dict']['address_port']
        sig = payload['contact_req_dict']['sig']
        data = payload['contact_req_dict']['data']
        data_row = (status,
                    nonce,
                    gpg_pub_key,
                    address_host,
                    address_port,
                    sig,
                    data)

        result = self.build_named_tuple(data_row)
        return result

    def handle_new_payload(self, payload):
        data_row = self.build_input_from_payload(payload)
        self.insert_data_row(data_row)

    def fetch_all_address_and_nonce(self):
        command = 'select {}, {} from {}'.format(self.column_names_tuple[3],
                                                 self.column_names_tuple[1],
                                                 self.table_name)
        result = self.fetch_all(command)
        return result

    def fetch_all_address_and_nonce_with_status(self):
        command = 'select {}, {}, {} from {}'.format(self.column_names_tuple[3],
                                                     self.column_names_tuple[1],
                                                     self.column_names_tuple[0],
                                                     self.table_name)
        result = self.fetch_all(command)
        return result

    def fetch_one_by_nonce(self, nonce):
        command = "select * from {} where nonce='{}'".format(self.table_name, nonce)
        result = self.fetch_one(command)
        final = self.build_named_tuple(result[1:])
        return final

    def fetch_gpg_pub_key_by_nonce(self, nonce):
        command = "select gpg_pub_key from {} where nonce='{}'".format(self.table_name, nonce)
        result = self.fetch_one(command)
        if result is None:
            return None
        else:
            final = result[0]
            return final

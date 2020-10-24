"""
basemessagestable.py

Moduel for BaseMessagesTable class object, to hold methods common to sent and received messages tables.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.models.db.bases import abstractdbtable
import hashlib
import random
import sys


class BaseMessagesTable(abstractdbtable.AbstractDBTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def column_names_tuple(self):
        cols = ('nonce', 'ciphertext', 'status')
        return cols

    def build_input_from_payload(self, payload):
        nonce = self.random_hash()
        ciphertext = payload['ciphertext']
        status = 'unread'
        data_row = (nonce, ciphertext, status)
        result = self.build_named_tuple(data_row)
        return result

    def handle_new_payload(self, payload):
        data_row = self.build_input_from_payload(payload)
        self.insert_data_row(data_row)

    def fetch_all_nonces(self):
        command = 'select {} from {}'.format(self.column_names_tuple[0],
                                                 self.table_name)
        result = self.fetch_all(command)
        return result

    def fetch_all_nonces_with_status(self):
        command = 'select {}, {} from {}'.format(self.column_names_tuple[0],
                                                 self.column_names_tuple[2],
                                                 self.table_name)
        result = self.fetch_all(command)
        return result


    def fetch_named_tuple_by_nonce(self, nonce):
        command = "select * from {} where nonce='{}'".format(self.table_name,
                                                             nonce)
        result = self.fetch_one(command)
        result = self.build_named_tuple(result[1:])
        return result

    def delete_record_by_nonce(self, nonce_val):
        self.delete_record_where_x_equals_y(self.column_names_tuple[0], nonce_val)

    def update_record_status_to_read(self, nonce_val):
        new_status_val = 'read'
        self.update_record_col_to_val_where_x_equals_y('status', new_status_val, 'nonce', nonce_val)

    def hash_message(self, message):
        hasher = hashlib.sha1()
        hasher.update(bytes(message, 'UTF-8'))
        digest = hasher.hexdigest()
        return digest

    def random_hash(self):
        num_str = str(random.randint(0, sys.maxsize))
        result = self.hash_message(num_str)
        return result
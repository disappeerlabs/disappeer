"""
dbserversynctable.py

DBServerSyncTable module for syncing nonce vals to the ContactResponseServer thread.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.models.db.bases import abstractdbtable
import sqlite3


class DBServerSyncTable(abstractdbtable.AbstractDBTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'PendingContactResponseNoncesTable'

    @property
    def data_row_name(self):
        return 'PendingContactResponseNoncesTableRow'

    @property
    def column_names_tuple(self):
        cols = ('value', )
        return cols

    def insert_new_vals(self, val_list):
        """
        :param val_list: [('val1',), ('val2',), ('val3',)]
        """
        # TODO: refactor, execute many method should be pulled up into the db executor class
        execution_string = 'INSERT into {} values(null, ?)'.format(self.table_name)
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.executemany(execution_string, val_list)
        connection.commit()
        connection.close()

    def fetch_all_nonces(self):
        command = 'select value from {}'.format(self.table_name)
        result = self.fetch_all(command)
        final = [x[0] for x in result]
        return final

    def delete_all_nonces(self):
        execution_string = 'delete from {}'.format(self.table_name)
        self.execute(execution_string)


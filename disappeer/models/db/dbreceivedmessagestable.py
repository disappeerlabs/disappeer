"""
dbreceivedmessagestable.py

Module for DBReceivedMessagesTable class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.models.db.bases import basemessagestable


class DBPReceivedMessagesTable(basemessagestable.BaseMessagesTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'ReceivedMessages'

    @property
    def data_row_name(self):
        return 'ReceivedMessagesTableRow'


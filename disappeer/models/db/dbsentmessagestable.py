"""
dbsentmessagestable.py

Module for DBSentMessages class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.models.db.bases import basemessagestable


class DBPSentMessagesTable(basemessagestable.BaseMessagesTable):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)

    @property
    def table_name(self):
        return 'SentMessages'

    @property
    def data_row_name(self):
        return 'SentMessagesTableRow'



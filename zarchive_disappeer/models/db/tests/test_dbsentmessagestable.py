"""
test_dbsentmessagestable.py

Test suite for DBSentMessagesTable class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.models.db import dbsentmessagestable
from disappeer.models.db.bases import abstractdbtable
from disappeer.models.db import dbexecutor
from disappeer.models.db.bases import basemessagestable
import os


class TestImports(unittest.TestCase):

    def test_basemessagestable(self):
        self.assertEqual(basemessagestable, dbsentmessagestable.basemessagestable)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.example_payload_valid = dict(nonce='nonce_string', ciphertext='ciphertext_string')
        self.db_file_path = 'models/db/tests/testdb.sqlite'
        self.x = dbsentmessagestable.DBPSentMessagesTable(self.db_file_path)

    def tearDown(self):
        if os.path.isfile(self.db_file_path):
            os.remove(self.db_file_path)

    def test_instance(self):
        self.assertIsInstance(self.x, dbsentmessagestable.DBPSentMessagesTable)

    def test_instance_basemessagestable(self):
        self.assertIsInstance(self.x, basemessagestable.BaseMessagesTable)

    def test_instance_executor(self):
        self.assertIsInstance(self.x, dbexecutor.DBExecutor)

    def test_instance_abstract_table(self):
        self.assertIsInstance(self.x, abstractdbtable.AbstractDBTable)

    def test_db_executor_database_path_attribute_set(self):
        self.assertEqual(self.x.database, self.db_file_path)

    def test_table_name_class_attribute(self):
        target = 'SentMessages'
        self.assertEqual(self.x.table_name, target)
        with self.assertRaises(AttributeError):
            self.x.table_name = 'hello'

    def test_data_row_name_class_attribute(self):
        target = 'SentMessagesTableRow'
        self.assertEqual(self.x.data_row_name, target)
        with self.assertRaises(AttributeError):
            self.x.data_row_name = 'hello'

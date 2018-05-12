"""
test_checksanityreceiver.py

Test suite for command pattern check sanity receiver module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest

from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.executor.receivers import checksanityreceiver


class TestImports(unittest.TestCase):

    def test_abstractreceiver(self):
        self.assertEqual(abstractreceiver, checksanityreceiver.abstractreceiver)

    def test_constants(self):
        self.assertEqual(constants, checksanityreceiver.constants)


class TestCheckSanityReceiver(unittest.TestCase):

    def setUp(self):
        self.msg = 'hello'
        self.kwargs = dict(message='hello')
        self.x = checksanityreceiver.CheckSanityReceiver()

    def test_Wtf(self):
        pass

    def test_instance(self):
        self.assertIsInstance(self.x, checksanityreceiver.CheckSanityReceiver)
        self.assertIsInstance(self.x, abstractreceiver.AbstractReceiver)

    def test_name_property_set(self):
        name = constants.command_list.Check_Sanity + 'Receiver'
        self.assertEqual(self.x.name, name)

    def test_valid_kwarg_keys_set(self):
        target = set()
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_log_message(self):
        self.x.log_message(self.msg)

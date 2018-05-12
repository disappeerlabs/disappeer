"""
test_checksanitycommand.py

Test suite for command module check sanity command

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock

from disappeer.constants import constants
from disappeer.executor import commands
from disappeer.executor.commands import abstractcommand
from disappeer.executor.commands import checksanitycommand
from disappeer.executor.receivers import checksanityreceiver


class TestImports(unittest.TestCase):

    def test_abstractcommand(self):
        self.assertEqual(abstractcommand, commands.abstractcommand)

    def test_constants(self):
        self.assertEqual(constants, checksanitycommand.constants)


class TestCheckSanityCommand(unittest.TestCase):

    def setUp(self):
        self.receiver = MagicMock(spec=checksanityreceiver.CheckSanityReceiver)
        self.message = 'hello'
        self.kwargs = dict(message=self.message)
        self.x = checksanitycommand.CheckSanity(self.receiver, **self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, checksanitycommand.CheckSanity)
        self.assertIsInstance(self.x, abstractcommand.AbstractCommand)

    def test_name_attr(self):
        self.assertEqual(self.x.name, constants.command_list.Check_Sanity)

    def test_receiver_attr(self):
        self.assertEqual(self.x.receiver, self.receiver)

    def test_valid_kwarg_keys_set(self):
        target = {'message'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_message_attr_set(self):
        self.assertEqual(self.x.message, self.message)

    def test_execute_calls_log_message_on_receiver(self):
        msg = 'hello'
        self.x.execute()
        self.receiver.log_message.assert_called_with(self.x.message)

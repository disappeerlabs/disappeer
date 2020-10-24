"""
test_newcontactresponseclientrescommand.py

Module for command pattern newcontactresponseclientrescommand

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock

from disappeer.constants import constants
from disappeer.executor.commands import abstractcommand
from disappeer.executor.commands import newcontactresponseclientresponsecommand as command
from disappeer.executor.receivers import newcontactresponseclientresponsereceiver as receiver


class TestNewContactResponseClientResponseCommand(unittest.TestCase):

    def setUp(self):
        self.receiver = MagicMock(spec=receiver.NewContactResponseClientResponseReceiver)
        self.payload = dict()
        self.kwargs = dict(payload=self.payload)
        self.x = command.NewContactResponseClientResponseCommand(self.receiver, **self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, command.NewContactResponseClientResponseCommand)
        self.assertIsInstance(self.x, abstractcommand.AbstractCommand)

    def test_name_attr(self):
        self.assertEqual(self.x.name, constants.command_list.New_Contact_Res_Client_Res)

    def test_receiver_attr(self):
        self.assertEqual(self.x.receiver, self.receiver)

    def test_valid_kwarg_keys_set(self):
        target = {'payload'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_execute_calls_execute_on_receiver_with_payload_attr_as_arg(self):
        target = self.x.receiver = MagicMock()
        self.x.execute()
        target.execute.assert_called_with(self.x.payload)

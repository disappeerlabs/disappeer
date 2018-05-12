"""
test_newcontactrequestclientresponsecommand.py

Test suite for the newcontactrequestclientresponsecommand module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock

from disappeer.constants import constants
from disappeer.executor.commands import abstractcommand
from disappeer.executor.commands import newcontactrequestclientresponsecommand as command


class TestNewContactResponseClientResponseCommand(unittest.TestCase):

    def setUp(self):
        self.receiver = MagicMock()
        self.payload = dict()
        self.kwargs = dict(payload=self.payload)
        self.x = command.NewContactRequestClientResponseCommand(self.receiver, **self.kwargs)

    def test_instance(self):
        self.assertIsInstance(self.x, command.NewContactRequestClientResponseCommand)
        self.assertIsInstance(self.x, abstractcommand.AbstractCommand)

    def test_name_attr(self):
        self.assertEqual(self.x.name, constants.command_list.New_Contact_Req_Client_Res)

    def test_receiver_attr(self):
        self.assertEqual(self.x.receiver, self.receiver)

    def test_valid_kwarg_keys_set(self):
        target = {'payload'}
        self.assertEqual(target, self.x.valid_kwarg_keys)

    def test_execute_calls_execute_on_receiver_with_payload_attr_as_arg(self):
        target = self.x.receiver = MagicMock()
        self.x.execute()
        target.execute.assert_called_with(self.x.payload)
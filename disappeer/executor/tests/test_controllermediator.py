"""
test_controllermediator.py

Test suite for the ControllerMediator module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import executor.controllermediator as controllermediator


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.database_facade = MagicMock()
        self.gpg_datacontext = MagicMock()
        self.tor_datacontext = MagicMock()
        self.requests_controller = MagicMock()
        self.message_controller = MagicMock()
        self.console_controller = MagicMock()
        self.root_params = MagicMock()
        self.x = controllermediator.ControllerMediator(self.database_facade,
                                                       self.gpg_datacontext,
                                                       self.tor_datacontext,
                                                       self.requests_controller,
                                                       self.message_controller,
                                                       self.console_controller,
                                                       self.root_params)

    def test_instance(self):
        self.assertIsInstance(self.x, controllermediator.ControllerMediator)

    def test_attributes_set(self):
        self.assertEqual(self.x.database_facade, self.database_facade)
        self.assertEqual(self.x.gpg_datacontext, self.gpg_datacontext)
        self.assertEqual(self.x.tor_datacontext, self.tor_datacontext)
        self.assertEqual(self.x.requests_controller, self.requests_controller)
        self.assertEqual(self.x.message_controller, self.message_controller)
        self.assertEqual(self.x.console_controller, self.console_controller)
        self.assertEqual(self.x.root_params, self.root_params)


"""
test_clientcontroller.py

Test suite for the ClientController class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.net.bases import clientcontroller
from disappeer.net.bases import clientfactory
from disappeer.net.bases import threadmanagers
from types import SimpleNamespace


class TestImports(unittest.TestCase):

    def test_clientfactory(self):
        self.assertEqual(clientfactory, clientcontroller.clientfactory)

    def test_threadmanager(self):
        self.assertEqual(threadmanagers, clientcontroller.threadmanagers)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.client_type = 'contact_request'
        self.argnamespace = SimpleNamespace()
        self.argnamespace.test = 'test'
        self.x = clientcontroller.ClientController(self.client_type, self.argnamespace)

    def test_instance(self):
        self.assertIsInstance(self.x, clientcontroller.ClientController)

    def test_client_factory_attribute_is_factory_instance(self):
        self.assertIsInstance(self.x.client_factory, clientfactory.ClientFactory)

    def test_client_factory_internal_attributes(self):
        self.assertEqual(self.client_type, self.x.client_factory.client_type)
        self.assertEqual(self.argnamespace, self.x.client_factory.argnamespace)

    def test_client_attribute_is_instance_threadmanager(self):
        self.assertIsInstance(self.x.client, threadmanagers.ClientThreadManager)

    def test_start_method_calls_start_on_client_attribute(self):
        target = self.x.client = MagicMock()
        self.x.start()
        self.assertTrue(target.start.called)

    def test_stop_method_calls_stop_on_client_attribute(self):
        target = self.x.client = MagicMock()
        self.x.stop()
        self.assertTrue(target.stop.called)

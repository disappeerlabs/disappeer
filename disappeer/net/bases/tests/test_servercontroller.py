"""
test_servercontroller.py

Test suite for the ServerController class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.net.bases import servercontroller
from disappeer.utilities import observable


class TestImports(unittest.TestCase):

    def test_observable(self):
        self.assertEqual(observable, servercontroller.observable)


class TestServerControllerClassBasics(unittest.TestCase):

    def setUp(self):
        self.queue = MagicMock()
        self.factory = MagicMock()
        self.manager = MagicMock()
        self.x = servercontroller.ServerController(self.queue, self.factory, self.manager)

    def test_instance(self):
        self.assertIsInstance(self.x, servercontroller.ServerController)

    def test_status_attribute_is_observable(self):
        self.assertIsInstance(self.x.status, observable.Observable)

    def test_status_observable_set_false(self):
        check = self.x.status.get()
        self.assertFalse(check)

    def test_queue_attribute_is_queue(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_factory_attribute_is_factory_called_with_queue(self):
        check = self.factory(self.queue)
        self.assertEqual(self.x.factory, check)

    def test_server_attribute_is_manager_called_with_factory(self):
        check = self.manager(self.factory)
        self.assertEqual(self.x.server, check)

    def test_start_method_calls_start_on_server(self):
        self.x.start()
        self.assertTrue(self.x.server.start.called)

    def test_start_method_sets_status_true(self):
        self.x.start()
        self.assertTrue(self.x.status.get())

    def test_stop_method_calls_stop_on_server(self):
        self.x.stop()
        self.assertTrue(self.x.server.stop.called)

    def test_stop_method_sets_status_false(self):
        self.x.stop()
        self.assertFalse(self.x.status.get())

    def test_get_status_method(self):
        target = 'hello'
        self.x.status.set(target)
        check = self.x.get_status()
        self.assertEqual(target, check)

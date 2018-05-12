"""
test_abstractserverfactory.py

Test suite for AbstractServerFactory class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.net.bases import abstractserverfactory
import abc
import queue
from disappeer.constants import constants


class TestImports(unittest.TestCase):

    def test_abc(self):
        self.assertEqual(abc, abstractserverfactory.abc)

    def test_constants(self):
        self.assertEqual(constants, abstractserverfactory.constants)


class MockConcrete(abstractserverfactory.AbstractServerFactory):

    @property
    def name(self):
        return 'name'

    @property
    def host(self):
        return 'host'

    @property
    def port(self):
        return 'port'

    @property
    def request_handler_obj(self):
        return 'request_handler_obj'

    @property
    def server_obj(self):
        return MagicMock


class MockBuildError(abstractserverfactory.AbstractServerFactory):

    @property
    def name(self):
        return 'name'

    @property
    def host(self):
        return 'host'

    @property
    def port(self):
        return 'port'

    @property
    def request_handler_obj(self):
        return 'request_handler_obj'

    @property
    def server_obj(self):
        mock = MagicMock()
        mock.side_effect = OSError
        return mock()


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.q = queue.Queue()
        self.x = MockConcrete(self.q)
        self.mocked = MockConcrete(self.q)

    def test_instance(self):
        self.assertIsInstance(self.x, abstractserverfactory.AbstractServerFactory)

    def test_metaclass_attribute(self):
        check = hasattr(self.x, '_abc_registry')
        self.assertTrue(check)

    def test_name_property(self):
        with self.assertRaises(AttributeError):
            self.x.name = 'sss'

    def test_queue_attribute_set(self):
        self.assertEqual(self.x.queue, self.q)

    def test_host_attribute_not_none(self):
        self.assertIsNotNone(self.x.host)

    def test_port_attribute_not_none(self):
        self.assertIsNotNone(self.x.port)

    def test_concrete_interface_property(self):
        check = (self.mocked.host, self.mocked.port)
        result = self.mocked.interface
        self.assertEqual(result, check)

    def test_request_handler_obj_not_none(self):
        self.assertIsNotNone(self.x.request_handler_obj)

    def test_server_obj_not_none(self):
        self.assertIsNotNone(self.x.server_obj)

    def test_build_method_returns_server_obj(self):
        result = self.mocked.build()
        self.assertIsInstance(result, MagicMock)

    def test_build_method_sets_queue(self):
        result = self.mocked.build()
        self.assertEqual(result.queue, self.mocked.queue)

    def test_build_method_catches_os_error_puts_error_dict_to_queue_returns_none(self):
        error_class = MockBuildError(self.q)
        mock_queue = error_class.queue = MagicMock()
        result = error_class.build()
        self.assertTrue(mock_queue.put.called)
        self.assertIsNone(result)


"""
test_tordatacontext.py

Test suite for TorDataContext module and class object, for holding onion addresses

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.models import tordatacontext
from disappeer.utilities import observable


class TestImports(unittest.TestCase):

    def test_observable(self):
        self.assertEqual(observable, tordatacontext.observable)


class TestClassBasics(unittest.TestCase):

    def mock_tor_keys_dir_method():
        return 'hello'

    def setUp(self):
        self.x = tordatacontext.TorDataContext(self.mock_tor_keys_dir_method)

    def test_instance(self):
        self.assertIsInstance(self.x, tordatacontext.TorDataContext)

    def test_get_user_tor_keys_dir_method_attr_set(self):
        self.assertEqual(self.x.get_user_tor_keys_dir_method, self.mock_tor_keys_dir_method)

    def test_tor_request_proxy_addr_is_observable_set_none(self):
        self.assertIsInstance(self.x.tor_request_proxy_addr, observable.Observable)
        target = 'None...'
        self.assertEqual(target, self.x.tor_request_proxy_addr.get())

    def test_tor_response_proxy_addr_is_observable_set_none(self):
        self.assertIsInstance(self.x.tor_response_proxy_addr, observable.Observable)
        target = 'None...'
        self.assertEqual(target, self.x.tor_response_proxy_addr.get())

    def test_tor_message_proxy_addr_is_observable_set_none(self):
        self.assertIsInstance(self.x.tor_message_proxy_addr, observable.Observable)
        target = 'None...'
        self.assertEqual(target, self.x.tor_message_proxy_addr.get())

    def test_get_tor_request_proxy_addr_gets_addr(self):
        target = 'hello'
        self.x.tor_request_proxy_addr.set(target)
        result = self.x.get_tor_request_proxy_addr()
        self.assertEqual(result, target)

    def test_get_tor_response_proxy_addr_gets_addr(self):
        target = 'hello'
        self.x.tor_response_proxy_addr.set(target)
        result = self.x.get_tor_response_proxy_addr()
        self.assertEqual(result, target)

    def test_get_tor_message_proxy_addr_gets_addr(self):
        target = 'hello'
        self.x.tor_message_proxy_addr.set(target)
        result = self.x.get_tor_message_proxy_addr()
        self.assertEqual(result, target)

    def test_set_tor_request_proxy_addr_sets_addr(self):
        target = 'hello'
        self.x.set_tor_request_proxy_addr(target)
        result = self.x.tor_request_proxy_addr.get()
        self.assertEqual(result, target)

    def test_set_tor_response_proxy_addr_sets_addr(self):
        target = 'hello'
        self.x.set_tor_response_proxy_addr(target)
        result = self.x.tor_response_proxy_addr.get()
        self.assertEqual(result, target)

    def test_set_tor_message_proxy_addr_sets_addr(self):
        target = 'hello'
        self.x.set_tor_message_proxy_addr(target)
        result = self.x.tor_message_proxy_addr.get()
        self.assertEqual(result, target)

    def test_add_tor_request_proxy_addr_observer_adds_observer_to_tor_request_proxy_addr(self):
        sub = MagicMock()
        self.x.add_tor_request_proxy_addr_observer(sub)
        self.assertIn(sub, self.x.tor_request_proxy_addr.observer_list)

    def test_add_tor_response_proxy_addr_observer_adds_observer_to_tor_response_proxy_addr(self):
        sub = MagicMock()
        self.x.add_tor_response_proxy_addr_observer(sub)
        self.assertIn(sub, self.x.tor_response_proxy_addr.observer_list)

    def test_add_tor_message_proxy_addr_observer_adds_observer_to_tor_message_proxy_addr(self):
        sub = MagicMock()
        self.x.add_tor_message_proxy_addr_observer(sub)
        self.assertIn(sub, self.x.tor_message_proxy_addr.observer_list)

    def test_get_user_tor_keys_dir_calls_get_user_tor_keys_dir_method_with_arg(self):
        arg = 'xxx'
        val = 'aaa'
        target = self.x.get_user_tor_keys_dir_method = MagicMock(return_value=val)
        result = self.x.get_user_tor_keys_dir(arg)
        target.assert_called_with(arg)
        self.assertEqual(result, target.return_value)


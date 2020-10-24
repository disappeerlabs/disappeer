"""
test_keylistobservable.py

Test suite for the KeyListObservable module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.utilities import observable
from disappeer.gpg.helpers import keylistobservable
from disappeer.gpg.helpers import keylistformatter
from disappeer.gpg.agents import keyring


class TestImports(unittest.TestCase):

    def test_observable(self):
        self.assertEqual(observable, keylistobservable.observable)

    def test_key_list_formatter(self):
        self.assertEqual(keylistformatter, keylistobservable.keylistformatter)


class TestKeyListObservableBasics(unittest.TestCase):

    def setUp(self):
        self.target = ['alice, <alice@email.com>, 190DB52959AC3560']
        self.home = 'tests/data/keys'
        self.keyring = keyring.KeyRing(self.home)
        self.formatter = keylistformatter.KeyListFormatter()
        self.x = keylistobservable.KeyListObservable(self.keyring)

    def test_instance(self):
        self.assertIsInstance(self.x, keylistobservable.KeyListObservable)

    def test_instance_observable(self):
        self.assertIsInstance(self.x, observable.Observable)

    def test_keyring_arg(self):
        self.assertEqual(self.x.key_ring, self.keyring)

    def test_formatter_attribute(self):
        self.assertIsInstance(self.x.key_formatter, keylistformatter.KeyListFormatter)

    def test_keylist_attribute(self):
        name = 'key_list'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_get_method(self):
        result = self.x.get()
        self.assertEqual(result, self.x.key_list)

    def test_set_method_calls_formatter(self):
        self.x.key_formatter.format = MagicMock()
        result = self.x.set(None)
        self.assertTrue(self.x.key_formatter.format.called)

    def test_set_method_calls_run_callbacks(self):
        self.x.run_callbacks = MagicMock()
        result = self.x.set(None)
        self.assertTrue(self.x.run_callbacks.called)

    def test_set_method_sets_key_list_formatted(self):
        result = self.x.set(None)
        for item in self.target:
            self.assertIn(item, self.x.key_list)

    def test_key_list_attribute_set_by_constructor(self):
        for item in self.target:
            self.assertIn(item, self.x.key_list)

    def test_run_method(self):
        result = self.x._run_ops()
        for item in self.target:
            self.assertIn(item, result)

"""
test_hostkeyobservable.py

Test suite for HostKeyObservable module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.utilities import observable
from disappeer.gpg.helpers import hostkeyobservable
from disappeer.gpg.helpers import keylistformatter
from disappeer.gpg.agents import keyring
from disappeer import settings


class TestImports(unittest.TestCase):

    def test_observable(self):
        self.assertEqual(observable, hostkeyobservable.observable)

    def test_key_list_formatter(self):
        self.assertEqual(keylistformatter, hostkeyobservable.keylistformatter)

    def test_settings(self):
        self.assertEqual(settings, hostkeyobservable.settings)


class TestHostKeyObservableBasics(unittest.TestCase):

    def setUp(self):
        self.target = ['alice, <alice@email.com>, 190DB52959AC3560']
        self.home = 'tests/data/keys'
        self.keyring = keyring.KeyRing(self.home)
        self.formatter = keylistformatter.KeyListFormatter()
        self.x = hostkeyobservable.HostKeyObservable(self.keyring)

    def test_instance(self):
        self.assertIsInstance(self.x,  hostkeyobservable.HostKeyObservable)

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
        self.assertEqual(result, self.x.key_list[0])

    def test_get_method_no_keys(self):
        self.x.key_list = []
        result = self.x.get()
        msg = "No Private Key in Ring"
        self.assertEqual(result, msg)

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
        self.assertEqual(self.target, self.x.key_list)

    def test_key_list_attribute_set_by_constructor(self):
        self.assertEqual(self.target, self.x.key_list)

    def test_run_method(self):
        result = self.x._run_ops()
        self.assertEqual(result, self.target)

    def test_get_pub_key_valid_with_valid_key(self):
        targets = ['-----BEGIN PGP PUBLIC KEY BLOCK-----', '-----END PGP PUBLIC KEY BLOCK-----']
        result = self.x.get_pub_key()
        for item in targets:
            self.assertIn(item, result)

    def test_get_pub_key_with_no_key_is_empty_string(self):
        self.x.key_list = []
        result = self.x.get_pub_key()
        self.assertEqual(result, '')

    def test_write_pubkey_to_file_writes_pubkey_to_file(self):
        with open(settings.gpg_host_pubkey, 'w') as f:
            f.write('xxx')
        check = self.x.get_pub_key()
        self.x.write_pub_key_to_file()
        with open(settings.gpg_host_pubkey, 'r') as f:
            result = f.read()
        self.assertEqual(check, result)

    def test_set_method_calls_write_pubkey_to_file_method(self):
        target = self.x.write_pub_key_to_file = MagicMock()
        self.x.set(None)
        target.assert_called_with()

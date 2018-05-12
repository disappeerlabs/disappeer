"""
test_gpgdatacontext.py

Test suite for attempt at GPGDatContext module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.models import gpgdatacontext
from disappeer.utilities import observable
from disappeer import settings
from disappeer.gpg.agents import keyring
from disappeer.gpg.helpers import keylistobservable
from disappeer.gpg.helpers import hostkeyobservable
import copy
import stat
import os


class TestImports(unittest.TestCase):

    def test_observable(self):
        self.assertEqual(observable, gpgdatacontext.observable)

    def test_settings(self):
        self.assertEqual(settings, gpgdatacontext.settings)

    def test_keyring(self):
        self.assertEqual(keyring, gpgdatacontext.keyring)

    def test_keylistobservable(self):
        self.assertEqual(keylistobservable, gpgdatacontext.keylistobservable)

    def test_hostkeyobservable(self):
        self.assertEqual(hostkeyobservable, gpgdatacontext.hostkeyobservable)

    def test_os(self):
        self.assertEqual(os, gpgdatacontext.os)


class GPGDataContextSetupClass(unittest.TestCase):

    key_path = 'tests/data/keys'
    valid_obj = gpgdatacontext.GPGDataContext(key_path)

    def setUp(self):
        self.x = copy.deepcopy(self.valid_obj)


class TestGPGDataContextConfig(GPGDataContextSetupClass):

    def test_instance(self):
        self.assertIsInstance(self.x,  gpgdatacontext.GPGDataContext)

    def test_key_home_path_attribute(self):
        self.assertEqual(self.key_path, self.x.key_home_path)

    def test_home_dir_observable_attribute(self):
        name = 'home_dir_observable'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_config_home_dir_observable_method(self):
        result = self.x.config_home_dir_observable()
        self.assertIsInstance(result, observable.Observable)

    def test_config_home_dir_observable_calls_set_permissions_on_key_path(self):
        target = self.x.set_permissions = MagicMock()
        result = self.x.config_home_dir_observable()
        target.assert_called_with(self.x.key_home_path)

    def test_config_home_dir_observable_method_sets_key_dir(self):
        result = self.x.config_home_dir_observable()
        target = self.x.key_home_path
        check = result.get()
        self.assertEqual(target, check)

    def test_home_dir_attribute_equals_result_config_home_dir_observable(self):
        result = self.x.config_home_dir_observable()
        target = result.get()
        check = self.x.home_dir_observable.get()
        self.assertEqual(target, check)

    def test_key_ring_attribute(self):
        name = 'key_ring'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_config_key_ring_method_return_keyring(self):
        result = self.x.config_key_ring()
        self.assertIsInstance(result, keyring.KeyRing)

    def test_config_key_ring_method_sets_keyring_home(self):
        result = self.x.config_key_ring()
        self.assertEqual(result.home, self.x.home_dir_observable.get())

    def test_config_key_ring_method_adds_keyring_to_homedir_observers(self):
        result = self.x.config_key_ring()
        self.assertIn(result, self.x.home_dir_observable.observer_list)

    def test_config_key_ring_method_resets_home_dir(self):
        self.x.home_dir_observable.set = MagicMock()
        target = self.x.home_dir_observable.set
        result = self.x.config_key_ring()
        self.assertTrue(target.called)

    def test_key_ring_attribute_set_in_constructor(self):
        self.assertIsInstance(self.x.key_ring, keyring.KeyRing)

    def test_key_list_observable_attribute(self):
        name = 'key_list_observable'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_config_key_list_observable_returns_key_list_observable(self):
        result = self.x.config_key_list_observable()
        self.assertIsInstance(result, keylistobservable.KeyListObservable)

    def test_key_list_observable_has_keyring(self):
        result = self.x.config_key_list_observable()
        self.assertIsInstance(result.key_ring, keyring.KeyRing)

    def test_config_key_list_adds_self_to_home_dir_observer_list(self):
        result = self.x.config_key_list_observable()
        self.assertIn(result, self.x.home_dir_observable.observer_list)

    def test_config_key_list_sets_home(self):
        self.x.home_dir_observable.set = MagicMock()
        target = self.x.home_dir_observable.set
        result = self.x.config_key_list_observable()
        self.assertTrue(target.called)

    def test_key_list_attribute_set_in_constructor(self):
        self.assertIsInstance(self.x.key_list_observable, keylistobservable.KeyListObservable)

    def test_host_key_observable_attribute(self):
        name = 'host_key_observable'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_config_host_key_observable_returns_host_key_observable(self):
        result = self.x.config_host_key_observable()
        self.assertIsInstance(result, hostkeyobservable.HostKeyObservable)

    def test_host_key_observable_has_keyring(self):
        result = self.x.config_host_key_observable()
        self.assertIsInstance(result.key_ring, keyring.KeyRing)

    def test_config_host_key_adds_self_to_home_dir_observer_list(self):
        result = self.x.config_host_key_observable()
        self.assertIn(result, self.x.home_dir_observable.observer_list)

    def test_config_host_key_sets_home(self):
        self.x.home_dir_observable.set = MagicMock()
        target = self.x.home_dir_observable.set
        result = self.x.config_host_key_observable()
        self.assertTrue(target.called)

    def test_host_key_attribute_set_in_constructor(self):
        self.assertIsInstance(self.x.host_key_observable, hostkeyobservable.HostKeyObservable)


class TestGPGDataContextMethods(GPGDataContextSetupClass):

    def test_set_home_dir_sets_home_dir(self):
        new_path = 'tests/data/keys'
        self.x.set_home_dir(new_path)
        self.assertEqual(self.x.home_dir_observable.get(), new_path)

    def test_set_home_dir_calls_set_permissions(self):
        new_path = 'tests/data/keys'
        target = self.x.set_permissions = MagicMock()
        self.x.set_home_dir(new_path)
        target.assert_called_with(new_path)

    def test_get_home_dir_returns_home_dir(self):
        result = self.x.get_home_dir()
        self.assertEqual(self.x.home_dir_observable.get(), result)

    def test_add_home_dir_observer_adds_observer_to_home_dir(self):
        sub = MagicMock()
        self.x.add_home_dir_observer(sub)
        self.assertIn(sub, self.x.home_dir_observable.observer_list)

    def test_set_key_list_calls_set_key_list_observable(self):
        sub = self.x.key_list_observable.set = MagicMock()
        self.x.set_key_list()
        sub.assert_called_with(None)

    def test_add_key_list_observer_adds_observer_to_key_list(self):
        sub = MagicMock()
        self.x.add_key_list_observer(sub)
        self.assertIn(sub, self.x.key_list_observable.observer_list)

    def test_add_host_key_observer_adds_observer_to_host_key(self):
        sub = MagicMock()
        self.x.add_host_key_observer(sub)
        self.assertIn(sub, self.x.host_key_observable.observer_list)

    def test_get_raw_key_list_calls_key_ring(self):
        sub = self.x.key_ring.get_raw_key_list = MagicMock()
        result = self.x.get_raw_key_list()
        self.assertTrue(sub.called)

    def test_set_host_key_calls_set_on_host_key_observable(self):
        target = self.x.host_key_observable = MagicMock()
        self.x.set_host_key()
        target.set.assert_called_with(None)

    def test_import_gpg_pub_key_to_key_ring_calls_import_on_key_ring(self):
        pub_key = 'xxxx'
        target = self.x.key_ring = MagicMock()
        self.x.import_gpg_pub_key_to_key_ring(pub_key)
        target.import_key.assert_called_with(pub_key)

    def test_get_host_key_gets_host_key(self):
        val = 'xxxx'
        target = self.x.host_key_observable.get = MagicMock(return_value=val)
        result = self.x.get_host_key()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_get_host_key_id_gets_host_key_id(self):
        val = 'x, y, z'
        target = self.x.host_key_observable.get = MagicMock(return_value=val)
        result = self.x.get_host_key_id()
        self.assertEqual(result, 'z')

    def test_get_pub_key_by_identifier(self):
        val = 'xxxx'
        mock_id = 'aaaaa'
        target = self.x.key_ring.export_key = MagicMock(return_value=val)
        result = self.x.export_pubkey_from_key_ring(mock_id)
        target.assert_called_with(mock_id)
        self.assertEqual(result, target.return_value)

    def test_get_key_dict_by_identifier(self):
        host_key_id = self.x.get_host_key_id()
        result = self.x.get_key_dict_by_identifier(host_key_id)
        self.assertEqual(result['keyid'], host_key_id)

    def test_get_host_key_fingerprint_returns_fingerprint(self):
        keyid = self.x.get_host_key_id()
        key_dict = self.x.get_key_dict_by_identifier(keyid)
        fingerprint = key_dict['fingerprint']
        result = self.x.get_host_key_fingerprint()
        self.assertEqual(result, fingerprint)

    def test_set_permissions_sets(self):
        result = self.x.get_home_dir()
        self.x.set_permissions(result)
        permissions_result = oct(stat.S_IMODE(os.lstat(result).st_mode))
        target_permissions = '0o700'
        self.assertEqual(target_permissions, permissions_result)


class TestGPGDataContextObserverObjects(GPGDataContextSetupClass):

    def test_config_home_dir_observer_returns_observable(self):
        result = self.x.config_home_dir_observer()
        self.assertIsInstance(result, observable.Observable)

    def test_config_home_dir_observer_adds_home_dir_obs_to_home_dir_obs_list(self):
        result = self.x.config_home_dir_observer()
        self.assertIn(result, self.x.home_dir_observable.observer_list)

    def test_config_home_dir_observer_called_by_init_sets_attr(self):
        self.assertIn(self.x.home_dir_observer, self.x.home_dir_observable.observer_list)

    def test_get_home_dir_observer_returns_home_dir_observer_obj(self):
        result = self.x.get_home_dir_observer()
        self.assertEqual(result, self.x.home_dir_observer)

    def test_config_host_key_observer_returns_observable(self):
        result = self.x.config_host_key_observer()
        self.assertIsInstance(result, observable.Observable)

    def test_config_host_key_observer_adds_host_key_obs_to_host_key_observable_list(self):
        result = self.x.config_host_key_observer()
        self.assertIn(result, self.x.host_key_observable.observer_list)

    def test_config_host_key_observer_called_by_init_sets_attr(self):
        self.assertIn(self.x.host_key_observer, self.x.host_key_observable.observer_list)

    def test_get_host_key_observer_returns_host_key_observer_obj(self):
        result = self.x.get_host_key_observer()
        self.assertEqual(result, self.x.host_key_observer)






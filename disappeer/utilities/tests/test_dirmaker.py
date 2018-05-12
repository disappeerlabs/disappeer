"""
test_dirmaker.py

Test suite for the DirMaker module to check and create app data dirs

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import os
from disappeer.utilities import dirmaker
import shutil
import stat
import copy


class TestImports(unittest.TestCase):

    def test_os(self):
        self.assertEqual(os, dirmaker.os)


class TestClassBasics(unittest.TestCase):
    root_dir = "utilities/tests/disapeer/"
    valid_obj = dirmaker.DirMaker(root_dir)

    def setUp(self):
        self.x = copy.deepcopy(self.valid_obj)

    @classmethod
    def tearDownClass(cls):
        cls._delete_root_dir()

    @classmethod
    def _delete_root_dir(cls):
        if os.path.exists(cls.root_dir):
            shutil.rmtree(cls.root_dir)

    def test_instance(self):
        self.assertIsInstance(self.x, dirmaker.DirMaker)

    def test_keys_dir_name_attr(self):
        target = 'keys/'
        self.assertEqual(self.x.keys_dir_name, target)

    def test_data_dir_name_attr(self):
        target = 'data/'
        self.assertEqual(self.x.data_dir_name, target)

    def test_log_dir_name_attr(self):
        target = 'log/'
        self.assertEqual(self.x.log_dir_name, target)

    def test_default_dir_name_attr(self):
        target = 'default/'
        self.assertEqual(self.x.default_dir_name, target)

    def test_tor_keys_dir_name_attr(self):
        target = 'tor_keys/'
        self.assertEqual(self.x.tor_keys_dir_name, target)

    def test_databases_dir_name_attr(self):
        target = 'databases/'
        self.assertEqual(self.x.databases_dir_name, target)

    def test_root_dir_attr(self):
        self.assertEqual(self.x.root_dir, self.root_dir)

    def test_get_root_dir(self):
        result = self.x.get_root_dir()
        self.assertTrue(os.path.exists(self.x.root_dir))
        target = os.path.abspath(self.root_dir) + '/'
        self.assertEqual(result, target)

    def test_create_top_level_called_by_constructor(self):
        self.assertTrue(os.path.exists(self.x.root_dir))
        self.assertTrue(os.path.exists(self.x.root_dir + self.x.keys_dir_name))

    def test_get_key_dir(self):
        target = self.x.root_dir + self.x.keys_dir_name
        result = self.x.get_keys_dir()
        self.assertTrue(os.path.exists(target))
        absolute = os.path.abspath(target) + '/'
        self.assertEqual(result, absolute)

    def test_get_data_dir(self):
        target = self.x.root_dir + self.x.data_dir_name
        result = self.x.get_data_dir()
        self.assertTrue(os.path.exists(target))
        absolute = os.path.abspath(target) + '/'
        self.assertEqual(result, absolute)

    def test_get_log_dir(self):
        target = self.x.root_dir + self.x.log_dir_name
        result = self.x.get_log_dir()
        self.assertTrue(os.path.exists(target))
        absolute = os.path.abspath(target) + '/'
        self.assertEqual(result, absolute)

    def test_create_top_level_dirs(self):
        root = self.x.get_root_dir = MagicMock()
        keys = self.x.get_keys_dir = MagicMock()
        data = self.x.get_data_dir = MagicMock()
        log = self.x.get_log_dir = MagicMock()
        self.x.create_top_level_dirs()
        root.assert_called_with()
        keys.assert_called_with()
        data.assert_called_with()
        log.assert_called_with()

    def test_get_keys_default_dir(self):
        target = self.x.root_dir + self.x.keys_dir_name + self.x.default_dir_name
        result = self.x.get_keys_default_dir()
        self.assertTrue(os.path.exists(target))
        absolute = os.path.abspath(target) + '/'
        self.assertEqual(result, absolute)

    def test_create_data_sub_dirs_creates_all_dirs(self):
        target_name = 'user_keyid'
        self.x.create_data_sub_dirs(target_name)
        first_dir_target = self.x.root_dir + self.x.data_dir_name + target_name
        self.assertTrue(os.path.exists(first_dir_target))
        tor_dir_target = self.x.root_dir + self.x.data_dir_name + target_name + '/' + self.x.tor_keys_dir_name
        self.assertTrue(os.path.exists(tor_dir_target))
        databases_dir_target = self.x.root_dir + self.x.data_dir_name + target_name + '/' + self.x.databases_dir_name
        self.assertTrue(os.path.exists(databases_dir_target))

    def test_create_tor_keys_sub_dir(self):
        super_dir = self.x.root_dir + self.x.data_dir_name + self.x.default_dir_name
        self.x.create_tor_keys_sub_dir(super_dir)
        self.assertTrue(os.path.exists(super_dir + self.x.tor_keys_dir_name))

    def test_create_databases_sub_dir(self):
        super_dir = self.x.root_dir + self.x.data_dir_name + self.x.default_dir_name
        self.x.create_databases_sub_dir(super_dir)
        self.assertTrue(os.path.exists(super_dir + self.x.databases_dir_name))

    def test_set_permissions_sets(self):
        result = self.x.get_keys_default_dir()
        self.x.set_permissions(result)
        permissions_result = oct(stat.S_IMODE(os.lstat(result).st_mode))
        target_permissions = '0o700'
        self.assertEqual(target_permissions, permissions_result)

    def test_create_default_sub_dirs(self):
        target = self.x.create_data_sub_dirs = MagicMock()
        self.x.create_default_sub_dirs()
        target.assert_called_with(self.x.default_dir_name)

    def test_create_user_sub_dirs(self):
        name = 'hello'
        target = self.x.create_data_sub_dirs = MagicMock()
        self.x.create_user_sub_dirs(name)
        target.assert_called_with(name)

    def test_create_default_sub_dirs_called_by_constructor(self):
        data_dir_path = self.x.root_dir + self.x.data_dir_name + self.x.default_dir_name
        self.assertTrue(os.path.exists(data_dir_path))
        key_dir_path = self.x.root_dir + self.x.keys_dir_name + self.x.default_dir_name
        self.assertTrue(os.path.exists(key_dir_path))
        permissions_result = oct(stat.S_IMODE(os.lstat(key_dir_path).st_mode))
        target_permissions = '0o700'
        self.assertEqual(target_permissions, permissions_result)

    def test_get_user_database_dir_creates_returns_new_dir(self):
        new_name = 'new_name_string'
        result = self.x.get_user_database_dir(new_name)
        target = self.x.root_dir + self.x.data_dir_name + new_name + '/' + self.x.databases_dir_name
        self.assertIn(target, result)

    def test_get_user_tor_keys_dir_creates_returns_new_dir(self):
        new_name = 'new_name_string'
        result = self.x.get_user_tor_keys_dir(new_name)
        target = self.x.root_dir + self.x.data_dir_name + new_name + '/' + self.x.tor_keys_dir_name
        self.assertIn(target, result)

    def test_basic(self):
        pass

    def print_tree(self):
        from subprocess import call
        print()
        call(["tree", self.root_dir])


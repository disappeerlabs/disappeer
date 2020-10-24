"""
test_tempkeyring.py

Test suite for TempKeyRing class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.gpg.helpers import tempkeyring
from disappeer.gpg.agents import keyring
import tempfile


class TestImports(unittest.TestCase):

    def test_keyring(self):
        self.assertEqual(keyring, tempkeyring.keyring)

    def test_tempfile(self):
        self.assertEqual(tempfile, tempkeyring.tempfile)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.x = tempkeyring.TempKeyRing()

    def test_instance(self):
        self.assertIsInstance(self.x, tempkeyring.TempKeyRing)

    def test_create_temp_dir_returns_temp_dir(self):
        result = self.x.create_temp_dir()
        self.assertIsInstance(result, tempfile.TemporaryDirectory)
        result.cleanup()

    def test_temp_dir_attribute_is_temp_dir(self):
        self.assertIsInstance(self.x.temp_dir, tempfile.TemporaryDirectory)

    def test_close_temp_dir_calls_close_on_temp_dir(self):
        try:
            self.x.close_temp_dir()
        except:
            self.assertTrue(False)

    def test_close_temp_dir_called_by_del(self):
        target = self.x.close_temp_dir = MagicMock()
        self.x.__del__()
        target.assert_called_with()
        self.x.temp_dir.cleanup()

    def test_temp_dir_name_attribute_is_temp_dir_name(self):
        self.assertEqual(self.x.temp_dir_name, self.x.temp_dir.name)

    def test_key_ring_attribute_is_keyring_with_temp_dir(self):
        self.assertIsInstance(self.x.key_ring, keyring.KeyRing)
        self.assertEqual(self.x.key_ring.home, self.x.temp_dir_name)
"""
test_keydeleter.py

Test suite for KeyDeleter gpgagent module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg.agents import keydeleter
from disappeer.gpg.agents import gpgagent


class TestImports(unittest.TestCase):

    def test_gpgagent(self):
        self.assertEqual(gpgagent, keydeleter.gpgagent)


class TestKeyDeleterClass(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.d = keydeleter.KeyDeleter(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.d, keydeleter.KeyDeleter)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.d, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.d, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.d, name)
        self.assertTrue(check)

    @unittest.skip("Skip key deletion, requires lengthy key creation")
    def test_execute_method(self):
        before = self.d.gpg.list_keys()
        before_len = len(before)
        target = 'EA65A9E6ABC97F54A6E63ACAA8E19FA23E3F1956'
        result = self.d.execute(target)
        after = self.d.gpg.list_keys()
        after_len = len(after)
        self.assertEqual(after_len - before_len, -1)


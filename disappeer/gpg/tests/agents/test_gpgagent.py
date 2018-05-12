"""
test_gpgagent.py

Test suite for gpgagent module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from gpg.agents import gpgagent
import gnupg


class TestImports(unittest.TestCase):

    def test_gnupg(self):
        self.assertEqual(gnupg, gpgagent.gnupg)


class TestAgentClass(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.g = gpgagent.GPGAgent(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.g, gpgagent.GPGAgent)

    def test_keydir_attribute(self):
        self.assertEqual(self.keydir, self.g.home)

    def test_gpg_attribute(self):
        self.assertIsInstance(self.g.gpg, gnupg.GPG)


class TestAgentGetGPGMethod(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.g = gpgagent.GPGAgent(self.keydir)

    def test_get_gpg_obj_result_instance(self):
        result = self.g.get_gpg_obj()
        self.assertIsInstance(result, gnupg.GPG)

    def test_get_gpg_obj_result_home_attr(self):
        result = self.g.get_gpg_obj()
        self.assertEqual(result.gnupghome, self.keydir)

    def test_get_gpg_obj_result_encoding_attr(self):
        result = self.g.get_gpg_obj()
        self.assertEqual(result.encoding, 'utf-8')


class TestAgentSetMethod(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.alt = "tests/data/altkeys"

        self.g = gpgagent.GPGAgent(self.keydir)

    def test_set_method_check_new_home(self):
        self.g.set(self.alt)
        self.assertEqual(self.g.home, self.alt)

    def test_call_instance_check_new_gpg_obj(self):
        self.g.set(self.alt)
        self.assertEqual(self.g.gpg.gnupghome, self.alt)
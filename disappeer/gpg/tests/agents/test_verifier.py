"""
test_verifier.py

Test suite for the Verifier gpg agent module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg.agents import verifier
from disappeer.gpg.agents import gpgagent
from disappeer.gpg.agents import signer


class TestImports(unittest.TestCase):

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, verifier.gpgagent)


class TestVerifierClass(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.key_fingerprint = 'AA74BBFE8A31ADBC0E9ED26B190DB52959AC3560'
        self.v = verifier.Verifier(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.v, verifier.Verifier)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.v, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.v, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.v, name)
        self.assertTrue(check)

    def test_execute_method_valid(self):
        self.message = "Hello world."
        self.passphrase = 'passphrase'
        self.s = signer.Signer(self.keydir)
        sig = self.s.execute(self.message, self.key_fingerprint, self.passphrase)
        result = self.v.execute(str(sig))
        self.assertTrue(result.valid)

    def test_execute_method_not_valid(self):
        self.message = "Hello world."
        result = self.v.execute(self.message)
        self.assertFalse(result.valid)
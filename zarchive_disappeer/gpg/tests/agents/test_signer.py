"""
test_signer.py

Test suite for the Signer module gpg agent class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg.agents import signer
from disappeer.gpg.agents import gpgagent


class TestImports(unittest.TestCase):

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, signer.gpgagent)


class TestSignerClass(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.key_fingerprint = 'AA74BBFE8A31ADBC0E9ED26B190DB52959AC3560'
        self.s = signer.Signer(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.s, signer.Signer)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.s, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.s, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.s, name)
        self.assertTrue(check)

    def test_execute_method_valid(self):
        self.message = "Hello world."
        self.passphrase = 'passphrase'
        result = self.s.execute(self.message, self.key_fingerprint, self.passphrase)
        self.assertIn("SIGNED MESSAGE", str(result))

    @unittest.skip("FAILS ON MAC")
    def test_execute_method_not_valid(self):
        # TODO: This test does not pass on Mac machine, works on Debian
        self.message = "Hello world."
        self.passphrase = 'xxxyyy'
        result = self.s.execute(self.message, self.key_fingerprint, self.passphrase)
        self.assertEqual(0, len(str(result)))

    def test_execute_method_valid_detached(self):
        self.message = "Hello world."
        self.passphrase = 'passphrase'
        result = self.s.execute(self.message,
                                self.key_fingerprint,
                                self.passphrase,
                                detach=True)
        self.assertNotIn(self.message, str(result))


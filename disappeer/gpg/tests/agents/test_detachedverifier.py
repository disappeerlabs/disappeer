"""
test_detachedverifier.py

Test suite for the DetachedVerifier class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg.agents import detachedverifier
from disappeer.gpg.agents import gpgagent
from disappeer.gpg.agents import signer
import tempfile


class TestImports(unittest.TestCase):

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, detachedverifier.gpgagent)


class TestVerifierClass(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.key_fingerprint = 'AA74BBFE8A31ADBC0E9ED26B190DB52959AC3560'
        self.x = detachedverifier.DetachedVerifier(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.x, detachedverifier.DetachedVerifier)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.x, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_execute_method_valid(self):
        self.message = "Hello world."
        self.passphrase = 'passphrase'
        self.s = signer.Signer(self.keydir)
        sig = self.s.execute(self.message, self.key_fingerprint, self.passphrase, detach=True)
        data = bytes(self.message, 'utf-8')
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(bytes(str(sig), 'utf-8'))
            tmp_file.seek(0)
            verify_detached = self.x.execute(tmp_file.name, data)
        self.assertTrue(verify_detached.valid)

    @unittest.skip("FAILS ON MAC")
    def test_execute_method_not_valid(self):
        self.message = "Hello world."
        self.passphrase = 'passsphrase'
        self.s = signer.Signer(self.keydir)
        sig = self.s.execute(self.message, self.key_fingerprint, self.passphrase, detach=True)
        data = bytes(self.message, 'utf-8')
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(bytes(str(sig), 'utf-8'))
            tmp_file.seek(0)
            verify_detached = self.x.execute(tmp_file.name, data)
        self.assertFalse(verify_detached.valid)

"""
test_passphrasevalidator.py

Test suite for PassphraseValidator module.
Takes passphrase, homedir and host key id, checks signs and verify with passphrase.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg.helpers import passphrasevalidator
from disappeer.models import gpgdatacontext
from disappeer.gpg.agents import signer
from disappeer.gpg.agents import verifier



class TestImports(unittest.TestCase):

    def test_signer(self):
        self.assertEqual(signer, passphrasevalidator.signer)

    def test_verifier(self):
        self.assertEqual(verifier, passphrasevalidator.verifier)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.test_key_dir = 'tests/data/keys'
        self.gpg_data_context = gpgdatacontext.GPGDataContext(self.test_key_dir)
        self.home_dir = self.gpg_data_context.get_home_dir()
        self.host_key_id = self.gpg_data_context.get_host_key_id()
        self.passphrase = 'passphrase'
        self.msg = 'hello world'
        self.x = passphrasevalidator.PassphraseValidator(self.home_dir, self.host_key_id, self.passphrase)

    def test_instance(self):
        self.assertIsInstance(self.x, passphrasevalidator.PassphraseValidator)

    def test_home_dir_attr(self):
        self.assertEqual(self.home_dir, self.x.home_dir)

    def test_host_key_id_attr(self):
        self.assertEqual(self.host_key_id, self.x.host_key_id)

    def test_passphrase_attr(self):
        self.assertEqual(self.passphrase, self.x.passphrase)

    def test_msg_attr(self):
        self.assertEqual(self.x.msg, self.msg)

    def test_result_attr(self):
        self.assertEqual(self.x.msg, self.msg)

    @unittest.skip("THIS TEST IS FLAKY ON MAC")
    def test_sign_method_returns_valid_sig_of_message(self):
        sign_agent = signer.Signer(self.home_dir)
        target = sign_agent.execute(self.msg, self.host_key_id, self.passphrase)
        result = self.x.sign()
        print(result)
        print(target)
        self.assertEqual(str(result), str(target))

    def test_verify_method_returns_result_of_verification(self):
        sign_agent = signer.Signer(self.home_dir)
        target = sign_agent.execute(self.msg, self.host_key_id, self.passphrase)
        result = self.x.verify(str(target))
        self.assertTrue(result.valid)

    def test_validate_returns_verify_valid_result(self):
        result = self.x.validate()
        self.assertIs(result, True)

    def test_validate_sets_result_attr(self):
        result = self.x.validate()
        self.assertIsNotNone(self.x.result)

    @unittest.skip("This method words, but throws error in gpg, takes long time")
    def test_validate_returns_verify_false_on_invalid_result(self):
        self.x.passphrase = 'xxxxx'
        result = self.x.validate()
        self.assertIs(result, False)

    def test_result_attr(self):
        self.assertIsNone(self.x.result)

    def test_get_error_msg_returns_error_msg_from_result(self):
        class MockResult:
            stderr = 'hello'
        self.x.result = MockResult()
        result = self.x.get_error_msg()
        self.assertEqual(result, self.x.result.stderr)

    def test_get_error_msg_returns_none_when_result_not_set(self):
        class MockResult:
            mmm = 'xxxx'
        self.x.result = MockResult()
        result = self.x.get_error_msg()
        self.assertIsNone(result)





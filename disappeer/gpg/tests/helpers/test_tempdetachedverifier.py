"""
test_tempdetachedverifier.py

Test suite for TempDetachedVerifier class object and module.
Object should take gpg_pub_key and sig_dict as input.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.gpg.helpers import tempdetachedverifier
from disappeer.gpg.helpers import tempkeyring
from disappeer.gpg.agents import detachedverifier
from disappeer.gpg.agents.signer import Signer
import json
from disappeer.gpg.agents.keyring import KeyRing
import tempfile
import copy


class TestImports(unittest.TestCase):

    def test_tempkeyring(self):
        self.assertEqual(tempkeyring, tempdetachedverifier.tempkeyring)

    def test_detachedverifier(self):
        self.assertEqual(detachedverifier, tempdetachedverifier.detachedverifier)

    def test_tempfile(self):
        self.assertEqual(tempfile, tempdetachedverifier.tempfile)


def build_mock_sig_dict(data_dict):
    encoded_data_dict = json.dumps(data_dict)
    key_dir = 'tests/data/keys'
    signer = Signer(key_dir)
    result = signer.execute(encoded_data_dict, None, 'passphrase', detach=True)
    final_dict = dict(sig=str(result), data=encoded_data_dict)
    return final_dict, result.fingerprint


def get_gpg_pubkey(fingerprint):
    key_dir = 'tests/data/keys'
    key_ring = KeyRing(key_dir)
    result = key_ring.export_key(fingerprint)
    return result


class TestClassBasics(unittest.TestCase):
    """
    Define fixtures as class attributes, then copy valid obj in setup
    """
    data_dict = dict(desc='Hello World')
    sig_dict, fingerprint = build_mock_sig_dict(data_dict)
    gpg_pub_key = get_gpg_pubkey(fingerprint)
    valid_obj = tempdetachedverifier.TempDetachedVerifier(gpg_pub_key, sig_dict)

    def setUp(self):
        self.x = copy.deepcopy(self.valid_obj)

    def test_instance(self):
        self.assertIsInstance(self.x, tempdetachedverifier.TempDetachedVerifier)

    def test_instance_tempkeyring(self):
        self.assertIsInstance(self.x, tempkeyring.TempKeyRing)

    def test_parent_attribute_not_none(self):
        self.assertIsNotNone(self.x.temp_dir)

    def test_gpg_pub_key_attribute_set(self):
        self.assertEqual(self.x.gpg_pub_key, self.gpg_pub_key)

    def test_sig_dict_attribute_set(self):
        self.assertEqual(self.x.sig_dict, self.sig_dict)

    def test_error_attribute_set_none(self):
        self.assertIsNone(self.x.error)

    def test_valid_attribute_set(self):
        check = hasattr(self.x, 'valid')
        self.assertTrue(check)

    def test_detached_verifier_attribute_is_detached_verifier(self):
        self.assertIsInstance(self.x.detached_verifier, detachedverifier.DetachedVerifier)
        self.assertEqual(self.x.detached_verifier.home, self.x.temp_dir_name)

    def test_set_error_method_sets_error_and_valid(self):
        msg = 'Error Message'
        self.x.set_error(msg)
        self.assertEqual(self.x.error, msg)
        self.assertIs(self.x.valid, False)

    def test_is_key_valid_returns_false_sets_error_and_valid_false_on_bad_key(self):
        self.x.gpg_pub_key = 'xxx'
        result = self.x.is_key_valid()
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)
        self.assertIs(result, False)

    def test_is_key_valid_returns_true_on_valid(self):
        result = self.x.is_key_valid()
        self.assertIs(result, True)

    def test_is_sig_dict_valid_returns_true_on_valid_sig_dict(self):
        result = self.x.is_sig_dict_valid()
        self.assertIs(result, True)

    def test_is_sig_dict_valid_returns_false_sets_error_on_invalid_sig_dict(self):
        self.x.sig_dict = 'xxx'
        result = self.x.is_sig_dict_valid()
        self.assertIs(result, False)
        self.assertIsNotNone(self.x.error)

    def test_verify_sig_sets_error_on_invalid_sig(self):
        self.x.sig_dict = dict(sig='xxx', data='yyy')
        result = self.x.verify_sig()
        self.assertIs(result, False)
        self.assertIs(self.x.valid, False)

    def test_verify_sig_returns_valid_on_valid_sig(self):
        self.x.is_key_valid()
        result = self.x.verify_sig()
        self.assertIs(result, True)
        self.assertIs(self.x.valid, True)

    def test_run_method_calls_is_key_valid(self):
        target = self.x.is_key_valid = MagicMock()
        self.x.run()
        target.assert_called_with()

    def test_run_method_calls_is_sig_dict_valid(self):
        target = self.x.is_sig_dict_valid = MagicMock()
        self.x.run()
        target.assert_called_with()

    def test_run_method_calls_verify_sig(self):
        target = self.x.verify_sig = MagicMock()
        self.x.run()
        target.assert_called_with()

    def test_run_does_not_call_is_sig_valid_if_key_not_valid(self):
        self.x.gpg_pub_key = 'xxx'
        target = self.x.is_sig_dict_valid = MagicMock()
        self.x.run()
        self.assertFalse(target.called)

    def test_run_does_not_call_verify_if_sig_dict_not_valid(self):
        self.x.sig_dict = 'xxx'
        target = self.x.verify_sig = MagicMock()
        self.x.run()
        self.assertFalse(target.called)

    def test_run_called_by_init(self):
        self.assertIsNotNone(self.x.valid)


"""
test_contactrequestvalidatory.py

Test suite for the ContactRequestValidator module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.net.contact import contactrequestvalidator
from disappeer.net.contact import contactrequestfactory
from disappeer.gpg.agents import detachedverifier
from disappeer.gpg.agents import keyring
import tempfile
import json
import copy

host_address = '192.168.X.X'
key_dir = 'tests/data/keys'
passphrase = 'passphrase'
factory = contactrequestfactory.ContactRequestFactory(host_address, key_dir, passphrase)
req_dict = factory.build()


class TestImports(unittest.TestCase):

    def test_gpgdetachedverifier(self):
        self.assertEqual(detachedverifier, contactrequestvalidator.detachedverifier)

    def test_gpgkeyring(self):
        self.assertEqual(keyring, contactrequestvalidator.keyring)

    def test_tempfile(self):
        self.assertEqual(tempfile, contactrequestvalidator.tempfile)

    def test_json(self):
        self.assertEqual(json, contactrequestvalidator.json)


class ContactRequestValidatorSetUpClass(unittest.TestCase):

    """
    Creating the object once as a class attribute, than copying it in the setup is much faster than initializing in setup
    """
    valid_obj = contactrequestvalidator.ContactRequestValidator(req_dict)

    def setUp(self):
        self.req_dict_not_valid = dict('')
        self.req_dict_valid = req_dict
        self.x = copy.deepcopy(self.valid_obj)


class TestClassBasics(ContactRequestValidatorSetUpClass):

    def test_instance(self):
        self.assertIsInstance(self.x, contactrequestvalidator.ContactRequestValidator)

    def test_contact_req_dict_attribute_set(self):
        self.assertEqual(self.x.contact_req_dict, self.req_dict_valid)

    def test_check_sig_method_sets_sig_on_valid(self):
        target = self.req_dict_valid['sig']
        self.x.check_sig()
        self.assertEqual(self.x.sig, target)

    def test_check_sig_method_sets_sig_false_on_not_valid(self):
        self.x.contact_req_dict = self.req_dict_not_valid
        self.x.check_sig()
        self.assertFalse(self.x.sig)

    def test_check_data_method_sets_data_on_valid(self):
        target = self.req_dict_valid['data']
        self.x.check_data()
        self.assertEqual(self.x.data, target)

    def test_check_data_method_sets_data_false_on_not_valid(self):
        self.x.contact_req_dict = self.req_dict_not_valid
        self.x.check_data()
        self.assertFalse(self.x.data)

    def test_check_data_dict_method_unloads_valid_json(self):
        target = json.loads(self.req_dict_valid['data'])
        self.x.check_data_dict()
        self.assertEqual(self.x.data_dict, target)

    def test_check_data_dict_method_catches_INvalid_json(self):
        self.x.data = 'xxx'
        self.x.check_data_dict()
        self.assertIs(self.x.data_dict, False)

    def test_check_nonce_method_sets_nonce_on_valid(self):
        target = self.x.data_dict['nonce']
        self.x.check_nonce()
        self.assertEqual(self.x.nonce, target)

    def test_check_nonce_method_sets_nonce_false_on_not_valid(self):
        self.x.data_dict = None
        self.x.check_nonce()
        self.assertIs(self.x.nonce, False)

    def test_run_checks_method_checks_sig_data_data_dict_pub_key_methods(self):
        target_1 = self.x.check_sig = MagicMock()
        target_2 = self.x.check_data = MagicMock()
        target_3 = self.x.check_data_dict = MagicMock()
        target_4 = self.x.check_pub_key = MagicMock()
        target_5 = self.x.check_nonce = MagicMock()
        self.x.run_checks()
        target_1.assert_called_with()
        target_2.assert_called_with()
        target_3.assert_called_with()
        target_4.assert_called_with()
        target_5.assert_called_with()

    def test_run_checks_called_by_init_sig_and_data_attrs_set(self):
        self.assertIsNotNone(self.x.sig)
        self.assertIsNotNone(self.x.data)

    def test_check_pub_key_method(self):
        target = '-----BEGIN PGP PUBLIC KEY BLOCK-----'
        result = self.x.check_pub_key()
        self.assertIn(target, self.x.pub_key)

    def test_validate_sets_error_if_sig_is_false(self):
        self.x.sig = False
        result = self.x.validate()
        self.assertIsNotNone(self.x.error)

    def test_validate_sets_valid_false_if_sig_is_false(self):
        self.x.sig = False
        result = self.x.validate()
        self.assertIs(self.x.valid, False)

    def test_validate_returns_false_if_sig_is_false(self):
        self.x.sig = False
        result = self.x.validate()
        self.assertFalse(result)

    def test_validate_returns_false_if_data_is_false(self):
        self.x.data = False
        result = self.x.validate()
        self.assertFalse(result)

    def test_validate_returns_false_if_data_dict_is_false(self):
        self.x.data_dict = False
        result = self.x.validate()
        self.assertFalse(result)

    def test_validate_returns_false_if_pub_key_is_false(self):
        self.x.pub_key = False
        result = self.x.validate()
        self.assertFalse(result)

    def test_validate_returns_false_on_invalid_pubkey(self):
        self.x.pub_key = 'xxx'
        result = self.x.validate()
        self.assertIs(result, False)

    def test_validate_returns_false_on_invalid_nonce(self):
        self.x.nonce = False
        result = self.x.validate()
        self.assertIs(result, False)

    def test_validate_sets_error_and_valid_false_on_invalid_pubkey(self):
        self.x.pub_key = 'xxx'
        result = self.x.validate()
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)

    def test_validate_returns_valid_result_on_valid_input(self):
        result = self.x.validate()
        self.assertTrue(result.valid)

    def test_validate_sets_valid_attr_true_with_valid_result_on_valid_input(self):
        result = self.x.validate()
        self.assertTrue(self.x.valid)

    def test_validate_returns_INvalid_result_on_INvalid_input(self):
        self.x.data = 'xxx'
        result = self.x.validate()
        self.assertFalse(result.valid)

    def test_validate_returns_sets_error_on_INvalid_input(self):
        self.x.data = 'xxx'
        result = self.x.validate()
        self.assertIsNotNone(self.x.error)

    def test_validate_sets_valid_attr_false_with_INvalid_input(self):
        self.x.data = 'xxx'
        result = self.x.validate()
        self.assertIs(self.x.valid, False)

    def test_catch_type_error_on_bad_input(self):
        bad = '111'
        try:
            target = contactrequestvalidator.ContactRequestValidator(bad)
        except:
            self.assertTrue(False)

    def test_is_data_valid_returns_false_sets_error_and_valid_on_false_sig(self):
        self.x.sig = False
        result = self.x.is_data_valid()
        self.assertIs(result, False)
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)

    def test_is_data_valid_returns_false_sets_error_and_valid_on_false_data(self):
        self.x.data = None
        result = self.x.is_data_valid()
        self.assertIs(result, False)
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)

    def test_is_data_valid_returns_false_sets_error_and_valid_on_false_pub_key(self):
        self.x.pub_key = False
        result = self.x.is_data_valid()
        self.assertIs(result, False)
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)

    def test_is_data_valid_returns_false_sets_error_and_valid_on_false_data_dict(self):
        self.x.data_dict = False
        result = self.x.is_data_valid()
        self.assertIs(result, False)
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)

    def test_is_data_valid_returns_false_sets_error_and_valid_on_false_nonce(self):
        self.x.nonce = False
        result = self.x.is_data_valid()
        self.assertIs(result, False)
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)

    def test_is_key_valid_returns_false_sets_error_and_valid_false_on_bad_key(self):
        self.x.pub_key = 'xxx'
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = self.x.is_key_valid(tmp_dir)
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)

    def test_is_key_valid_sets_key_dict_on_valid(self):
        self.x.is_key_valid(key_dir)
        self.assertIsNotNone(self.x.key_dict)
        self.assertIsInstance(self.x.key_dict, type(dict()))

    def test_verify_sig_method_exists(self):
        name = 'verify_sig'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_validate_calls_verify_sig(self):
        target = self.x.verify_sig = MagicMock()
        self.x.validate()
        self.assertTrue(target.called)

    def test_validate_called_by_constructor(self):
        self.assertIsNotNone(self.x.valid)

    def test_construct_result_dict_constructs_dict_on_valid(self):
        target = dict(contact_req_dict=self.x.contact_req_dict,
                      nonce=self.x.nonce,
                      data_dict=self.x.data_dict)

        result = self.x.construct_result_dict()
        self.assertIsNotNone(self.x.result_dict)
        self.assertEqual(self.x.result_dict, result)

    def test_construct_result_dict_sets_false_on_not_valid(self):
        self.x.valid = False
        result = self.x.construct_result_dict()
        self.assertIs(self.x.result_dict, False)
        self.assertIs(result, False)

    def test_construct_result_dict_called_by_init(self):
        self.assertIsNotNone(self.x.result_dict)

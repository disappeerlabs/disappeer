"""
test_keylistformatter.py

Test suite for KeyListFormatter module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg.helpers import keylistformatter
from disappeer.gpg.agents import keyring

key_dir = 'tests/data/keys'

user_name = 'alice'
user_email = '<alice@email.com>'
user_keyid = '190DB52959AC3560'
user_key_uid_string = 'alice (in wonderland) <alice@email.com>'

key_ring = keyring.KeyRing(key_dir)
raw_key_list = key_ring.get_raw_key_list()


class TestKeyListFormatterBasics(unittest.TestCase):

    def setUp(self):
        self.key_list = raw_key_list
        self.key_uid_string = self.key_list[0]['uids'][0]
        self.x = keylistformatter.KeyListFormatter()

    def test_instance(self):
        self.assertIsInstance(self.x, keylistformatter.KeyListFormatter)

    def test_format_method_attribute(self):
        name = 'format'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_format_method_takes_list_arg(self):
        result = self.x.format(self.key_list)
        self.assertIsNotNone(result)

    def test_process_key_uid_string_method_attribute(self):
        name = 'process_key_uid'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_process_key_uid_string_result_is_not_none(self):
        result = self.x.process_key_uid(self.key_uid_string)
        self.assertIsNotNone(result)

    def test_process_key_uid_string_returns_packed_tuple(self):
        result = self.x.process_key_uid(self.key_uid_string)
        target_string = user_key_uid_string
        split = target_string.split()
        check = (split[0], split[-1])
        self.assertEqual(result, check)

    def test_create_userid_and_keyid_tuple_attribute(self):
        name = 'create_userid_and_keyid_tuple_list'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_create_userid_and_keyid_tuple_method_takes_raw_list(self):
        result = self.x.create_userid_and_keyid_tuple_list(self.key_list)
        self.assertIsNotNone(result)

    def test_create_userid_and_key_id_returns_tuple(self):
        userid = user_key_uid_string
        keyid = user_keyid
        target = (userid, keyid)
        result = self.x.create_userid_and_keyid_tuple_list(self.key_list)
        self.assertIn(target, result)

    def test_process_key_dropdown_strings_attribute(self):
        name = 'process_key_dropdown_list_strings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_process_key_dropdown_strings_method_result(self):
        name = user_name
        email = user_email
        keyid = user_keyid
        spacer = ', '
        target_string = name + spacer + email + spacer + keyid
        interim = self.x.create_userid_and_keyid_tuple_list(self.key_list)
        result = self.x.process_key_dropdown_list_strings(interim)
        self.assertIn(target_string, result)

    def test_format_result(self):
        target = [user_name + ', ' + user_email + ', ' + user_keyid]
        result = self.x.format(self.key_list)
        for item in target:
            self.assertIn(item, result)

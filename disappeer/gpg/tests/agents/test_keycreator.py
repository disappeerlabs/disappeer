"""
test_keycreator.py

Test suite for KeyCreator module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.gpg.agents import keycreator
from disappeer.gpg.agents import gpgagent
import queue
import threading
from disappeer import gpg
from disappeer.constants import constants


new_key_default_vals_dict = {"Name": "Newsy",
                             "Email": "newsy@email.com",
                             "Comment": "Default comment message",
                             "Key Length": "2048",
                             "Key Type": "RSA",
                             "Key Usage": "",
                             "Subkey Type": "ELG-E",
                             "Subkey Length": "2048",
                             "Expire Date": "2018-04-01",
                             "Passphrase": "passphrase"
                             }

new_key_input_dict = {"Name": "name_real",
                      "Email": "name_email",
                      "Comment": "name_comment",
                      "Key Length": "key_length",
                      "Key Type": "key_type",
                      "Key Usage": "key_usage",
                      "Subkey Type": "subkey_type",
                      "Subkey Length": "subkey_length",
                      "Expire Date": "expire_date",
                      "Passphrase": "passphrase"
                      }


def create_key_input_dict(key_dict=new_key_input_dict,
                          key_input_val_dict=new_key_default_vals_dict):
    """Take key vals dict as input, return dict structured for key creation"""
    new_key_default_vals_dict = key_input_val_dict
    new_key_input_dict = key_dict
    final_key_dict = {}
    for item in new_key_input_dict:
        key = new_key_input_dict[item]
        val = new_key_default_vals_dict[item]
        final_key_dict[key] = val
    return final_key_dict


class TestImportsAndConstants(unittest.TestCase):

    def test_gpgagent(self):
        self.assertEqual(gpgagent, keycreator.gpgagent)

    def test_threading(self):
        self.assertEqual(threading, keycreator.threading)

    def test_constants(self):
        self.assertEqual(constants, keycreator.constants)

    def test_constants_command_list(self):
        target = constants.command_list
        self.assertEqual(target, keycreator.command_list)


class TestKeyCreatorClass(unittest.TestCase):

    def setUp(self):
        self.queue = queue.Queue()
        self.keydir = "tests/data/keys"
        self.x = keycreator.KeyCreator(self.keydir, self.queue)

    def test_instance(self):
        self.assertIsInstance(self.x, keycreator.KeyCreator)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.x, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_queue_attribute_set(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_execute_method_attribute(self):
        name = 'execute'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_create_new_key_worker_method_attribute(self):
        name = '_create_new_key_worker'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch('disappeer.gpg.agents.keycreator.threading')
    def test_execute_calls_thread(self, mocked):
        key_input = create_key_input_dict(new_key_input_dict, new_key_default_vals_dict)
        mocked.Thread = MagicMock()
        self.x.execute(key_input)
        self.assertTrue(mocked.Thread.called)

    @patch.object(gpg.agents.keycreator.threading.Thread, 'start')
    def test_execute_calls_thread_start(self, mocked1):
        key_input = create_key_input_dict(new_key_input_dict, new_key_default_vals_dict)
        # sub = mocked1.start = MagicMock()
        self.x.execute(key_input)
        self.assertTrue(mocked1.called)

    @unittest.skip("Long running method for key creation")
    def test_create_new_key_method(self):
        before = self.x.gpg.list_keys()
        before_len = len(before)
        key_input = create_key_input_dict(new_key_input_dict, new_key_default_vals_dict)
        result = self.x._create_new_key_worker(key_input)
        after = self.x.gpg.list_keys()
        after_len = len(after)
        self.assertEqual(after_len - before_len, 1)

    def test_create_new_key_worker_puts_to_queue(self):
        target = "tests/data/keys"
        self.x.gpg = MagicMock()
        self.x.gpg.gen_key = MagicMock(return_value=target)
        result = self.x._create_new_key_worker(dict())
        got = self.queue.get()
        comp = dict(desc=constants.command_list.Create_New_Key, result=target)
        self.assertEqual(comp, got)

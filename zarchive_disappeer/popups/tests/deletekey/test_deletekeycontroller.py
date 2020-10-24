"""
test_deletekeycontroller.py

Test suite for popup DeleteKeyController module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.deletekey import deletekeycontroller
from disappeer.popups.deletekey import deletekeyview
from disappeer.popups.bases import basepopupcontroller
import tkinter


example_key_1={'expires': '1522555200',
                'type': 'pub',
                'dummy': '',
                'trust': '-',
                'length': '2048',
                'subkeys': [['D75B831381D22E16',
                          'e',
                          '5E903CE9E251F6DDB5B45FEED75B831381D22E16']],
                'uids': ['Mallory (Default comment message) <mallory@email.com>'],
                'date': '1495828561',
                'keyid': '5933EB9BDA9B62BB',
                'algo': '1',
                'ownertrust': '-',
                'fingerprint': 'C227D0EC9289CB9D1F06A9A85933EB9BDA9B62BB'}

key_list_test = [example_key_1]


class TestImports(unittest.TestCase):

    def test_keyinfo_view(self):
        self.assertEqual(deletekeyview, deletekeycontroller.deletekeyview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, deletekeycontroller.basepopupcontroller)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.key_list = key_list_test
        self.x = deletekeycontroller.DeleteKeyController(self.root, self.key_list)

    def test_instance(self):
        self.assertIsInstance(self.x, deletekeycontroller.DeleteKeyController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_key_list_arg(self):
        self.assertEqual(self.x.key_list, self.key_list)

    def test_view(self):
        self.assertIsInstance(self.x.view, deletekeyview.DeleteKeyView)

    def test_title_attribute_set(self):
        target = 'Delete Keys'
        self.assertEqual(target, self.x.title)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.cancel_button.bind.called)

    def test_config_event_bindings_calls_bind_with_on_cancel_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.x.view.cancel_button.bind.assert_called_with("<ButtonRelease-1>", self.x.cancel_button_clicked)

    def test_config_event_bindings_calls_bind_on_delete_button(self):
        self.x.view = MagicMock()
        self.x.view.delete_key_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.delete_key_button.bind.called)

    def test_config_event_bindings_calls_bind_with_on_delete_button(self):
        self.x.view = MagicMock()
        self.x.view.delete_key_button = MagicMock()
        self.x.config_event_bindings()
        self.x.view.delete_key_button.bind.assert_called_with("<ButtonRelease-1>", self.x.delete_button_clicked)

    @patch.object(deletekeycontroller.DeleteKeyController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = deletekeycontroller.DeleteKeyController(self.root, self.key_list)
        self.assertTrue(mocked.called)

    def test_read_check_button_vals(self):
        val = self._helper_set_check_button_vals()
        result = self.x.read_check_button_vals_and_pack_list()
        check = [(val, self.key_list[0]['fingerprint'], self.key_list[0]['uids'])]
        self.assertEqual(result, check)

    def _helper_set_check_button_vals(self):
        import random
        result = None
        for idx, item in enumerate(self.key_list):
            choice = random.choice([0, 1])
            self.x.view.int_vars[idx].set(choice)
            result = choice
        return result

    def test_delete_button_clicked_calls_read_check_button_vals(self):
        sub = self.x.read_check_button_vals_and_pack_list = MagicMock()
        self.x.delete_button_clicked(None)
        self.assertTrue(sub.called)

    def test_pack_deletion_targets_list(self):
        val = self._helper_set_check_button_vals()
        result = self.x.read_check_button_vals_and_pack_list()
        final = self.x.build_deletion_targets_list(result)
        if val == 0:
            self.assertEqual(len(final), 0)
        elif val == 1:
            self.assertEqual(len(final), 1)

    def test_delete_button_clicked_calls_build_deletion_targets(self):
        stub = self.x.read_check_button_vals_and_pack_list = MagicMock(return_value='hello')
        sub = self.x.build_deletion_targets_list = MagicMock()
        self.x.delete_button_clicked(None)
        sub.assert_called_with(stub.return_value)

    def test_if_selections_greater_than_zero_set_output(self):
        self.x.view.int_vars[0].set(1)
        self.x.delete_button_clicked(None)
        self.assertIsNotNone(self.x.output)



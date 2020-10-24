"""
test_keyinfocontroller.py

Test suite for KeyInfoController module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.keyinfo import keyinfocontroller
from disappeer.popups.keyinfo import keyinfoview
import tkinter


example_key={'expires': '1522555200',
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


class TestImports(unittest.TestCase):

    def test_keyinfo_view(self):
        self.assertEqual(keyinfoview, keyinfocontroller.keyinfoview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, keyinfocontroller.basepopupcontroller)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.key_dict = example_key
        self.x = keyinfocontroller.KeyInfoController(self.root, self.key_dict)

    def test_instance(self):
        self.assertIsInstance(self.x, keyinfocontroller.KeyInfoController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_title(self):
        name = "Key Info"
        self.assertEqual(name, self.x.title)

    def test_key_dict_arg(self):
        self.assertEqual(self.x.key_dict, self.key_dict)

    def test_view(self):
        self.assertIsInstance(self.x.view, keyinfoview.KeyInfoView)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.cancel_button.bind.called)

    def test_config_event_bindings_calls_bind_on_close_window(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.x.view.cancel_button.bind.assert_called_with("<ButtonRelease-1>", self.x.close_window)

    @patch.object(keyinfocontroller.KeyInfoController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = keyinfocontroller.KeyInfoController(self.root, self.key_dict)
        self.assertTrue(mocked.called)

    def test_close_window(self):
        self.x.set_output_and_close = MagicMock()
        self.x.close_window(None)
        self.x.set_output_and_close.assert_called_with(self.x.key_dict)


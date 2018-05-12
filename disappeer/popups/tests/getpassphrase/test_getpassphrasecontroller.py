"""
test_getpassphrasecontroller.py

Test suite for popup GetPassphraseController module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.getpassphrase import getpassphrasecontroller
from disappeer.popups.getpassphrase import getpassphraseview
from disappeer.popups.bases import basepopupcontroller
import tkinter


class TestImports(unittest.TestCase):

    def test_getpassphraseview(self):
        self.assertEqual(getpassphraseview, getpassphrasecontroller.getpassphraseview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, getpassphrasecontroller.basepopupcontroller)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.x = getpassphrasecontroller.GetPassphraseController(self.root)

    def test_instance(self):
        self.assertIsInstance(self.x, getpassphrasecontroller.GetPassphraseController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_root_attribute(self):
        self.assertEqual(self.root, self.x.root)

    def test_title_attribute_set(self):
        target = 'Enter Passphrase'
        self.assertEqual(target, self.x.title)

    def test_view_attribute(self):
        self.assertIsInstance(self.x.view, getpassphraseview.GetPassphraseView)

    def test_view_window_attribute(self):
        self.assertEqual(self.x.window, self.x.view.window)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.cancel_button.bind.called)

    def test_submit_button_clicked(self):
        sub = self.x.view.passphrase_entry.get = MagicMock(return_value='hello')
        target = self.x.set_output_and_close = MagicMock()
        self.x.submit_button_clicked(None)
        target.assert_called_with(sub.return_value)

    def test_config_event_bindings_calls_bind_on_submit_button(self):
        self.x.view = MagicMock()
        self.x.view.submit_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.submit_button.bind.called)

    @patch.object(getpassphrasecontroller.GetPassphraseController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = getpassphrasecontroller.GetPassphraseController(self.root)
        self.assertTrue(mocked.called)

    def test_config_event_bindings_sets_focus_to_entry(self):
        sub = self.x.view.passphrase_entry.focus_force = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(sub.called)

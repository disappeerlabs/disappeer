"""
test_displaymessagecontroller.py

Test suite for the DisplayMessageController popup module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.displaymessage import displaymessagecontroller
from disappeer.popups.displaymessage import displaymessageview
from disappeer.popups.bases import  basepopupcontroller
import tkinter
import types


class TestImports(unittest.TestCase):

    def test_displaymessageview(self):
        self.assertEqual(displaymessageview, displaymessagecontroller.displaymessageview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, displaymessagecontroller.basepopupcontroller)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.argnamespace = MagicMock()
        self.x = displaymessagecontroller.DisplayMessageController(self.root, self.argnamespace)

    def test_instance(self):
        self.assertIsInstance(self.x, displaymessagecontroller.DisplayMessageController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_has_config_event_bindings_attr(self):
        name = 'config_event_bindings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_title(self):
        name = "Message"
        self.assertEqual(name, self.x.title)
        with self.assertRaises(AttributeError):
            self.x.title = 'wtf'

    def test_root_attribute_set(self):
        self.assertEqual(self.root, self.x.root)

    def test_argnamespace_attribute_set(self):
        self.assertEqual(self.argnamespace, self.x.argnamespace)

    def test_view_attribute(self):
        self.assertIsInstance(self.x.view, displaymessageview.DisplayMessageView)
        self.assertEqual(self.x.view.window, self.x.window)
        self.assertEqual(self.x.view.argnamespace, self.x.argnamespace)

    def test_config_event_bindings_binds_cancel_button_to_default_close(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.cancel_button.bind.called)
        command_button_release_1 = "<ButtonRelease-1>"
        self.x.view.cancel_button.bind.assert_called_with(command_button_release_1, self.x.cancel_button_clicked)

    @patch.object(displaymessagecontroller.DisplayMessageController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = displaymessagecontroller.DisplayMessageController(self.root, MagicMock())
        self.assertTrue(mocked.called)

    def test_config_event_bindings_calls_bind_on_delete_button(self):
        self.x.view = MagicMock()
        target = self.x.view.delete_button.bind = MagicMock()
        self.x.config_event_bindings()
        command_button_release_1 = "<ButtonRelease-1>"
        target.assert_called_with(command_button_release_1, self.x.delete_button_clicked)

    def test_config_event_bindings_calls_bind_on_inspect_button(self):
        self.x.view = MagicMock()
        target = self.x.view.inspect_button.bind = MagicMock()
        self.x.config_event_bindings()
        command_button_release_1 = "<ButtonRelease-1>"
        target.assert_called_with(command_button_release_1, self.x.inspect_button_clicked)

    def test_delete_button_sets_output_to_delete(self):
        name = 'delete'
        target = self.x.set_output_and_close = MagicMock()
        self.x.delete_button_clicked(None)
        target.assert_called_with(name)

    def test_inspect_button_sets_output_to_inspect(self):
        name = 'inspect'
        target = self.x.set_output_and_close = MagicMock()
        self.x.inspect_button_clicked(None)
        target.assert_called_with(name)

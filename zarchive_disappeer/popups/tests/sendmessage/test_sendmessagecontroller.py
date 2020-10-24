"""
test_sendmessagecontroller.py

Test suite for the SendMessageController popup module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.sendmessage import sendmessagecontroller
from disappeer.popups.sendmessage import sendmessageview
from disappeer.popups.bases import basepopupcontroller
import types
import tkinter


class TestImports(unittest.TestCase):

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, sendmessagecontroller.basepopupcontroller)

    def test_sendmessageview(self):
        self.assertEqual(sendmessageview, sendmessagecontroller.sendmessageview)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.click_command = "<ButtonRelease-1>"
        self.data_record = types.SimpleNamespace(gpg_uid='USER INFO STRING')
        self.console_text = 'Hello world'
        self.root = tkinter.Tk()
        self.x = sendmessagecontroller.SendMessageController(self.root, self.data_record, self.console_text)

    def test_instance(self):
        self.assertIsInstance(self.x, sendmessagecontroller.SendMessageController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_root_attribute_set(self):
        self.assertEqual(self.x.root, self.root)

    def test_title_attribute(self):
        target = 'Send Message'
        self.assertEqual(target, self.x.title)

    def test_recpient_data_record_attribute_set(self):
        self.assertEqual(self.x.recipient_data_record, self.data_record)

    def test_console_text_attribute_set(self):
        self.assertEqual(self.x.console_text, self.console_text)

    def test_view_instantiated(self):
        self.assertIsInstance(self.x.view, sendmessageview.SendMessageView)

    def test_view_instantiated_with_window_and_uid_and_text(self):
        self.assertEqual(self.x.view.window, self.x.window)
        self.assertEqual(self.x.view.recipient_text, self.data_record.gpg_uid)
        self.assertEqual(self.x.view.message_text, self.console_text)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        target = self.x.view.cancel_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.click_command, self.x.cancel_button_clicked)

    def test_config_event_bindings_calls_bind_on_send_button(self):
        self.x.view = MagicMock()
        target = self.x.view.send_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.click_command, self.x.send_button_clicked)

    @patch.object(sendmessagecontroller.SendMessageController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = sendmessagecontroller.SendMessageController(self.root, self.data_record, self.console_text)
        self.assertTrue(mocked.called)

    def test_send_button_sets_output_to_send_with_view_message_text(self):
        text = 'hello world'
        console_text = self.x.view.get_text_area = MagicMock(return_value=text)
        target = self.x.set_output_and_close = MagicMock()
        target_args = console_text.return_value
        self.x.send_button_clicked(None)
        target.assert_called_with(target_args)


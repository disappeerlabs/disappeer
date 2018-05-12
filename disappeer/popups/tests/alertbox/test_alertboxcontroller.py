"""
test_alertboxcontroller.py

Test suite for AlertBoxController module popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.alertbox import alertboxview
from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.alertbox import alertboxcontroller
import tkinter


class TestImports(unittest.TestCase):

    def test_alertbox_view(self):
        self.assertEqual(alertboxview, alertboxcontroller.alertboxview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, alertboxcontroller.basepopupcontroller)


class TestAlertBoxControllerClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.msg = "This is a test message"
        self.x = alertboxcontroller.AlertBoxController(self.root, self.msg)

    def test_instance(self):
        self.assertIsInstance(self.x, alertboxcontroller.AlertBoxController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_title(self):
        name = "Alert!"
        self.assertEqual(name, self.x.title)

    def test_config_event_bindings_attribute(self):
        name = 'config_event_bindings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_root_attribute_set(self):
        self.assertEqual(self.root, self.x.root)

    def test_message_attribute_set(self):
        self.assertEqual(self.msg, self.x.message)

    def test_view_attribute(self):
        self.assertIsInstance(self.x.view, alertboxview.AlertBoxView)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.cancel_button.bind.called)

    @patch.object(alertboxcontroller.AlertBoxController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = alertboxcontroller.AlertBoxController(self.root, self.msg)
        self.assertTrue(mocked.called)
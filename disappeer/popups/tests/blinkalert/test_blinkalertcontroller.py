"""
test_blinkalertcontroller.py

Test suite for the BlinkAlert popup controller

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.blinkalert import blinkalertcontroller
from disappeer.popups.blinkalert import blinkalertview
from disappeer.popups.bases import basepopupcontroller
import tkinter


class TestImports(unittest.TestCase):

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, blinkalertcontroller.basepopupcontroller)

    def test_blinkalert_view(self):
        self.assertEqual(blinkalertview, blinkalertcontroller.blinkalertview)

    def test_tkinter(self):
        self.assertEqual(tkinter, blinkalertcontroller.tkinter)


class TestBlinkAlertControllerClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.msg = "This is a test message"
        self.x = blinkalertcontroller.BlinkAlertController(self.root, self.msg)

    def test_instance(self):
        self.assertIsInstance(self.x, blinkalertcontroller.BlinkAlertController)

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

    def test_alpha_attr_set_to_zero(self):
        check = 0.0
        self.assertEqual(check, self.x.window.attributes('-alpha'))

    def test_view_attribute(self):
        self.assertIsInstance(self.x.view, blinkalertview.BlinkAlertView)

    def test_geometry_attribute(self):
        target = '250x100-0+0'
        result = self.x.window.geometry()

    def test_blink_count_set_zero(self):
        self.assertEqual(0, self.x.blink_count)

    def test_show_method_calls_fade_in(self):
        target = self.x.fade_in = MagicMock()
        self.x.show()
        target.assert_called_with()

    def test_fade_in_calls_cancel_if_blink_count_greater_than_three(self):
        self.x.blink_count = 3
        target = self.x.cancel_button_clicked = MagicMock()
        self.x.fade_in()
        target.assert_called_with(None)

    def test_fade_in_catches_tcl_attribute_error(self):
        self.x.window.attributes = MagicMock(side_effect=tkinter.TclError)
        try:
            self.x.fade_in()
        except tkinter.TclError as err:
            self.assertTrue(False)

    def test_fade_in_incremenets_alpha_val_if_less_than_1(self):
        self.x.window.attributes('-alpha', .01)
        self.x.fade_in()
        self.assertEqual(self.x.window.attributes('-alpha'), .04)

    def test_fade_in_calls_root_after_if_less_than_1(self):
        self.x.window.attributes('-alpha', .01)
        target = self.x.root.after = MagicMock()
        self.x.fade_in()
        target.assert_called_with(50, self.x.fade_in)

    def test_fade_in_increments_blink_count_if_alpha_is_1(self):
        self.x.window.attributes('-alpha', 1)
        sub = self.x.root.after = MagicMock()
        self.x.fade_in()
        self.assertEqual(1, self.x.blink_count)

    def test_fade_in_calls_fade_away_with_root_after_if_alpha_is_1(self):
        self.x.window.attributes('-alpha', 1)
        target = self.x.root.after = MagicMock()
        self.x.fade_in()
        target.assert_called_with(2000, self.x.fade_away)

    def test_fade_away_catches_tcl_attribute_error(self):
        self.x.window.attributes = MagicMock(side_effect=tkinter.TclError)
        try:
            self.x.fade_away()
        except tkinter.TclError as err:
            self.assertTrue(False)

    def test_fade_away_decrements_alpha_if_greater_than_zero(self):
        self.x.window.attributes('-alpha', .9)
        self.x.fade_away()
        self.assertEqual(self.x.window.attributes('-alpha'), .8)

    def test_fade_away_calls_root_after_if_greater_than_zero(self):
        self.x.window.attributes('-alpha', .9)
        target = self.x.root.after = MagicMock()
        self.x.fade_away()
        target.assert_called_with(50, self.x.fade_away)

    def test_fade_away_calls_fade_in_if_alpha_equals_zerp(self):
        self.x.window.attributes('-alpha', 0.0)
        target = self.x.fade_in = MagicMock()
        self.x.fade_away()
        target.assert_called_with()

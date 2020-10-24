"""
test_basepopupcontroller.py

Test suite for BasePopupController module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.bases import basepopupcontroller
import tkinter
import abc


class TestImports(unittest.TestCase):

    def test_tkinter(self):
        self.assertEqual(tkinter, basepopupcontroller.tkinter)

    def test_abc(self):
        self.assertEqual(abc, basepopupcontroller.abc)


class FakePopUpControllerClass(basepopupcontroller.BasePopupController):

    def config_event_bindings(self):
        pass

    def title(self):
        return 'Default Base Title'


class FakePopUpControllerClassNoConfig(basepopupcontroller.BasePopupController):

    def title(self):
        return 'Default Base Title'

class TestBaseControllerBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.x = FakePopUpControllerClass(self.root)

    def test_instance(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_instance_abc(self):
        self.assertIsInstance(self.x, abc.ABC)

    def test_root_attribute_set(self):
        self.assertEqual(self.root, self.x.root)

    def test_window_attribute_set(self):
        self.assertIsInstance(self.x.window, tkinter.Toplevel)

    def test_title_attribute(self):
        name = 'title'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_title_attribute_default(self):
        name = 'Default Base Title'
        self.assertEqual(self.x.title(), name)

    # TODO Figure out how to mock the call to window.title()
    def test_title_attribute_set(self):
        pass

    def test_output_attribute(self):
        name = 'output'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_output_attribute_is_none(self):
        self.assertIsNone(self.x.output)

    def test_show_method_attribute(self):
        name = 'show'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_show_method_calls_window_transient(self):
        self.x.window = MagicMock()
        subject = self.x.window.transient = MagicMock()
        self.x.show()
        subject.assert_called_with(self.x.root)

    def test_show_method_calls_window_grab_set(self):
        self.x.window = MagicMock()
        subject = self.x.window.grab_set = MagicMock()
        self.x.show()
        subject.assert_called_with()

    def test_show_method_calls_window_deiconify(self):
        self.x.window = MagicMock()
        subject = self.x.window.deiconify = MagicMock()
        self.x.show()
        subject.assert_called_with()

    def test_show_method_calls_window_wait_window(self):
        self.x.window = MagicMock()
        subject = self.x.window.wait_window = MagicMock()
        self.x.show()
        subject.assert_called_with()

    def test_show_method_returns_output(self):
        self.x.output = 123
        self.x.window = MagicMock()
        result = self.x.show()
        self.assertEqual(result, self.x.output)

    def test_config_event_bindings_method_attribute(self):
        name = 'config_event_bindings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_config_event_bindings_method_is_abstract(self):
        with self.assertRaises(TypeError):
            x = FakePopUpControllerClassNoConfig(self.root)

    def test_cancel_button_clicked_method_attribute(self):
        name = 'cancel_button_clicked'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_cancel_button_clicked_calls_destroy(self):
        self.x.window = MagicMock()
        subject = self.x.window.destroy = MagicMock()
        self.x.cancel_button_clicked(None)
        subject.assert_called_with()

    def test_set_output_and_close_method_attribute(self):
        name = 'set_output_and_close'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_set_output_and_close_method_sets_output(self):
        msg = '666'
        self.x.set_output_and_close(msg)
        self.assertEqual(self.x.output, msg)

    def test_set_output_and_close_method_closes_window(self):
        self.x.window = MagicMock()
        subject = self.x.window.destroy = MagicMock()
        self.x.set_output_and_close(None)
        self.assertTrue(subject.called)
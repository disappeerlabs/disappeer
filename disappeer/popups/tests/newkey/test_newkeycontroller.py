"""
test_newkeycontroller.py

Test Suite for the popup NewKeyController module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.newkey import newkeycontroller
from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.newkey import newkeyview
import tkinter
from disappeer.constants import constants


class TestImports(unittest.TestCase):

    def test_keyinfo_view(self):
        self.assertEqual(newkeyview, newkeycontroller.newkeyview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, newkeycontroller.basepopupcontroller)

    def test_constants(self):
        self.assertEqual(constants, newkeycontroller.constants)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.x = newkeycontroller.NewKeyController(self.root)

    def test_instance(self):
        self.assertIsInstance(self.x,newkeycontroller.NewKeyController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_root_attribute(self):
        self.assertEqual(self.x.root, self.root)

    def test_view(self):
        self.assertIsInstance(self.x.view, newkeyview.NewKeyView)

    def test_title_attribute_set(self):
        target = 'Create New Key'
        self.assertEqual(target, self.x.title)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.cancel_button.bind.called)

    def test_reset_button_clicked_method_attribute(self):
        name = 'reset_button_clicked'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_reset_button_calls_view_reset(self):
        sub = self.x.view.reset_entry_vals = MagicMock()
        self.x.reset_button_clicked(None)
        sub.assert_called_with()

    def test_config_event_bindings_calls_bind_on_reset_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.reset_button.bind.called)

    def test_create_new_key_button_clicked_method_attribute(self):
        name = 'create_new_key_button_clicked'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_config_event_bindings_calls_bind_on_new_key_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.create_new_key_button.bind.called)

    @patch.object(newkeycontroller.NewKeyController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = newkeycontroller.NewKeyController(self.root)
        self.assertTrue(mocked.called)

    def test_create_new_key_button_gathers_view_vals(self):
        sub = self.x.get_view_string_var_vals = MagicMock()
        sub_2 = self.x.zip_key_dict = MagicMock()
        result = self.x.create_new_key_button_clicked(None)
        sub.assert_called_with()

    def test_get_view_string_var_vals(self):
        vals = self._helper_populate_view_string_vars()
        result = self.x.get_view_string_var_vals()
        self.assertEqual(vals, result)

    def test_zip_key_dict(self):
        vals = self._helper_populate_view_string_vars()
        form_field_vals_dict = self._helper_return_zipped_dict_comp()
        result = self.x.zip_key_dict(vals)
        self.assertEqual(form_field_vals_dict, result)

    def test_prepare_output_dict(self):
        form_field_vals_dict = self._helper_return_zipped_dict_comp()
        output_dict = {}
        for item in constants.new_key_ordered_field_labels:
            key = constants.new_key_input_dict[item]
            val = form_field_vals_dict[item]
            output_dict[key] = val
        result = self.x.prepare_output_dict(form_field_vals_dict)
        self.assertEqual(output_dict, result)

    def test_create_new_key_calls_zip_method(self):
        vals = self._helper_populate_view_string_vars()
        sub_2 = self.x.get_view_string_var_vals = MagicMock()
        sub = self.x.zip_key_dict = MagicMock()
        result = self.x.create_new_key_button_clicked(None)
        self.assertTrue(sub.called)

    def test_create_new_key_calls_output_with_correct(self):
        target = {'name_email': 'mallory@email.com', 'passphrase': 'passphrase', 'key_usage': '', 'key_type': 'RSA', 'expire_date': '2028-04-01', 'subkey_type': 'ELG-E', 'subkey_length': '2048', 'key_length': '2048', 'name_comment': 'Default comment message', 'name_real': 'Mallory'}
        vals = self._helper_populate_view_string_vars()
        sub = self.x.set_output_and_close = MagicMock()
        result = self.x.create_new_key_button_clicked(None)
        sub.assert_called_with(target)

    def _helper_populate_view_string_vars(self):
        vals = []
        for idx, item in enumerate(constants.new_key_ordered_field_labels):
            current = constants.new_key_default_vals_dict[item]
            self.x.view.string_vars[idx].set(current)
            vals.append(current)
        return vals

    def _helper_return_zipped_dict_comp(self):
        vals = self._helper_populate_view_string_vars()
        form_field_vals_dict = dict(zip(constants.new_key_ordered_field_labels, vals))
        return form_field_vals_dict

"""
test_contactrequestcontroller.py

Test suite for the ContactRequestController, controller class object for the new contact request popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.contactrequest import contactrequestcontroller
from disappeer.popups.contactrequest import contactrequestview
from disappeer.net.contact import contactrequestvalidator
from disappeer.models.db import dbcontactrequesttable
import tkinter
from disappeer.net.contact import contactrequestfactory
from disappeer.net.contact import contactrequestvalidator


class TestImports(unittest.TestCase):

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, contactrequestcontroller.basepopupcontroller)

    def test_contactrequestview(self):
        self.assertEqual(contactrequestview, contactrequestcontroller.contactrequestview)

    def test_contactrequestvalidator(self):
        self.assertEqual(contactrequestvalidator, contactrequestcontroller.contactrequestvalidator)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.click_command = "<ButtonRelease-1>"
        self.key_test_dir = 'tests/data/keys'
        self.db_file_path = 'models/db/tests/testdatabasesmain.sqlite'
        self.db_table = dbcontactrequesttable.DBContactRequestTable(self.db_file_path)
        self.last_record = self.db_table.fetch_last_record()
        self.nonce = self.last_record[1]
        self.record = self.db_table.fetch_one_by_nonce(self.nonce)
        self.invalid_record = list(self.record)
        self.invalid_record[-1] = 'xxx'
        self.invalid_record = self.db_table.build_named_tuple(self.invalid_record)
        self.root = tkinter.Tk()
        with patch.object(contactrequestcontroller.contactrequestvalidator, 'ContactRequestValidator'):
            self.x = contactrequestcontroller.ContactRequestController(self.root, self.record)

    def test_instance(self):
        self.assertIsInstance(self.x, contactrequestcontroller.ContactRequestController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_root_attribute_set(self):
        self.assertEqual(self.x.root, self.root)

    def test_request_record_attribute_set(self):
        self.assertEqual(self.x.request_record, self.record)

    def test_title_attribute_set(self):
        target = 'New Contact Request'
        self.assertEqual(target, self.x.title)

    def test_construct_data_dict_method_reconstructs_contact_req_dict(self):
        target = dict(sig=self.record.sig, data=self.record.data)
        result = self.x.construct_contact_req_dict(self.record)
        self.assertEqual(target, result)

    def test_contact_req_dict_attribute_set_by_construct_contact_req_dict(self):
        target = dict(sig=self.record.sig, data=self.record.data)
        result = self.x.construct_contact_req_dict(self.record)
        self.assertEqual(self.x.data_dict, result)

    def test_validator_attribute_is_instance_of_validator(self):
        self.x = contactrequestcontroller.ContactRequestController(self.root, self.record)
        self.assertIsInstance(self.x.validator, contactrequestvalidator.ContactRequestValidator)

    def test_validator_takes_contact_req_dict_as_arg(self):
        self.x = contactrequestcontroller.ContactRequestController(self.root, self.record)
        self.assertEqual(self.x.validator.contact_req_dict, self.x.data_dict)

    def test_view_instantiated_if_validator_is_valid(self):
        self.assertIsInstance(self.x.view, contactrequestview.ContactRequestView)

    def test_view_instantiated_with_window_and_validator_key_dict(self):
        self.assertEqual(self.x.view.window, self.x.window)
        self.assertEqual(self.x.view.key_dict, self.x.validator.key_dict)

    @patch.object(contactrequestcontroller.ContactRequestController, 'handle_invalid_request')
    def test_init_returns_false_if_invalid_input(self, target):
        invalid = contactrequestcontroller.ContactRequestController(self.root, self.invalid_record)
        target.assert_called_with()

    @patch.object(contactrequestcontroller.ContactRequestController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = contactrequestcontroller.ContactRequestController(self.root, self.record)
        self.assertTrue(mocked.called)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        target = self.x.view.cancel_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.click_command, self.x.cancel_button_clicked)

    def test_config_event_bindings_calls_bind_on_accept_button(self):
        self.x.view = MagicMock()
        target = self.x.view.accept_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.click_command, self.x.accept_button_clicked)

    def test_config_event_bindings_calls_bind_on_reject_button(self):
        self.x.view = MagicMock()
        target = self.x.view.reject_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.click_command, self.x.reject_button_clicked)

    def test_handle_invalid_request_sets_output_to_invalid(self):
        name = 'invalid'
        target = self.x.set_output_and_close = MagicMock()
        self.x.handle_invalid_request()
        target.assert_called_with(name)

    def test_accept_button_sets_output_to_accept(self):
        name = 'accept'
        target = self.x.set_output_and_close = MagicMock()
        self.x.accept_button_clicked(None)
        target.assert_called_with(name)

    def test_reject_button_sets_output_false(self):
        name = 'reject'
        target = self.x.set_output_and_close = MagicMock()
        self.x.reject_button_clicked(None)
        target.assert_called_with(name)



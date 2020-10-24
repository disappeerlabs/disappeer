"""
test_gpgcontroller.py

Test suite for the gpgcontroler module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg import gpgcontroller
from unittest.mock import MagicMock, patch
from disappeer.gpg.agents import keyring
from disappeer.gpg.agents import keycreator
from disappeer.gpg.agents import keydeleter
import tkinter.filedialog as filedialog
from disappeer.popups import popuplauncher
from disappeer.gpg.helpers import keyfinder
from disappeer.utilities import queueconsumer
import queue
from disappeer.constants import constants
from disappeer.gpg.helpers import passphrasevalidator
import functools
from disappeer.gpg.tests.gpgcontroller import gpgcontrollersetupclass


class TestImportsAndConstants(unittest.TestCase):

    def test_tkinter_filedialog(self):
        self.assertEqual(filedialog, gpgcontroller.tkinter.filedialog)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, gpgcontroller.popuplauncher)

    def test_keyfinder(self):
        self.assertEqual(keyfinder, gpgcontroller.keyfinder)

    def test_keycreator(self):
        self.assertEqual(keycreator, gpgcontroller.keycreator)

    def test_queueconsumer(self):
        self.assertEqual(queueconsumer, gpgcontroller.queueconsumer)

    def test_constants(self):
        self.assertEqual(constants, gpgcontroller.constants)

    def test_keydeleter(self):
        self.assertEqual(keydeleter, gpgcontroller.keydeleter)

    def test_passphrasevalidator(self):
        self.assertEqual(passphrasevalidator, gpgcontroller.passphrasevalidator)

    def test_functools(self):
        self.assertEqual(functools, gpgcontroller.functools)


class TestGPGControllerClassBasics(gpgcontrollersetupclass.TestGPGControllerSetupClass):

    def test_instance(self):
        self.assertIsInstance(self.x, gpgcontroller.GPGController)

    def test_instance_queue_consumer(self):
        self.assertIsInstance(self.x, queueconsumer.QueueConsumer)

    def test_root_params_attr_set(self):
        self.assertEqual(self.root_params, self.x.root_params)

    def test_root_attribute(self):
        self.assertTrue(self.root, self.x.root)

    def test_view_attribute(self):
        self.assertTrue(self.view, self.x.view)

    def test_command_list_attribute(self):
        self.assertEqual(self.x.command_list, constants.command_list)

    def test_root_queue_attribute(self):
        self.assertTrue(self.queue, self.x.root_queue)

    def test_self_queue_attribute(self):
        self.assertIsInstance(self.x.queue, queue.Queue)

    def test_data_context_attribute_set(self):
        self.assertEqual(self.x.gpg_data_context, self.data_context)

    def test_handle_queue_payload_method_does_not_raise_error(self):
        result = self.x.handle_queue_payload(dict(desc=constants.command_list.Check_Sanity))
        self.assertIsNone(result)

    def test_creating_new_key_state_attribute(self):
        self.assertFalse(self.x.creating_new_key)

    def test_clean_up_new_key_result_stderr_string_method_attribute(self):
        name = 'cleanup_new_key_success_stderr_string'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_clean_up_new_key_result_stderr_string_method_cleans_string(self):
        string_input = 'Hello\n[GNUPG:] PROGRESS primegen\nHello\n'
        target = '[GNUPG:] PROGRESS primegen'
        result = self.x.cleanup_new_key_success_stderr_string(string_input)
        self.assertNotIn(target, result)

    def test_print_notification_method(self):
        name = 'print_notification'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_print_notification_method_calls_view_method(self):
        target = "Hello there print message"
        sub = self.x.view.notifications_box.print_msg = MagicMock()
        self.x.print_notification(target)
        sub.assert_called_with(target)

    def test_append_notification_method(self):
        name = 'append_notification'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_append_notification_method_calls_view_method(self):
        target = "Hello there append msg"
        sub = self.x.view.notifications_box.append_msg = MagicMock()
        self.x.append_notification(target)
        sub.assert_called_with(target)

    def test_config_data_context_method_adds_home_dir_entry_var(self):
        sub = self.x.view.home_dir_entry_var = MagicMock()
        self.x.config_data_context()
        self.assertIn(sub, self.x.gpg_data_context.home_dir_observable.observer_list)

    def test_config_data_context_method_adds_key_info_dropdown_var(self):
        sub = self.x.view.key_info_dropdown_handler = MagicMock()
        self.x.config_data_context()
        self.assertIn(sub, self.x.gpg_data_context.key_list_observable.observer_list)

    def test_config_data_context_method_adds_host_key_observer_var(self):
        sub = self.x.view.host_key_entry_var = MagicMock()
        self.x.config_data_context()
        self.assertIn(sub, self.x.gpg_data_context.host_key_observable.observer_list)

    def test_config_data_context_sets_session_passphrase_none(self):
        target = self.root_params.set_session_passphrase_observable = MagicMock()
        self.x.config_data_context()
        target.assert_called_with(None)

    @patch('disappeer.gpg.gpgcontroller.GPGController.config_data_context')
    def test_config_data_context_called_by_constructor(self, mocked_method):
        self.x = gpgcontroller.GPGController(self.root_params, self.data_context)
        self.assertTrue(mocked_method.called)

    @patch.object(gpgcontroller.popuplauncher, 'launch_alert_box_popup')
    def test_launch_alert_log_launches_alert_and_log_with_msg(self, alertbox):
        msg = 'hello'
        self.x.launch_alert_log(msg)
        alertbox.assert_called_with(self.x.root, msg)

    def test_config_menubar_configs_menu(self):
        mock_menu = MagicMock()
        target = self.x.root_params.get_gpg_menu_obj = MagicMock(return_value=mock_menu)
        self.x.config_menubar()
        target.assert_called_with()
        self.assertTrue(mock_menu.add_command.called)

    @patch.object(gpgcontroller.GPGController, 'config_menubar')
    def test_constructor_calls_config_menubar(self, mocked_method):
        x = gpgcontroller.GPGController(self.root_params,
                                                self.data_context)
        self.assertTrue(mocked_method.called)


class NewKeyResultMockBad:
    fingerprint = None
    stderr = "ERROR MESSAGE"


class NewKeyResultMockGood:
    fingerprint = 'mockfingerprintstring'
    stderr = "Success MESSAGE"


class TestGPGControllerHandleQueuePayloadMethodAndRelated(gpgcontrollersetupclass.TestGPGControllerSetupClass):

    bad_result_mock = NewKeyResultMockBad()
    good_result_mock = NewKeyResultMockGood()
    new_key_payload_bad = dict(desc=constants.command_list.Create_New_Key, result=bad_result_mock)
    new_key_payload_good = dict(desc=constants.command_list.Create_New_Key, result=good_result_mock)
    home = 'tests/data/keys'
    althome = 'tests/data/altkeys'
    key_ring = keyring.KeyRing(home)
    key_dir = 'tests/data/keys'

    def test_handle_queue_payload_method_attribute(self):
        name = 'handle_queue_payload'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_handle_create_new_key_result_method_attribute(self):
        name = 'handle_create_new_key_result'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_handle_queue_payload_create_new_key_calls_create_new_key_callback(self):
        sub = self.x.handle_create_new_key_result = MagicMock()
        self.x.handle_queue_payload(self.new_key_payload_bad)
        sub.assert_called_with(self.new_key_payload_bad)

    def test_handle_create_new_key_result_sets_creating_new_key_attribute(self):
        self.x.creating_new_key = True
        self.x.handle_create_new_key_result(self.new_key_payload_bad)
        self.assertFalse(self.x.creating_new_key)

    def test_handle_create_new_key_result_prints_and_appends_on_bad_result(self):
        sub1 = self.x.print_notification = MagicMock()
        sub2 = self.x.append_notification = MagicMock()
        self.x.handle_create_new_key_result(self.new_key_payload_bad)
        self.assertTrue(sub1.called)
        sub2.assert_called_with(self.bad_result_mock.stderr)

    def test_handle_create_new_key_result_prints_and_appends_on_good_result(self):
        sub1 = self.x.print_notification = MagicMock()
        sub2 = self.x.append_notification = MagicMock()
        self.x.handle_create_new_key_result(self.new_key_payload_good)
        self.assertTrue(sub1.called)
        sub2.assert_called_with(self.good_result_mock.stderr)

    def test_handle_create_new_key_result_sets_key_list_on_good_result(self):
        sub1 = self.x.key_list_observable = MagicMock()
        sub = self.x.gpg_data_context.set_key_list = MagicMock()
        self.x.handle_create_new_key_result(self.new_key_payload_good)
        self.assertTrue(sub.called)

    def test_handle_create_new_key_result_sets_host_key_on_good_result(self):
        sub1 = self.x.key_list_observable = MagicMock()
        sub = self.x.gpg_data_context.set_key_list = MagicMock()
        target = self.x.gpg_data_context.set_host_key = MagicMock()
        self.x.handle_create_new_key_result(self.new_key_payload_good)
        self.assertTrue(target.called)
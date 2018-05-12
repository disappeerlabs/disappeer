"""
test_gpgcontrollereventmethods.py

Test Suite for GPGController Event Methods

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
import gpg.gpgcontroller as gpgcontroller
from unittest.mock import MagicMock, patch
import gpg.agents.keyring as keyring
import types
import gpg.tests.gpgcontroller.gpgcontrollersetupclass as gpgcontrollersetupclass


class TestGPGControllerClickMethods(gpgcontrollersetupclass.TestGPGControllerSetupClass):

    valid_keyid = '190DB52959AC3560'
    home = 'tests/data/keys'
    althome = 'tests/data/altkeys'
    key_ring = keyring.KeyRing(home)

    def test_homedir_entry_clicked_attribute(self):
        name = 'homedir_entry_clicked'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch('tkinter.filedialog.askdirectory')
    def test_homedir_entry_clicked_launches_ask_dir(self, mocked):
        sub = self.x.is_tor_proxy_running = MagicMock(return_value=False)
        sub_start_routine = self.x.start_set_passphrase_routine = MagicMock()
        mocked.return_value = self.althome
        self.x.homedir_entry_clicked(None)
        self.assertTrue(mocked.called)

    def test_homedir_entry_clicked_returns_none_on_empty_string(self):
        sub = self.x.is_tor_proxy_running = MagicMock(return_value=False)
        import tkinter.filedialog as fd
        fd.askdirectory = MagicMock(return_value='')
        result = self.x.homedir_entry_clicked(None)
        self.assertIsNone(result)

    def test_homedir_entry_clicked_returns_none_on_empty_tuple(self):
        sub = self.x.is_tor_proxy_running = MagicMock(return_value=False)
        import tkinter.filedialog as fd
        fd.askdirectory = MagicMock(return_value=())
        result = self.x.homedir_entry_clicked(None)
        self.assertIsNone(result)

    @patch('tkinter.filedialog.askdirectory')
    def test_homedir_entry_clicked_sets_home_dir_and_calls_start_set_passphrase_routine(self, mocked):
        sub = self.x.is_tor_proxy_running = MagicMock(return_value=False)
        mocked.return_value = self.althome
        sub = self.x.gpg_data_context.set_home_dir = MagicMock()
        target = self.x.start_set_passphrase_routine = MagicMock()
        result = self.x.homedir_entry_clicked(None)
        self.assertTrue(mocked.called)
        self.assertTrue(sub.called)
        sub.assert_called_with(mocked.return_value)
        target.assert_called_with()

    def test_homedir_entry_clicked_returns_false_if_tor_proxy_is_running(self):
        sub = self.x.is_tor_proxy_running = MagicMock(return_value=True)
        result = self.x.homedir_entry_clicked(None)
        self.assertIs(result, False)

    def test_is_tor_proxy_running_launches_alert_returns_true_if_observable_status_is_true(self):
        sub = self.x.root_params.get_tor_proxy_running_observable = MagicMock(return_value=True)
        target = self.x.launch_alert_log = MagicMock()
        result = self.x.is_tor_proxy_running()
        self.assertTrue(target.called)
        self.assertIs(result, True)

    def test_is_tor_proxy_running_returns_false_if_obs_is_false(self):
        sub = self.x.root_params.get_tor_proxy_running_observable = MagicMock(return_value=False)
        result = self.x.is_tor_proxy_running()
        self.assertIs(result, False)

    def test_start_set_passphrase_routine_sets_passphrase_none(self):
        target = self.x.launch_alert_log = MagicMock()
        sub = self.x.home_dir_has_private_key = MagicMock(return_value=False)
        sub_new_key = self.x.new_key_button_clicked = MagicMock()
        obs_target = self.x.root_params.set_session_passphrase_observable = MagicMock()
        self.x.start_set_passphrase_routine()
        obs_target.assert_called_with(None)

    def test_start_set_passphrase_routine_calls_launch_get_session_passphrase_if_home_dir_has_private_key_is_true(self):
        sub = self.x.home_dir_has_private_key = MagicMock(return_value=True)
        target = self.x.launch_get_session_passphrase = MagicMock()
        self.x.start_set_passphrase_routine()
        target.assert_called_with()

    def test_start_set_passphrase_routine_launches_alert_and_new_key_popup_if_has_private_key_returns_false(self):
        no_key_msg = "No Private Key in Ring"
        sub = self.x.gpg_data_context.get_host_key = MagicMock(return_value=no_key_msg)
        sub_1 = self.x.home_dir_has_private_key = MagicMock(return_value=False)
        target_alert = self.x.launch_alert_log = MagicMock()
        target_new_key = self.x.new_key_button_clicked = MagicMock()
        self.x.start_set_passphrase_routine()
        self.assertTrue(target_alert.called)
        self.assertTrue(target_new_key.called)

    def test_home_dir_has_private_key_returns_false_if_no_key(self):
        no_key_msg = "No Private Key in Ring"
        sub = self.x.gpg_data_context.get_host_key = MagicMock(return_value=no_key_msg)
        result = self.x.home_dir_has_private_key()
        self.assertIs(result, False)

    def test_new_home_dir_returns_true_if_private_key_exists(self):
        key_msg = "xxxkeyid"
        sub = self.x.gpg_data_context.get_host_key = MagicMock(return_value=key_msg)
        result = self.x.home_dir_has_private_key()
        self.assertIs(result, True)

    @patch.object(gpgcontroller.popuplauncher, 'launch_get_session_passphrase_popup')
    def test_launch_get_session_passphrase_launches_popup_calls_verify_with_result(self, pop):
        val = 'xxx'
        pop.return_value = val
        target = self.x.verify_session_passphrase = MagicMock()
        self.x.launch_get_session_passphrase()
        pop.assert_called_with(self.x.root)
        target.assert_called_with(pop.return_value)

    @patch.object(gpgcontroller.popuplauncher, 'launch_get_session_passphrase_popup')
    def test_launch_get_session_passphrase_launches_popup_sets_passphrase_obs_none_does_nothing_if_result_none(self, pop):
        val = 'xxx'
        pop.return_value = None
        target = self.x.verify_session_passphrase = MagicMock()
        obs_target = self.x.root_params.set_session_passphrase_observable = MagicMock()
        self.x.launch_get_session_passphrase()
        pop.assert_called_with(self.x.root)
        self.assertFalse(target.called)
        obs_target.assert_called_with(None)

    @patch.object(gpgcontroller.passphrasevalidator, 'PassphraseValidator')
    def test_verify_session_passphrase_inits_validator_with_args(self, validator):
        passphrase_val = 'passphrase'
        homedir_val = 'home_dir_val'
        host_key_id_val = 'host_key_id_val'
        sub_alert = self.x.launch_alert_log = MagicMock()
        sub_launch_passphrase = self.x.launch_get_session_passphrase = MagicMock()
        home_dir = self.x.gpg_data_context.get_home_dir = MagicMock(return_value=homedir_val)
        key_id = self.x.gpg_data_context.get_host_key_id = MagicMock(return_value=host_key_id_val)
        self.x.verify_session_passphrase(passphrase_val)
        validator.assert_called_with(home_dir.return_value, key_id.return_value, passphrase_val)

    @patch.object(gpgcontroller.passphrasevalidator, 'PassphraseValidator')
    def test_verify_session_passphrase_calls_validate_on_validator(self, validator):
        class MockValidator:
            result = types.SimpleNamespace(stderr='wtfwtf')
            validate = MagicMock()

        passphrase_val = 'passphrase'
        validator.return_value = MockValidator()
        validate = validator.return_value.validate
        sub_alert = self.x.launch_alert_log = MagicMock()
        sub_launch_passphrase = self.x.launch_get_session_passphrase = MagicMock()
        self.x.verify_session_passphrase(passphrase_val)
        self.assertTrue(validate.called)

    @patch.object(gpgcontroller.passphrasevalidator, 'PassphraseValidator')
    def test_verify_session_passphrase_calls_alert_and_relaunches_passphrase_if_validate_returns_false(self, validator):
        class MockValidator:
            result = types.SimpleNamespace(stderr='wtfwtf')
            validate = MagicMock(return_value=False)
        passphrase_val = 'passphrase'
        validator.return_value = MockValidator()
        validate = validator.return_value.validate
        target_alert = self.x.launch_alert_log = MagicMock()
        target_launch_passphrase = self.x.launch_get_session_passphrase = MagicMock()
        self.x.verify_session_passphrase(passphrase_val)
        self.assertTrue(target_alert.called)
        self.assertTrue(target_launch_passphrase.called)

    @patch.object(gpgcontroller.passphrasevalidator, 'PassphraseValidator')
    def test_verify_session_passphrase_sets_root_param_session_passphrase_if_validate_true(self, validator):
        class MockValidator:
            result = types.SimpleNamespace(stderr='wtfwtf')
            validate = MagicMock(return_value=True)
        passphrase_val = 'passphrase'
        validator.return_value = MockValidator()
        validate = validator.return_value.validate
        target = self.x.root_params.set_session_passphrase_observable = MagicMock()
        self.x.verify_session_passphrase(passphrase_val)
        target.assert_called_with(passphrase_val)

    def test_set_passphrase_button_clicked_calls_start_session_passphrase_routine(self):
        target = self.x.start_set_passphrase_routine = MagicMock()
        self.x.set_passphrase_button_clicked(None)
        target.assert_called_with()

    def test_get_keyid_from_view_option_var(self):
        name = 'get_keyid_from_view_option_var_widget'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_get_keyid_from_view_option_var_returns_keyid(self):
        formatted_key_string = 'mactower, <mactower@email.com>, 55A45A99FE45E540'
        target = '55A45A99FE45E540'
        mock_view_var = MagicMock()
        mock_view_var.get = MagicMock(return_value=formatted_key_string)
        result = self.x.get_keyid_from_view_option_var_widget(mock_view_var)
        self.assertEqual(result, target)

    def test_key_info_button_clicked_attribute(self):
        name = 'key_info_button_clicked'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_key_info_button_clicked_calls_view_var(self):
        self.x.get_keyid_from_view_option_var_widget = MagicMock()
        subject = self.x.get_keyid_from_view_option_var_widget
        self.x.key_info_button_clicked(None)
        subject.assert_called_with(self.x.view.key_info_option_var)

    @patch.object(gpgcontroller.popuplauncher, 'launch_key_info_popup')
    def test_key_info_button_returns_valid_key_with_valid_selection(self, func):
        func.return_value = dict(keyid=self.valid_keyid)
        self.x.get_keyid_from_view_option_var_widget = MagicMock(return_value=self.valid_keyid)
        final = self.x.key_info_button_clicked(None)
        self.assertEqual(final['keyid'], self.valid_keyid)

    @patch.object(gpgcontroller.popuplauncher, 'launch_key_info_popup')
    def test_key_info_button_launches_popup_with_valid_selection(self, func):
        self.x.get_keyid_from_view_option_var_widget = MagicMock(return_value=self.valid_keyid)
        final = self.x.key_info_button_clicked(None)
        self.assertTrue(func.called)

    def test_key_info_button_returns_none_with_no_valid_selection(self):
        self.x.get_keyid_from_view_option_var_widget = MagicMock(return_value='XXX')
        final = self.x.key_info_button_clicked(None)
        self.assertIsNone(final)

    def test_create_new_key_button_clicked_attribute(self):
        name = 'new_key_button_clicked'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch.object(gpgcontroller.popuplauncher, 'launch_new_key_popup')
    def test_new_key_button_returns_none_if_already_creating(self, pop):
        self.x.creating_new_key = True
        result = self.x.new_key_button_clicked(None)
        self.assertIsNone(result)

    @patch.object(gpgcontroller.popuplauncher, 'launch_new_key_popup')
    def test_new_key_button_prints_msg_if_already_creating(self, pop):
        self.x.creating_new_key = True
        sub = self.x.print_notification = MagicMock()
        result = self.x.new_key_button_clicked(None)
        self.assertTrue(sub.called)

    @patch.object(gpgcontroller.popuplauncher, 'launch_new_key_popup')
    def test_new_key_button_launches_popup_if_not_creating(self, pop):
        pop.return_value='hello there'
        self.x.create_new_key = MagicMock()
        result = self.x.new_key_button_clicked(None)
        pop.assert_called_with(self.root)

    @patch.object(gpgcontroller.popuplauncher, 'launch_new_key_popup')
    def test_new_key_button_returns_none_if_key_dict_is_none(self, pop):
        pop.return_value=None
        result = self.x.new_key_button_clicked(None)
        self.assertIsNone(result)

    @patch.object(gpgcontroller.popuplauncher, 'launch_new_key_popup')
    def test_new_key_button_returns_none_if_key_dict_is_none(self, pop):
        pop.return_value=None
        sub = self.x.print_notification = MagicMock()
        result = self.x.new_key_button_clicked(None)
        self.assertTrue(sub.called)

    @patch.object(gpgcontroller.popuplauncher, 'launch_new_key_popup')
    def test_new_key_button_clicked_sets_creating_new_key_var(self, pop):
        pop.return_value=dict()
        self.x.create_new_key = MagicMock()
        sub = self.x.print_notification = MagicMock()
        result = self.x.new_key_button_clicked(None)
        self.assertTrue(self.x.creating_new_key)

    @patch.object(gpgcontroller.popuplauncher, 'launch_new_key_popup')
    def test_new_key_button_clicked_calls_create_new_key_on_valid(self, pop):
        pop.return_value = dict(data='hello')
        sub = self.x.create_new_key = MagicMock()
        result = self.x.new_key_button_clicked(None)
        sub.assert_called_with(pop.return_value)

    def test_create_new_key_method_attribute(self):
        name = 'create_new_key'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch.object(gpgcontroller.keycreator, 'KeyCreator')
    def test_create_new_key_method_initializes_keycreator(self, agent):
        key_input = dict(data='hello')
        agent.gpg.gen_key_input = MagicMock()
        agent.gpg.gen_key = MagicMock()
        self.x.create_new_key(key_input)
        agent.assert_called_with(self.x.gpg_data_context.get_home_dir(), self.x.queue)

    @patch.object(gpgcontroller.keycreator.KeyCreator, 'execute')
    def test_create_new_key_method_calls_execute_on_keycreator(self, method):
        val = '123'
        self.x.create_new_key(val)
        method.assert_called_with(val)

    @patch.object(gpgcontroller.keycreator, 'KeyCreator')
    @patch.object(gpgcontroller.keycreator.KeyCreator, 'execute')
    def test_create_new_key_method_prints_msg(self, execute, keycreator):
        sub = self.x.print_notification = MagicMock()
        keycreator.gpg.gen_key_input = MagicMock()
        keycreator.gpg.gen_key = MagicMock()
        result = self.x.create_new_key(None)
        self.assertTrue(sub.called)

    @patch.object(gpgcontroller.popuplauncher, 'DeleteKeyController')
    @patch.object(gpgcontroller.popuplauncher, 'launch_delete_key_popup')
    def test_delete_key_button_clicked_calls_get_raw_key_list(self, pop, controller):
        sub = self.x.gpg_data_context.get_raw_key_list = MagicMock(return_value=[1])
        pop.return_value = None
        self.x.delete_key_button_clicked(None)
        self.assertTrue(sub.called)

    @unittest.skip("TEST FAILS DUE TO GPG PROBLEM, SKIP FOR REFACTORING")
    @patch.object(gpgcontroller.popuplauncher, 'DeleteKeyController')
    @patch.object(gpgcontroller.popuplauncher, 'launch_delete_key_popup')
    def test_delete_key_button_launches_popup(self, pop, controller):
        stub = controller.show = MagicMock()
        pop.return_value='hello there'
        sub = self.x.gpg_data_context.get_raw_key_list = MagicMock(return_value=['one'])
        result = self.x.delete_key_button_clicked(None)
        pop.assert_called_with(self.root, sub.return_value)


    @patch.object(gpgcontroller.popuplauncher, 'DeleteKeyController')
    @patch.object(gpgcontroller.popuplauncher, 'launch_delete_key_popup')
    def test_if_delete_key_popup_returns_none_print_message_returns_none(self, pop, controller):
        msg = 'Delete Keys Cancelled'
        sub = pop.return_value=None
        target = self.x.print_notification = MagicMock()
        result = self.x.delete_key_button_clicked(None)
        target.assert_called_with(msg)
        self.assertIsNone(result)

    @patch.object(gpgcontroller.popuplauncher, 'DeleteKeyController')
    @patch.object(gpgcontroller.popuplauncher, 'launch_delete_key_popup')
    @patch.object(gpgcontroller.keydeleter, 'KeyDeleter')
    def test_delete_key_method_initializes_keydeleter_if_target_not_none(self, agent, pop, controller):
        agent.gpg = MagicMock()
        agent.gpg.delete_keys = MagicMock()
        agent.execute = MagicMock()
        val = [1]
        sub = gpgcontroller.popuplauncher.launch_delete_key_popup = MagicMock(return_value=val)
        self.x.delete_key_button_clicked(None)
        agent.assert_called_with(self.x.gpg_data_context.get_home_dir())

    @patch.object(gpgcontroller.popuplauncher, 'DeleteKeyController')
    @patch.object(gpgcontroller.popuplauncher, 'launch_delete_key_popup')
    @patch.object(gpgcontroller.keydeleter.KeyDeleter, 'execute')
    def test_delete_key_method_prints_if_deleter_returns_ok(self, execute, pop, controller):

        class FakeTrueReturn:
            status = 'ok'
            stderr = 'stderr message'

        execute.return_value = FakeTrueReturn()
        target_1 = self.x.print_notification = MagicMock()
        target_2 = self.x.append_notification = MagicMock()
        target_3 = self.x.key_list_observable.set = MagicMock()
        self.x.delete_key_button_clicked(None)
        self.assertTrue(target_1.called)
        target_2.assert_called_with(FakeTrueReturn.stderr)
        self.assertTrue(target_3.called)

    @patch.object(gpgcontroller.popuplauncher, 'DeleteKeyController')
    @patch.object(gpgcontroller.popuplauncher, 'launch_delete_key_popup')
    @patch.object(gpgcontroller.keydeleter.KeyDeleter, 'execute')
    def test_delete_key_method_prints_if_deleter_returns_ok(self, execute, pop, controller):

        class FakeTrueReturn:
            status = 'ok'
            stderr = 'stderr message'

        execute.return_value = FakeTrueReturn()
        target_1 = self.x.print_notification = MagicMock()
        target_2 = self.x.append_notification = MagicMock()
        target_3 = self.x.gpg_data_context.set_key_list = MagicMock()
        target_4 = self.x.gpg_data_context.set_host_key = MagicMock()
        self.x.delete_key_button_clicked(None)
        self.assertTrue(target_1.called)
        target_2.assert_called_with(FakeTrueReturn.stderr)
        self.assertTrue(target_3.called)
        self.assertTrue(target_4.called)


class TestGPGControllerEventBindings(gpgcontrollersetupclass.TestGPGControllerSetupClass):

    home = 'tests/data/keys'
    althome = 'tests/data/altkeys'
    key_ring = keyring.KeyRing(home)
    key_dir = 'tests/data/keys'

    def test_config_event_bindings_attribute(self):
        name = 'config_event_bindings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch('gpg.gpgcontroller.GPGController.config_event_bindings')
    def test_constructor_calls_config_event_bindings(self, mocked_method):
        self.x = gpgcontroller.GPGController(self.root_params, self.data_context)
        self.assertTrue(mocked_method.called)

    def test_view_homedir_entry_bind_called(self):
        self.assertTrue(self.x.view.home_dir_entry.bind.called)

    def test_view_homedir_entry_bind_called_with(self):
        self.x.view.home_dir_entry.bind.assert_called_with(self.command, self.x.homedir_entry_clicked)

    def test_view_keyinfo_button_bind_called(self):
        self.assertTrue(self.x.view.key_info_button.bind.called)

    def test_view_keyinfo_button_bind_called_with(self):
        self.x.view.key_info_button.bind.assert_called_with(self.command, self.x.key_info_button_clicked)

    def test_view_create_new_key_button_bind_called_with(self):
        self.x.view.new_key_button.bind.assert_called_with(self.command, self.x.new_key_button_clicked)

    def test_view_delete_key_button_bind_called_with(self):
        self.x.view.delete_key_button.bind.assert_called_with(self.command, self.x.delete_key_button_clicked)

    def test_view_set_passphrase_button_bind_called_with(self):
        self.x.view.set_passphrase_button.bind.assert_called_with(self.command, self.x.set_passphrase_button_clicked)


"""
test_consolecontroller.py

Test suite for the Console Controller module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
import tkinter
from disappeer.console import consolecontroller
import tkinter.filedialog
from disappeer.models import gpgdatacontext
from disappeer.gpg.agents import gpgclient
from disappeer.popups import popuplauncher
from disappeer.root import rootparameters
from disappeer.models.db import databasefacade
import functools
import copy


class SetUpClass(unittest.TestCase):
    """
    Using class attributes for static setup objects is slightly faster for setup.
    """

    func_list = ['Encrypt', 'Decrypt', 'Import', 'Export', 'Sign', 'Verify']
    command = "<ButtonRelease-1>"
    root = MagicMock(spec=tkinter.Tk())
    root_view = MagicMock()
    queue = MagicMock()
    database_facade = MagicMock(spec=databasefacade.DatabaseFacade)
    mock_observer = MagicMock()
    root_params = rootparameters.RootParameters(root, root_view, queue, database_facade,
                                                     mock_observer)
    mock_view_method = root_params.get_console_frame = MagicMock(return_value=MagicMock())
    view = mock_view_method.return_value
    key_dir = 'tests/data/keys'
    data_context = gpgdatacontext.GPGDataContext(key_dir)

    def setUp(self):
        self.data_context = copy.deepcopy(self.data_context)
        self.x = consolecontroller.ConsoleController(self.root_params,
                                                     self.data_context)


class TestImports(unittest.TestCase):

    def test_filedialog(self):
        self.assertEqual(tkinter.filedialog, consolecontroller.tkinter.filedialog)

    def test_gpg_client(self):
        self.assertEqual(gpgclient, consolecontroller.gpgclient)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, consolecontroller.popuplauncher)

    def test_functools(self):
        self.assertEqual(functools, consolecontroller.functools)


class TestControllerBasics(SetUpClass):

    def test_instance(self):
        self.assertIsInstance(self.x, consolecontroller.ConsoleController)

    def test_root_params_attr_set(self):
        self.assertEqual(self.root_params, self.x.root_params)

    def test_gpg_client_attribute(self):
        self.assertIsInstance(self.x.gpg_client, gpgclient.GPGClient)

    def test_gpg_client_key_dir_is_data_context_home_dir(self):
        self.assertEqual(self.x.gpg_client.key_dir, self.x.gpg_data_context.get_home_dir())

    def test_gpg_function_list_attribute(self):
        self.assertEqual(self.x.func_list, self.func_list)

    def test_running_job_attribute(self):
        self.assertFalse(self.x.running_job)

    def test_print_to_console_method(self):
        msg = "hello"
        sub = self.x.view.print_to_console_text_box = MagicMock()
        self.x.print_to_console(msg)
        sub.assert_called_with(msg)

    def test_config_menubar_configs_menu(self):
        mock_menu = MagicMock()
        target = self.x.root_params.get_file_menu_obj = MagicMock(return_value=mock_menu)
        self.x.config_menubar()
        target.assert_called_with()
        self.assertTrue(mock_menu.add_command.called)

    @patch.object(consolecontroller.ConsoleController, 'config_menubar')
    def test_constructor_calls_config_menubar(self, mocked_method):
        x = consolecontroller.ConsoleController(self.root_params,
                                                self.data_context)
        self.assertTrue(mocked_method.called)



class TestControllerConsoleFileHandlingButtonMethods(SetUpClass):

    @patch('console.consolecontroller.tkinter.filedialog')
    def test_save_button_clicked(self, wtf):
        sub = self.x.view.get_console_text = MagicMock()
        self.x.save_button_clicked(None)
        sub.assert_called_with()

    @patch('console.consolecontroller.tkinter.filedialog')
    def test_save_button_asks_save_file(self, target):
        target.asksaveasfile = MagicMock()
        self.x.save_button_clicked(None)
        self.assertTrue(target.asksaveasfile.called)

    @patch('console.consolecontroller.tkinter.filedialog.asksaveasfile')
    def test_save_button_returns_none_if_filedialog_none(self, target):
        target.return_value = None
        result = self.x.save_button_clicked(None)
        self.assertIsNone(result)

    @unittest.skip('Figure out how to patch/mock the calls to write and close file')
    def test_save_button_writes_file(self):
        pass

    @patch('disappeer.console.consolecontroller.tkinter')
    def test_open_button_asks_open_file(self, target):
        result = self.x.open_button_clicked(None)
        self.assertTrue(target.filedialog.askopenfile.called)

    @patch('disappeer.console.consolecontroller.tkinter')
    def test_open_button_returns_none_if_ask_open_returns_none(self, target):
        target.return_value = None
        result = self.x.open_button_clicked(None)
        self.assertIsNone(result)

    @patch('disappeer.console.consolecontroller.tkinter')
    def test_open_button_prints_to_console_if_ask_open_not_none(self, target):
        target.return_value = True
        sub = self.x.view.print_to_console_text_box = MagicMock()
        result = self.x.open_button_clicked(None)
        self.assertTrue(sub.called)

    def test_clear_console_button_clears_console(self):
        sub = self.x.view.clear_console_text_box = MagicMock()
        self.x.clear_button_clicked(None)
        self.assertTrue(sub.called)


class TestConsoleControllerEventBindingsAndDataContext(SetUpClass):

    def test_config_event_bindings_attribute(self):
        name = 'config_event_bindings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch('disappeer.console.consolecontroller.ConsoleController.config_event_bindings')
    def test_constructor_calls_config_event_bindings(self, mocked_method):
        self.x = consolecontroller.ConsoleController(self.root_params, self.data_context)
        self.assertTrue(mocked_method.called)

    def test_view_save_button_bind_called_with(self):
        self.x.view.save_button.bind.assert_called_with(self.command, self.x.save_button_clicked)

    def test_view_open_button_bind_called_with(self):
        self.x.view.open_button.bind.assert_called_with(self.command, self.x.open_button_clicked)

    def test_view_clear_button_bind_called_with(self):
        self.x.view.clear_button.bind.assert_called_with(self.command, self.x.clear_button_clicked)

    def test_view_run_button_bind_called_with(self):
        self.x.view.run_button.bind.assert_called_with(self.command, self.x.run_button_clicked)

    def test_config_data_context_attribute(self):
        name = 'config_data_context'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch('disappeer.console.consolecontroller.ConsoleController.config_data_context')
    def test_constructor_calls_config_data_context(self, mocked_method):
        self.x = consolecontroller.ConsoleController(self.root_params, self.data_context)
        self.assertTrue(mocked_method.called)

    def test_config_data_context_adds_view_key_list_handler_to_list_observable(self):
        self.assertIn(self.x.view.key_info_dropdown_handler, self.x.gpg_data_context.key_list_observable.observer_list)

    def test_config_data_context_adds_gpg_client_to_data_context_as_data_context_home_dir_observer(self):
        self.assertIn(self.x.gpg_client, self.x.gpg_data_context.home_dir_observable.observer_list)

    def test_config_data_context_sets_view_func_list_to_controller_func_list(self):
        sub = self.x.view.console_function_dropdown_handler.set = MagicMock()
        self.x.config_data_context()
        sub.assert_called_with(self.func_list)


class TestConsoleRunButtonAndRelated(SetUpClass):

    def test_get_selected_key_helper_method(self):
        val = 'hah 1234'
        target = val.split()[-1]
        sub = self.view.console_key_option_var.get = MagicMock(return_value=val)
        result = self.x.get_selected_key()
        self.assertEqual(target, result)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_get_selected_key_helper_method_alerts_on_fail(self, mocked):
        val = 'Public Keys'
        target = val.split()[-1]
        sub = self.view.console_key_option_var.get = MagicMock(return_value=val)
        result = self.x.get_selected_key()
        self.assertTrue(mocked.called)
        self.assertIsNone(result)

    def test_get_selected_function_helper_method(self):
        val = 'hah'
        sub = self.view.console_function_option_var.get = MagicMock(return_value=val)
        result = self.x.get_selected_function()
        self.assertEqual(sub.return_value, result)

    def test_get_console_text_helper_method(self):
        sub = self.view.get_console_text = MagicMock(return_value='hello')
        result = self.x.get_console_text()
        self.assertEqual(sub.return_value, result)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_button_calls_function_helper(self, mocked):
        sub = self.x.get_selected_function = MagicMock()
        self.x.run_button_clicked(None)
        sub.assert_called_with()

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_button_launches_alert_if_running_job(self, mocked):
        self.x.running_job = True
        self.x.run_button_clicked(None)
        self.assertTrue(mocked.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_button_launches_alert_if_no_function_selected(self, mocked):
        sub = self.x.get_selected_function = MagicMock(return_value='bla')
        self.x.run_button_clicked(None)
        self.assertTrue(mocked.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_button_calls_run_encrypt_if_encrypt_selected(self, mocked):
        sub = self.x.get_selected_function = MagicMock(return_value='Encrypt')
        target_sub = self.x.run_encrypt = MagicMock()
        self.x.run_button_clicked(None)
        self.assertTrue(target_sub.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_button_calls_run_decrypt_if_decrypt_selected(self, mocked):
        sub = self.x.get_selected_function = MagicMock(return_value='Decrypt')
        target_sub = self.x.run_decrypt = MagicMock()
        self.x.run_button_clicked(None)
        self.assertTrue(target_sub.called)

    def test_run_button_calls_run_export_if_export_selected(self):
        sub = self.x.get_selected_function = MagicMock(return_value='Export')
        target_sub = self.x.run_export = MagicMock()
        self.x.run_button_clicked(None)
        self.assertTrue(target_sub.called)

    def test_run_button_calls_run_import_if_import_selected(self):
        sub = self.x.get_selected_function = MagicMock(return_value='Import')
        target_sub = self.x.run_import = MagicMock()
        self.x.run_button_clicked(None)
        self.assertTrue(target_sub.called)

    def test_run_button_calls_run_sign_if_sign_selected(self):
        sub = self.x.get_selected_function = MagicMock(return_value='Sign')
        target_sub = self.x.run_sign = MagicMock()
        self.x.run_button_clicked(None)
        self.assertTrue(target_sub.called)

    def test_run_button_calls_run_verify_if_verify_selected(self):
        sub = self.x.get_selected_function = MagicMock(return_value='Verify')
        target_sub = self.x.run_verify = MagicMock()
        self.x.run_button_clicked(None)
        self.assertTrue(target_sub.called)


class TestConsoleVerifyMethod(SetUpClass):
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_verify_method_calls_get_console_text(self, alert):
        msg = 'hello'
        target = self.x.get_console_text = MagicMock(return_value=msg)
        self.x.run_verify()
        self.assertTrue(target.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_verify_method_calls_gpg_client_verify(self, alert):
        msg = 'hello'
        sub = self.x.get_console_text = MagicMock(return_value=msg)
        target = self.x.gpg_client.verify = MagicMock()
        self.x.run_verify()
        self.assertTrue(target.called)
        target.assert_called_with(sub.return_value)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_verify_method_calls_gpg_client_verify(self, alert):
        msg = 'hello'
        sub = self.x.get_console_text = MagicMock(return_value=msg)
        target = self.x.gpg_client.verify = MagicMock()
        self.x.run_verify()
        self.assertTrue(target.called)
        self.assertTrue(alert.called)

class TestConsoleSignMethod(SetUpClass):
    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_method_calls_get_keyid(self, mocked, getpass):
        sub = self.x.get_selected_key = MagicMock()
        stub = self.x.gpg_client.sign = MagicMock()
        self.x.run_sign()
        self.assertTrue(sub.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_returns_none_if_keyid_is_none(self, mocked, getpass):
        sub = self.x.get_selected_key = MagicMock(return_value=None)
        stub = self.x.gpg_client.sign = MagicMock()
        result = self.x.run_sign()
        self.assertIsNone(result)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_calls_get_passphrase(self, alert, getpass):
        sub = self.x.get_selected_key = MagicMock(return_value='1233')
        stub = self.x.gpg_client.sign = MagicMock()
        result = self.x.run_sign()
        self.assertTrue(getpass.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_calls_get_passphrase(self, alert, getpass):
        sub = self.x.get_selected_key = MagicMock(return_value='1233')
        getpass.return_value = None
        stub = self.x.gpg_client.sign = MagicMock()
        result = self.x.run_sign()
        self.assertTrue(alert.called)
        self.assertIsNone(result)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_calls_get_console_text(self, alert, getpass):
        sub = self.x.get_selected_key = MagicMock(return_value='1233')
        getpass.return_value = True
        target = self.x.get_console_text = MagicMock()
        stub = self.x.gpg_client.sign = MagicMock()
        result = self.x.run_sign()
        self.assertTrue(target.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_calls_gpg_client_sign(self, alert, getpass):
        sub = self.x.get_selected_key = MagicMock(return_value='1233')
        getpass.return_value = 'pass'
        sub_1 = self.x.get_console_text = MagicMock(return_value='xxx')
        target = self.x.gpg_client.sign = MagicMock()
        result = self.x.run_sign()
        target.assert_called_with(sub_1.return_value, sub.return_value, getpass.return_value)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_prints_error_if_sign_result_none(self, alert, getpass):
        sub = self.x.get_selected_key = MagicMock(return_value='1233')
        getpass.return_value = 'pass'
        sub_1 = self.x.get_console_text = MagicMock(return_value='xxx')

        class MockResult:
            fingerprint = None
            stderr = 'errmessage'
        mock_result = MockResult()
        target = self.x.gpg_client.sign = MagicMock(return_value=mock_result)
        result = self.x.run_sign()
        self.assertTrue(alert.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_sign_prints_to_console_if_valid(self, alert, getpass):
        sub = self.x.get_selected_key = MagicMock(return_value='1233')
        getpass.return_value = 'pass'
        sub_1 = self.x.get_console_text = MagicMock(return_value='xxx')

        class MockResult:
            fingerprint = '1234'
            stderr = 'errmessage'
        mock_result = MockResult()
        stubb = self.x.gpg_client = MagicMock()
        stub = self.x.gpg_client.sign = MagicMock(return_value=mock_result)
        result = self.x.run_sign()
        target = self.x.print_to_console = MagicMock()
        result = self.x.run_sign()
        self.assertTrue(target.called)


class TestConsoleRunImportMethod(SetUpClass):

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_import_calls_get_console_text(self, alert):
        sub = self.x.get_console_text = MagicMock()
        sub_x = self.x.gpg_client.import_key = MagicMock()
        self.x.run_import()
        self.assertTrue(sub.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_import_calls_gpg_client_import(self, alert):
        pub_key = self.x.get_console_text = MagicMock(return_value='hello')
        sub = self.x.gpg_client.import_key = MagicMock()
        self.x.run_import()
        sub.assert_called_with(pub_key.return_value)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_import_alerts_on_no_import(self, alert):
        class MockResult:
            imported = 0
            stderr = 'ERR MSG'
        mock_result = MockResult()
        pub_key = self.x.get_console_text = MagicMock(return_value='hello')
        sub = self.x.gpg_client.import_key = MagicMock(return_value=mock_result)
        self.x.run_import()
        self.assertTrue(alert.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_import_alerts_on_success(self, alert):
        class MockResult:
            imported = 1
            stderr = 'ERR MSG'
        mock_result = MockResult()
        pub_key = self.x.get_console_text = MagicMock(return_value='hello')
        sub = self.x.gpg_client.import_key = MagicMock(return_value=mock_result)
        self.x.run_import()
        self.assertTrue(alert.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_import_alerts_on_success(self, alert):
        class MockResult:
            imported = 1
            stderr = 'ERR MSG'
        mock_result = MockResult()
        pub_key = self.x.get_console_text = MagicMock(return_value='hello')
        sub = self.x.gpg_client.import_key = MagicMock(return_value=mock_result)
        target = self.x.gpg_data_context.set_key_list = MagicMock()
        self.x.run_import()
        self.assertTrue(target.called)


class TestConsoleRunExportMethod(SetUpClass):

    def test_run_export_calls_get_selected_key(self):
        sub = self.x.get_selected_key = MagicMock()
        target = self.x.gpg_client.export_key = MagicMock(return_value='wwww')
        self.x.run_export()
        self.assertTrue(sub.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_export_launches_alert_if_no_key_selected(self, mocked):
        sub = self.x.get_selected_key = MagicMock(return_value='Keys')
        self.x.run_export()
        self.assertTrue(mocked.called)

    def test_run_export_calls_client_export_on_valid_key(self):
        sub = self.x.get_selected_key = MagicMock()
        sub.return_value = '55A45A99FE45E540'
        target = self.x.gpg_client.export_key = MagicMock(return_value='wwww')
        self.x.run_export()
        self.assertTrue(target.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_export_alerts_on_fail(self, alert):
        sub = self.x.get_selected_key = MagicMock()
        sub.return_value = '55A45A99FE45E540'
        sub_1 = self.x.gpg_client.export_key = MagicMock(return_value='')
        self.x.run_export()
        self.assertTrue(alert.called)

    def test_run_export_prints_to_console_on_valid(self):
        sub = self.x.get_selected_key = MagicMock()
        sub.return_value = '55A45A99FE45E540'
        sub_1 = self.x.gpg_client.export_key = MagicMock(return_value='wwww')
        target = self.x.print_to_console = MagicMock()
        self.x.run_export()
        self.assertTrue(target.called)


class TestConsoleRunDecryptMethod(SetUpClass):
    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    def test_run_decrypt_launches_get_passphrase(self, mocked):
        sub = self.x.gpg_client = MagicMock()
        self.x.run_decrypt()
        self.assertTrue(mocked.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    def test_run_encrypt_launches_alert_if_passphrase_is_none(self, passphrase, alert):
        sub = self.x.gpg_client = MagicMock()
        passphrase.return_value = None
        self.x.run_decrypt()
        self.assertTrue(alert.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    def test_run_decrypt_gets_console_text_if_passphrase_not_none(self, mocked):
        sub = self.x.gpg_client = MagicMock()
        mocked.return_value = 'hello'
        target = self.x.get_console_text = MagicMock()
        self.x.run_decrypt()
        self.assertTrue(target.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    def test_run_decrypt_executes_decrypt(self, mocked):
        mocked.return_value = 'hello'
        console_text = self.x.get_console_text = MagicMock(return_value='wer')
        sub = self.x.gpg_client = MagicMock()
        target = self.x.gpg_client.decrypt = MagicMock()
        self.x.run_decrypt()
        self.assertTrue(target.called)
        target.assert_called_with(console_text.return_value, mocked.return_value)

    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    def test_run_decrypt_prints_on_success(self, mocked):
        mocked.return_value = 'hello'
        console_text = self.x.get_console_text = MagicMock(return_value='wer')
        sub = self.x.gpg_client = MagicMock()
        class MockResult:
            ok = True
        stub = self.x.gpg_client.decrypt = MagicMock(return_value=MockResult())
        target = self.x.print_to_console = MagicMock()
        self.x.run_decrypt()
        self.assertTrue(target.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    @patch.object(consolecontroller.popuplauncher, 'launch_get_passphrase_popup')
    def test_run_decrypt_alerts_on_fail(self, mocked, alert):
        mocked.return_value = 'hello'
        console_text = self.x.get_console_text = MagicMock(return_value='wer')
        sub = self.x.gpg_client = MagicMock()
        class MockResult:
            ok = False
            stderr = 'Errr mess'
        resut = MockResult()
        stub = self.x.gpg_client.decrypt = MagicMock(return_value=resut)
        target = self.x.print_to_console = MagicMock()
        self.x.run_decrypt()
        self.assertTrue(alert.called)


class TestConsoleRunEncryptMethod(SetUpClass):

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_encrypt_launches_alert_if_no_key_selected(self, mocked):
        sub = self.x.get_selected_key = MagicMock(return_value='Keys')
        self.x.run_encrypt()
        self.assertTrue(mocked.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_encrypt_returns_none_if_no_key_selected(self, mocked):
        sub = self.x.get_selected_key = MagicMock(return_value='Keys')
        result = self.x.run_encrypt()
        self.assertIsNone(result)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_encrypt_gets_console_text_on_valid_key(self, mocked):
        sub_0 = self.x.get_selected_key = MagicMock(return_value=True)
        sub = self.x.get_console_text = MagicMock()
        result = self.x.run_encrypt()
        self.assertTrue(sub.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_encrypt_calls_client_encrypt_with_plaintext_and_key(self, mocked):
        sub_1 = self.x.get_selected_key = MagicMock(return_value='keyid')
        sub = self.x.get_console_text = MagicMock(return_value='plaintext')
        target = self.x.gpg_client.encrypt = MagicMock()
        result = self.x.run_encrypt()
        target.assert_called_with(sub.return_value, sub_1.return_value)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_encrypt_prints_error_on_none_encrypt_result(self, mocked):
        sub_1 = self.x.get_selected_key = MagicMock(return_value='keyid')
        sub = self.x.get_console_text = MagicMock(return_value='plaintext')
        target = self.x.gpg_client.encrypt = MagicMock(return_value=None)
        final = self.x.run_encrypt()
        self.assertTrue(mocked.called)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_encrypt_prints_error_on_none_encrypt_result(self, mocked):
        sub_1 = self.x.get_selected_key = MagicMock(return_value=True)
        sub = self.x.get_console_text = MagicMock(return_value='plaintext')
        target = self.x.print_to_console = MagicMock()
        class MockResult:
            ok = True
        encrypted = self.x.gpg_client.encrypt = MagicMock()
        encrypted.return_value = MockResult()
        final = self.x.run_encrypt()
        target.assert_called_with(encrypted.return_value)

    @patch.object(consolecontroller.popuplauncher, 'launch_alert_box_popup')
    def test_run_encrypt_prints_error_on_none_encrypt_result(self, mocked):
        sub_1 = self.x.get_selected_key = MagicMock(return_value=True)
        sub = self.x.get_console_text = MagicMock(return_value='plaintext')
        target = self.x.print_to_console = MagicMock()
        class MockResult:
            ok = False
            stderr = 'Error Message'
        encrypted = self.x.gpg_client.encrypt = MagicMock()
        encrypted.return_value = MockResult()
        final = self.x.run_encrypt()
        self.assertTrue(mocked.called)

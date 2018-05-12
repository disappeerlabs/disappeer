"""
test_tornetcontroller.py

Test suite for TorNetController module and class object, view controller for TorNetFrame

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.tornet import tornetcontroller
from disappeer.utilities import queueconsumer
from disappeer.models import tordatacontext
from disappeer.net import networkservers
from disappeer.torproxy import torproxycontroller
from disappeer.constants import constants
import queue
import tkinter
from disappeer.root import rootparameters
from disappeer.root import rootview
from disappeer.utilities import logger
from disappeer.utilities.logger import log
from disappeer.models.db import databasefacade
from disappeer.popups import popuplauncher



class TestImports(unittest.TestCase):

    def test_queueconsumer(self):
        self.assertEqual(queueconsumer, tornetcontroller.queueconsumer)

    def test_networkservers(self):
        self.assertEqual(networkservers, tornetcontroller.networkservers)

    def test_torproxycontroller(self):
        self.assertEqual(torproxycontroller, tornetcontroller.torproxycontroller)

    def test_constants(self):
        self.assertEqual(constants, tornetcontroller.constants)

    def test_logger(self):
        self.assertEqual(logger, tornetcontroller.logger)

    def test_log(self):
        self.assertEqual(logger.log, tornetcontroller.log)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, tornetcontroller.popuplauncher)


class TestClassBasics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.command = "<ButtonRelease-1>"
        cls.root = tkinter.Tk()

    def setUp(self):
        # USE SETUPCLASS INSTEAD OF INSTANTIATING ROOT TK IN SETUP, takes less time
        # self.command = "<ButtonRelease-1>"
        # self.root = tkinter.Tk()
        self.root_view = MagicMock()
        self.queue = MagicMock()
        self.database_facade = MagicMock(spec=databasefacade.DatabaseFacade)
        self.mock_observer = MagicMock()
        self.root_params = rootparameters.RootParameters(self.root, self.root_view, self.queue, self.database_facade, self.mock_observer)
        self.view = self.root_params.get_tor_net_frame()
        self.mock_method = MagicMock()
        self.tor_datacontext = tordatacontext.TorDataContext(self.mock_method)
        self.x = tornetcontroller.TorNetController(self.root_params, self.tor_datacontext)

    def test_instance(self):
        self.assertIsInstance(self.x, tornetcontroller.TorNetController)

    def test_instance_queue_consumer(self):
        self.assertIsInstance(self.x, queueconsumer.QueueConsumer)

    def test_root_params_attr_set(self):
        self.assertEqual(self.x.root_params, self.root_params)

    def test_root_attribute_set(self):
        self.assertEqual(self.root, self.x.root)

    def test_view_attribute_set(self):
        self.assertEqual(self.view, self.x.view)

    def test_root_queue_attribute_set(self):
        self.assertEqual(self.queue, self.x.root_queue)

    def test_queue_consume_queue_attribute(self):
        check = hasattr(self.x, 'queue')
        self.assertTrue(check)
        self.assertIsInstance(self.x.queue, queue.Queue)

    def test_has_handle_queue_payload_method_attribute(self):
        self.x.handle_queue_payload(dict(desc=''))

    def test_tor_datacontext_attr_set(self):
        self.assertEqual(self.x.tor_datacontext, self.tor_datacontext)

    def test_tor_proxy_controller_attr_set(self):
        self.assertIsInstance(self.x.tor_proxy_controller, torproxycontroller.TorProxyController)
        self.assertEqual(self.x.queue, self.x.tor_proxy_controller.queue)

    def test_init_patches_contact_response_server_get_sync_db_path_with_database_facade_method(self):
        self.assertEqual(tornetcontroller.networkservers.contactresponseserver.SSLThreadedContactResponseTCPServer.get_sync_db_path, self.x.root_params.database_facade.get_server_sync_db_path)

    def test_net_servers_attr_set_with_root_queue(self):
        self.assertIsInstance(self.x.net_servers, networkservers.NetworkServers)
        self.assertEqual(self.x.net_servers.queue, self.x.root_queue)

    def test_config_event_bindings_calls_bind_on_net_server_on_button(self):
        target = self.view.net_server_on_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.command, self.x.net_server_radio_button_clicked)

    def test_config_event_bindings_calls_bind_on_net_server_off_button(self):
        target = self.view.net_server_off_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.command, self.x.net_server_radio_button_clicked)

    def test_config_event_bindings_calls_bind_on_tor_proxy_on_button(self):
        target = self.view.tor_proxy_on_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.command, self.x.tor_proxy_radio_button_clicked)

    def test_config_event_bindings_calls_bind_on_tor_proxy_off_button(self):
        target = self.view.tor_proxy_off_button.bind = MagicMock()
        self.x.config_event_bindings()
        target.assert_called_with(self.command, self.x.tor_proxy_radio_button_clicked)

    @patch('disappeer.tornet.tornetcontroller.TorNetController.config_event_bindings')
    def test_constructor_calls_config_event_bindings(self, mocked_method):
        self.x = tornetcontroller.TorNetController(self.root_params, self.tor_datacontext)
        self.assertTrue(mocked_method.called)

    def test_config_data_context_adds_view_request_onion_entry_var_to_tor_datacontext_req_addr_observer(self):
        target_method = self.x.tor_datacontext.add_tor_request_proxy_addr_observer = MagicMock()
        target_arg = self.x.view.request_onion_entry_var = MagicMock()
        self.x.config_data_context()
        target_method.assert_called_with(target_arg)

    def test_config_data_context_adds_view_response_onion_entry_var_to_tor_datacontext_res_addr_observer(self):
        target_method = self.x.tor_datacontext.add_tor_response_proxy_addr_observer = MagicMock()
        target_arg = self.x.view.response_onion_entry_var = MagicMock()
        self.x.config_data_context()
        target_method.assert_called_with(target_arg)

    def test_config_data_context_adds_view_message_onion_entry_var_to_tor_datacontext_msg_addr_observer(self):
        target_method = self.x.tor_datacontext.add_tor_message_proxy_addr_observer = MagicMock()
        target_arg = self.x.view.message_onion_entry_var = MagicMock()
        self.x.config_data_context()
        target_method.assert_called_with(target_arg)

    def test_config_data_context_adds_session_passphrase_observable_callback_to_root_params_session_passphrase_obs(self):
        target_method = self.x.root_params.add_session_passphrase_observable_callback = MagicMock()
        target_arg = self.x.session_passphrase_observable_callback = MagicMock()
        self.x.config_data_context()
        target_method.assert_called_with(target_arg)

    @patch('disappeer.tornet.tornetcontroller.TorNetController.config_data_context')
    def test_constructor_calls_config_data_context(self, mocked_method):
        self.x = tornetcontroller.TorNetController(self.root_params, self.tor_datacontext)
        self.assertTrue(mocked_method.called)

    def test_net_server_radio_button_clicked_calls_start_services_if_on_clicked(self):
        sub = self.x.start_network_services = MagicMock()
        target = self.x.start_network_services = MagicMock()
        self.x.view.get_net_server_radio_var = MagicMock(return_value=1)
        self.x.net_server_radio_button_clicked(None)
        self.assertTrue(target.called)

    def test_net_server_radio_button_clicked_sets_status_var_if_on_clicked(self):
        sub = self.x.start_network_services = MagicMock()
        mocked = self.x.start_contact_services = MagicMock()
        target = self.x.view.set_net_server_status_var = MagicMock()
        self.x.view.get_net_server_radio_var = MagicMock(return_value=1)
        self.x.net_server_radio_button_clicked(None)
        target.assert_called_with('Running')

    def test_net_server_radio_button_clicked_calls_view_disable_enable_handler_if_on_clicked(self):
        sub = self.x.start_network_services = MagicMock()
        mocked = self.x.start_contact_services = MagicMock()
        sub = self.x.view.set_net_server_status_var = MagicMock()
        target = self.x.view.handle_net_server_on_clicked_actions = MagicMock()
        self.x.view.get_net_server_radio_var = MagicMock(return_value=1)
        self.x.net_server_radio_button_clicked(None)
        target.assert_called_with()

    def test_net_server_radio_button_clicked_checks_button_state_if_on_clicked(self):
        sub = self.x.start_network_services = MagicMock()
        mocked = self.x.start_contact_services = MagicMock()
        sub_1 = self.x.view.set_net_server_status_var = MagicMock()
        sub_2 = self.x.view.handle_net_server_on_clicked_actions = MagicMock()
        self.x.view.net_server_on_button = dict(state='disabled')
        self.x.view.get_net_server_radio_var = MagicMock(return_value=1)
        self.x.net_server_radio_button_clicked(None)
        self.assertFalse(sub.called)

    def test_net_server_radio_button_clicked_calls_stop_services_if_off_clicked(self):
        target = self.x.stop_network_services = MagicMock()
        self.x.view.get_net_server_radio_var = MagicMock(return_value=0)
        self.x.net_server_radio_button_clicked(None)
        self.assertTrue(target.called)

    def test_net_server_radio_button_clicked_calls_proxy_threads_are_alive_if_off_clicked(self):
        sub = self.x.stop_network_services = MagicMock()
        target = self.x.proxy_threads_are_alive = MagicMock()
        self.x.view.get_net_server_radio_var = MagicMock(return_value=0)
        self.x.net_server_radio_button_clicked(None)
        self.assertTrue(target.called)

    def test_net_server_radio_button_clicked_sets_status_var_if_off_clicked(self):
        sub = self.x.stop_network_services = MagicMock()
        self.x.view.get_net_server_radio_var = MagicMock(return_value=0)
        target = self.x.view.set_net_server_status_var = MagicMock()
        self.x.net_server_radio_button_clicked(None)
        target.assert_called_with('Stopped')

    def test_net_server_radio_button_clicked_calls_view_disable_enable_handler_if_off_clicked(self):
        sub = self.x.stop_network_services = MagicMock()
        self.x.view.get_net_server_radio_var = MagicMock(return_value=0)
        sub = self.x.view.set_net_server_status_var = MagicMock()
        target = self.x.view.handle_net_server_off_clicked_actions = MagicMock()
        self.x.net_server_radio_button_clicked(None)
        target.assert_called_with()

    def test_start_network_services_calls_start_services_on_net_servers(self):
        target = self.x.net_servers.start_network_services = MagicMock()
        self.x.start_network_services()
        target.assert_called_with()

    def test_stop_network_services_calls_stop_services_on_net_servers(self):
        target = self.x.net_servers.stop_network_services = MagicMock()
        self.x.stop_network_services()
        target.assert_called_with()

    def test_tor_proxy_radio_button_clicked_calls_is_session_passphrase_none_returns_none_if_true(self):
        target = self.x.is_session_passphrase_none = MagicMock(return_value=True)
        result = self.x.tor_proxy_radio_button_clicked(None)
        self.assertTrue(target.called)
        self.assertIsNone(result)

    def test_tor_proxy_radio_button_clicked_calls_start_services_if_on_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        net_check_sub = self.x.check_network_servers = MagicMock()
        target = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        self.assertTrue(target.called)

    def test_tor_proxy_radio_button_clicked_calls_start_services_with_no_args_if_persist_false_if_on_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        target = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        sub = self.x.view.get_tor_proxy_persistent_checkbutton_var = MagicMock(return_value=0)
        net_check_sub = self.x.check_network_servers = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        target.assert_called_with()

    def test_tor_proxy_radio_button_clicked_calls_check_network_servers_if_on_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        target = self.x.check_network_servers = MagicMock()
        sub = self.x.view.get_tor_proxy_persistent_checkbutton_var = MagicMock(return_value=0)
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        target.assert_called_with()

    def test_tor_proxy_radio_button_clicked_calls_off_methods_and_returns_if_on_clicked_and_check_network_servers_false(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub_net = self.x.check_network_servers = MagicMock(return_value=False)
        sub = self.x.view.get_tor_proxy_persistent_checkbutton_var = MagicMock(return_value=0)
        target = self.x._update_tor_proxy_off_methods = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        self.assertFalse(sub.called)
        target.assert_called_with()

    def test_tor_proxy_radio_button_clicked_calls_proxy_threads_are_alive_if_on_clicked_calls_off_method_if_they_are(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub_net = self.x.check_network_servers = MagicMock(return_value=True)
        proxy_check = self.x.proxy_threads_are_alive = MagicMock(return_value=True)
        sub = self.x.view.get_tor_proxy_persistent_checkbutton_var = MagicMock(return_value=0)
        target = self.x._update_tor_proxy_off_methods = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        proxy_check.assert_called_with()
        self.assertFalse(sub.called)
        target.assert_called_with()

    def test_tor_proxy_radio_button_clicked_calls_start_services_with_persist_arg_from_check_button_and_current_tor_dir_if_on_clicked_and_persist_true(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        target = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        sub = self.x.view.get_tor_proxy_persistent_checkbutton_var = MagicMock(return_value=1)
        net_check_sub = self.x.check_network_servers = MagicMock()
        tor_dir_string = 'tor_dir_string'
        sub_2 = self.x.get_user_tor_keys_dir = MagicMock(return_value=tor_dir_string)
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        target.assert_called_with(persistent=sub.return_value, tor_key_dir=sub_2.return_value)

    def test_tor_proxy_radio_button_clicked_calls_disable_checkbutton_if_on_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        net_check_sub = self.x.check_network_servers = MagicMock()
        target = self.x.view.disable_tor_proxy_persistent_checkbutton = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        self.assertTrue(target.called)

    def test_tor_proxy_radio_button_clicked_sets_tor_proxy_status_vars_if_on_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        net_check_sub = self.x.check_network_servers = MagicMock()
        target_1 = self.x.view.set_tor_proxy_status_var = MagicMock()
        target_2 = self.x.root_params.set_tor_proxy_running_observable = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        self.x.tor_proxy_radio_button_clicked(None)
        target_1.assert_called_with('Running')
        target_2.assert_called_with(True)

    def test_tor_proxy_radio_button_clicked_calls_disable_enable_handler_if_on_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        sub_1 = self.x.view.set_tor_proxy_status_var = MagicMock()
        net_check_sub = self.x.check_network_servers = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        target = self.x.view.handle_tor_proxy_on_clicked_actions = MagicMock()
        self.x.tor_proxy_radio_button_clicked(None)
        target.assert_called_with()

    def test_tor_proxy_radio_button_clicked_checks_button_state_does_nothing_if_disabled_if_on_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        sub_1 = self.view.set_tor_proxy_status_var = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=1)
        sub_2 = self.x.view.handle_tor_proxy_on_clicked_actions = MagicMock()
        self.x.view.tor_proxy_on_button = dict(state='disabled')
        self.x.tor_proxy_radio_button_clicked(None)
        self.assertFalse(sub.called)

    def test_tor_proxy_radio_button_clicked_checks_button_state_does_nothing_if_disabled_if_off_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.stop_all_proxies = MagicMock()
        self.x.view.tor_proxy_off_button = dict(state='disabled')
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=0)
        self.x.tor_proxy_radio_button_clicked(None)
        self.assertFalse(sub.called)

    def test_tor_proxy_radio_button_clicked_calls_stop_services_if_off_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        target = self.x.tor_proxy_controller.stop_all_proxies = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=0)
        self.x.tor_proxy_radio_button_clicked(None)
        self.assertTrue(target.called)

    def test_tor_proxy_radio_button_clicked_sets_tor_proxy_status_vars_if_off_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.start_all_proxies = MagicMock()
        target_1 = self.x.view.set_tor_proxy_status_var = MagicMock()
        target_2 = self.x.root_params.set_tor_proxy_running_observable = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=0)
        self.x.tor_proxy_radio_button_clicked(None)
        target_1.assert_called_with('Stopped')
        target_2.assert_called_with(False)

    def test_tor_proxy_radio_button_clicked_calls_enable_checkbutton_if_off_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.stop_all_proxies = MagicMock()
        target = self.x.view.enable_tor_proxy_persistent_checkbutton = MagicMock()
        self.x.view.get_tor_proxy_radio_var = MagicMock(return_value=0)
        self.x.tor_proxy_radio_button_clicked(None)
        self.assertTrue(target.called)

    def test_tor_proxy_radio_button_clicked_calls_enable_disable_handler_if_off_clicked(self):
        sub_pass = self.x.is_session_passphrase_none = MagicMock(return_value=False)
        sub = self.x.tor_proxy_controller.stop_all_proxies = MagicMock()
        sub_1 = self.x.view.enable_tor_proxy_persistent_checkbutton = MagicMock()
        target = self.x.view.handle_tor_proxy_off_clicked_actions = MagicMock()
        self.view.get_tor_proxy_radio_var = MagicMock(return_value=0)
        self.x.tor_proxy_radio_button_clicked(None)
        target.assert_called_with()

    def test_check_network_servers_status_launches_alert_if_false(self):
        target = self.x.launch_alert_log = MagicMock()
        sub = self.x.net_servers.are_running = MagicMock(return_value=False)
        self.x.check_network_servers()
        self.assertTrue(target.called)

    def test_check_network_servers_status_returns_false_if_false(self):
        target = self.x.launch_alert_log = MagicMock()
        sub = self.x.net_servers.are_running = MagicMock(return_value=False)
        result = self.x.check_network_servers()
        self.assertIs(result, False)

    def test_check_network_servers_status_returns_true_if_true(self):
        # target = self.x.launch_alert_log = MagicMock()
        sub = self.x.net_servers.are_running = MagicMock(return_value=True)
        result = self.x.check_network_servers()
        self.assertIs(result, True)

    def test_proxy_threads_are_alive_returns_result_from_tor_proxy_controller_method(self):
        expected = False
        sub = self.x.tor_proxy_controller.is_any_alive = MagicMock(return_value=expected)
        result = self.x.proxy_threads_are_alive()
        sub.assert_called_with()
        self.assertIs(result, expected)

    def test_proxy_threads_are_alive_launches_alert_returns_true_if_any_thread_alive(self):
        expected = True
        sub = self.x.tor_proxy_controller.is_any_alive = MagicMock(return_value=expected)
        target = self.x.launch_alert_log = MagicMock()
        result = self.x.proxy_threads_are_alive()
        sub.assert_called_with()
        self.assertIs(result, expected)
        self.assertTrue(target.called)


    def test_handle_queue_payload_calls_handle_tor_proxy_request_server_with_given_payload(self):
        payload = dict(desc=constants.command_list.Tor_Proxy_Request_Server, address='address_string')
        target = self.x.handle_tor_proxy_request_server = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_tor_proxy_response_server_with_given_payload(self):
        payload = dict(desc=constants.command_list.Tor_Proxy_Response_Server, address='address_string')
        target = self.x.handle_tor_proxy_response_server = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_tor_proxy_message_server_with_given_payload(self):
        payload = dict(desc=constants.command_list.Tor_Proxy_Message_Server, address='address_string')
        target = self.x.handle_tor_proxy_message_server = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_tor_proxy_error_with_given_payload(self):
        payload = dict(desc=constants.command_list.Tor_Proxy_Error, name='proxy_name', error='proxy_error_object')
        target = self.x.handle_tor_proxy_error = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_tor_proxy_request_server_sets_data_context_observer(self):
        payload = dict(desc=constants.command_list.Tor_Proxy_Request_Server, address='address_string')
        self.x.handle_tor_proxy_request_server(payload)
        self.assertEqual(self.x.tor_datacontext.get_tor_request_proxy_addr(), payload['address'])

    def test_handle_tor_proxy_response_server_sets_root_and_net_attr(self):
        payload = dict(desc=constants.command_list.Tor_Proxy_Response_Server, address='address_string')
        self.x.handle_tor_proxy_response_server(payload)
        self.assertEqual(self.x.tor_datacontext.get_tor_response_proxy_addr(), payload['address'])

    def test_handle_tor_proxy_message_server_sets_root_and_net_attr(self):
        payload = dict(desc=constants.command_list.Tor_Proxy_Message_Server, address='address_string')
        self.x.handle_tor_proxy_message_server(payload)
        self.assertEqual(self.x.tor_datacontext.get_tor_message_proxy_addr(), payload['address'])

    def test_get_user_tor_keys_dir_calls_tor_data_context_method_with_result_from_root_params_method(self):
        key_id = 'key_id_string'
        target_1 = self.x.root_params.get_host_key_id = MagicMock(return_value=key_id)
        tor_key_dir = 'tor_key_dir_string'
        target_2 = self.x.tor_datacontext.get_user_tor_keys_dir = MagicMock(return_value=tor_key_dir)
        result = self.x.get_user_tor_keys_dir()
        target_1.assert_called_with()
        target_2.assert_called_with(target_1.return_value)
        self.assertEqual(result, target_2.return_value)

    def test_is_session_passphrase_none_launches_alert_returns_true_if_none(self):
        sub = self.x.root_params.get_session_passphrase_observable = MagicMock(return_value=None)
        target = self.x.launch_alert_log = MagicMock()
        result = self.x.is_session_passphrase_none()
        self.assertIs(result, True)
        self.assertTrue(target.called)

    def test_is_session_passphrase_none_returns_false_if_not_none(self):
        sub = self.x.root_params.get_session_passphrase_observable = MagicMock(return_value='xxxx')
        result = self.x.is_session_passphrase_none()
        self.assertIs(result, False)

    @patch.object(tornetcontroller.popuplauncher, 'launch_alert_box_popup')
    def test_launch_alert_log_launches_alert_and_log_with_msg(self, alertbox):
        msg = 'hello'
        self.x.launch_alert_log(msg)
        alertbox.assert_called_with(self.x.root, msg)

    def test_disable_tor_proxy_buttons(self):
        target_1 = self.x.view.disable_tor_proxy_on_button = MagicMock()
        target_2 = self.x.view.disable_tor_proxy_off_button = MagicMock()
        self.x.disable_tor_proxy_buttons()
        target_1.assert_called_with()
        target_2.assert_called_with()

    def test_enable_tor_proxy_buttons(self):
        target_1 = self.x.view.enable_tor_proxy_on_button = MagicMock()
        target_2 = self.x.view.enable_tor_proxy_off_button = MagicMock()
        self.x.enable_tor_proxy_buttons()
        target_1.assert_called_with()
        target_2.assert_called_with()

    def test_session_passphrase_observable_callback_disables_if_none(self):
        class MockObs:
            def get(self):
                return None
        obs = MockObs()
        target = self.x.disable_tor_proxy_buttons = MagicMock()
        self.x.session_passphrase_observable_callback(obs)
        target.assert_called_with()

    def test_session_passphrase_observable_callback_enables_if_not_none(self):
        class MockObs:
            def get(self):
                return 'sss'
        obs = MockObs()
        target = self.x.enable_tor_proxy_buttons = MagicMock()
        self.x.session_passphrase_observable_callback(obs)
        target.assert_called_with()

    def test_handle_tor_proxy_error_sets_view_on_connection_refused_for_tor_proxy_request_server(self):
        mock_error_dict = dict(desc=constants.command_list.Tor_Proxy_Error,
                               error=ConnectionRefusedError(111, 'Connection refused'),
                               name=constants.command_list.Tor_Proxy_Request_Server)
        target = self.x.view.set_tor_onion_request_addr = MagicMock()
        self.x.handle_tor_proxy_error(mock_error_dict)
        self.assertTrue(target.called)

    def test_handle_tor_proxy_error_sets_view_on_connection_refused_for_tor_proxy_respone_server(self):
        mock_error_dict = dict(desc=constants.command_list.Tor_Proxy_Error,
                               error=ConnectionRefusedError(111, 'Connection refused'),
                               name=constants.command_list.Tor_Proxy_Response_Server)
        target = self.x.view.set_tor_onion_response_addr = MagicMock()
        self.x.handle_tor_proxy_error(mock_error_dict)
        self.assertTrue(target.called)

    def test_handle_tor_proxy_error_sets_view_on_connection_refused_for_tor_proxy_message_server(self):
        mock_error_dict = dict(desc=constants.command_list.Tor_Proxy_Error,
                               error=ConnectionRefusedError(111, 'Connection refused'),
                               name=constants.command_list.Tor_Proxy_Message_Server)
        target = self.x.view.set_tor_onion_message_addr = MagicMock()
        self.x.handle_tor_proxy_error(mock_error_dict)
        self.assertTrue(target.called)


"""
test_torproxycontroller.py

Test suite for TorProxyController module and class object.
This object should contain refs to all tor server threads and control access to addresses etc.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.torproxy import torproxycontroller
from disappeer.torproxy import torproxyservice
from disappeer.constants import constants
import queue
from disappeer import settings


class TestImports(unittest.TestCase):

    def test_torproxyservice(self):
        self.assertEqual(torproxyservice, torproxycontroller.torproxyservice)

    def test_constants(self):
        self.assertEqual(constants, torproxycontroller.constants)

    def test_settings(self):
        self.assertEqual(settings, torproxycontroller.settings)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.queue = queue.Queue()
        self.x = torproxycontroller.TorProxyController(self.queue)

    def test_instance(self):
        self.assertIsInstance(self.x, torproxycontroller.TorProxyController)

    def test_queue_attribute_set(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_contact_req_thread_att_exists(self):
        name = 'request_proxy_thread'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_contact_res_thread_att_exists(self):
        name = 'response_proxy_thread'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_message_server_thread_att_exists(self):
        name = 'message_proxy_thread'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch.object(torproxycontroller.torproxyservice.TorProxyService, 'start')
    def test_start_request_proxy_thread_method_starts_with_args_persist_false(self, start_mock):
        name = constants.command_list.Tor_Proxy_Request_Server
        port = settings.port_contact_request_server
        persist_val = False
        self.x.start_request_proxy(persistent=persist_val)
        self.assertIsInstance(self.x.request_proxy_thread, torproxyservice.TorProxyServiceThread)
        self.assertTrue(start_mock.called)
        self.assertEqual(self.x.request_proxy_thread.proxy.name, name)
        self.assertEqual(self.x.request_proxy_thread.proxy.port, port)
        self.assertEqual(self.x.request_proxy_thread.proxy.queue, self.x.queue)
        self.assertEqual(self.x.request_proxy_thread.persistent, persist_val)

    @patch.object(torproxycontroller.torproxyservice.TorProxyService, 'start_persistent')
    def test_start_request_proxy_thread_method_starts_with_args_persist_true(self, start_mock):
        name = constants.command_list.Tor_Proxy_Request_Server
        port = settings.port_contact_request_server
        persist_val = True
        tor_dir_string = 'tor_dir_string'
        self.x.start_request_proxy(persistent=persist_val, tor_key_dir=tor_dir_string)
        self.assertIsInstance(self.x.request_proxy_thread, torproxyservice.TorProxyServiceThread)
        self.assertTrue(start_mock.called)
        self.assertEqual(self.x.request_proxy_thread.proxy.name, name)
        self.assertEqual(self.x.request_proxy_thread.proxy.port, port)
        self.assertEqual(self.x.request_proxy_thread.proxy.queue, self.x.queue)
        self.assertEqual(self.x.request_proxy_thread.persistent, persist_val)
        self.assertEqual(self.x.request_proxy_thread.tor_key_dir, tor_dir_string)

    @patch.object(torproxycontroller.torproxyservice.TorProxyService, 'start')
    def test_start_response_proxy_thread_method_starts_with_args_persist_false(self, start_mock):
        name = constants.command_list.Tor_Proxy_Response_Server
        port = settings.port_contact_response_server
        persist_val = False
        self.x.start_response_proxy(persistent=persist_val)
        self.assertIsInstance(self.x.response_proxy_thread, torproxyservice.TorProxyServiceThread)
        self.assertTrue(start_mock.called)
        self.assertEqual(self.x.response_proxy_thread.proxy.name, name)
        self.assertEqual(self.x.response_proxy_thread.proxy.port, port)
        self.assertEqual(self.x.response_proxy_thread.proxy.queue, self.x.queue)
        self.assertEqual(self.x.response_proxy_thread.persistent, persist_val)

    @patch.object(torproxycontroller.torproxyservice.TorProxyService, 'start_persistent')
    def test_start_response_proxy_thread_method_starts_with_args_persist_true(self, start_mock):
        name = constants.command_list.Tor_Proxy_Response_Server
        port = settings.port_contact_response_server
        persist_val = True
        tor_dir_string = 'tor_dir_string'
        self.x.start_response_proxy(persistent=persist_val, tor_key_dir=tor_dir_string)
        self.assertIsInstance(self.x.response_proxy_thread, torproxyservice.TorProxyServiceThread)
        self.assertTrue(start_mock.called)
        self.assertEqual(self.x.response_proxy_thread.proxy.name, name)
        self.assertEqual(self.x.response_proxy_thread.proxy.port, port)
        self.assertEqual(self.x.response_proxy_thread.proxy.queue, self.x.queue)
        self.assertEqual(self.x.response_proxy_thread.persistent, persist_val)
        self.assertEqual(self.x.response_proxy_thread.tor_key_dir, tor_dir_string)


    @patch.object(torproxycontroller.torproxyservice.TorProxyService, 'start')
    def test_start_message_proxy_thread_method_starts_with_args_persist_false(self, start_mock):
        name = constants.command_list.Tor_Proxy_Message_Server
        port = settings.port_message_server
        persist_val = False
        self.x.start_message_proxy(persistent=persist_val)
        self.assertIsInstance(self.x.message_proxy_thread, torproxyservice.TorProxyServiceThread)
        self.assertTrue(start_mock.called)
        self.assertEqual(self.x.message_proxy_thread.proxy.name, name)
        self.assertEqual(self.x.message_proxy_thread.proxy.port, port)
        self.assertEqual(self.x.message_proxy_thread.proxy.queue, self.x.queue)
        self.assertEqual(self.x.message_proxy_thread.persistent, persist_val)

    @patch.object(torproxycontroller.torproxyservice.TorProxyService, 'start_persistent')
    def test_start_message_proxy_thread_method_starts_with_args_persist_true(self, start_mock):
        name = constants.command_list.Tor_Proxy_Message_Server
        port = settings.port_message_server
        persist_val = True
        tor_dir_string = 'tor_dir_string'
        self.x.start_message_proxy(persistent=persist_val, tor_key_dir=tor_dir_string)
        self.assertIsInstance(self.x.message_proxy_thread, torproxyservice.TorProxyServiceThread)
        self.assertTrue(start_mock.called)
        self.assertEqual(self.x.message_proxy_thread.proxy.name, name)
        self.assertEqual(self.x.message_proxy_thread.proxy.port, port)
        self.assertEqual(self.x.message_proxy_thread.proxy.queue, self.x.queue)
        self.assertEqual(self.x.message_proxy_thread.persistent, persist_val)
        self.assertEqual(self.x.message_proxy_thread.tor_key_dir, tor_dir_string)

    def test_start_all_proxies_starts_all_proxies_with_persist_val_and_key_dir(self):
        targ_1 = self.x.start_request_proxy = MagicMock()
        targ_2 = self.x.start_response_proxy = MagicMock()
        targ_3 = self.x.start_message_proxy = MagicMock()
        persist_val = True
        key_dir = 'key_dir_string'
        self.x.start_all_proxies(persistent=persist_val, tor_key_dir=key_dir)
        targ_1.assert_called_with(persistent=persist_val, tor_key_dir=key_dir)
        targ_2.assert_called_with(persistent=persist_val, tor_key_dir=key_dir)
        targ_3.assert_called_with(persistent=persist_val, tor_key_dir=key_dir)

    def test_stop_all_proxies_calls_quit_on_all_proxy_threads_sets_none(self):
        targ_1 = self.x.request_proxy_thread = MagicMock()
        targ_2 = self.x.response_proxy_thread = MagicMock()
        targ_3 = self.x.message_proxy_thread = MagicMock()
        self.x.stop_all_proxies()
        self.assertTrue(targ_1.quit.called)
        self.assertTrue(targ_2.quit.called)
        self.assertTrue(targ_3.quit.called)

    def test_stop_all_proxies_does_nothing_if_thread_is_none_sets_none(self):
        targ_1 = self.x.request_proxy_thread = None
        targ_2 = self.x.response_proxy_thread = None
        targ_3 = self.x.message_proxy_thread = None
        result = self.x.stop_all_proxies()
        self.assertIsNone(result)

    def test_is_any_alive_calls_is_alive_on_all_threads(self):
        targ_1 = self.x.request_proxy_thread = MagicMock()
        targ_2 = self.x.response_proxy_thread = MagicMock()
        targ_3 = self.x.message_proxy_thread = MagicMock()
        result = self.x.is_any_alive()
        targ_1.is_alive.assert_called_with()
        targ_2.is_alive.assert_called_with()
        targ_3.is_alive.assert_called_with()

    def test_is_any_alive_returns_true_if_any_alive(self):
        req = self.x.request_proxy_thread = MagicMock()
        targ_1 = req.is_alive = MagicMock(return_value=True)
        res = self.x.response_proxy_thread = MagicMock()
        msg = self.x.message_proxy_thread = MagicMock()
        result = self.x.is_any_alive()
        self.assertIs(result, True)

    def test_is_any_alive_returns_false_if_all_dead(self):
        req = self.x.request_proxy_thread = MagicMock()
        targ_1 = req.is_alive = MagicMock(return_value=False)
        res = self.x.response_proxy_thread = MagicMock()
        targ_2 = res.is_alive = MagicMock(return_value=False)
        msg = self.x.message_proxy_thread = MagicMock()
        targ_3 = msg.is_alive = MagicMock(return_value=False)
        result = self.x.is_any_alive()
        self.assertIs(result, False)

    def test_is_any_alive_returns_false_if_all_none(self):
        result = self.x.is_any_alive()
        self.assertIs(result, False)


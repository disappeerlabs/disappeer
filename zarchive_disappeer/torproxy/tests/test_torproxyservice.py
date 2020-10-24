"""
test_torproxyservice.py

Test suite for TorProxyService and TorProxyServiceThread class objects, for running ephemeral hidden services

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.torproxy import torproxyservice
import threading
import stem
import queue
import types
import time
from disappeer import settings
import os
from disappeer.constants import constants
import stem.connection
import copy
from disappeer.utilities.logger import timer


class TestImports(unittest.TestCase):

    def test_threading(self):
        self.assertEqual(threading, torproxyservice.threading)

    def test_stem(self):
        self.assertEqual(stem, torproxyservice.stem)

    def test_stem_controller_attribute(self):
        from stem.control import Controller
        self.assertEqual(Controller, torproxyservice.Controller)

    def test_time(self):
        self.assertEqual(time, torproxyservice.time)

    def test_settings(self):
        self.assertEqual(settings, torproxyservice.settings)

    def test_os(self):
        self.assertEqual(os, torproxyservice.os)

    def test_constants(self):
        self.assertEqual(constants, torproxyservice.constants)


class TestTorProxyServiceClassBasics(unittest.TestCase):

    def setUp(self):
        self.name = 'ServiceName'
        self.port = 16663
        self.q = MagicMock() # queue.Queue()
        self.tor_key_dir_val = None
        self.x = torproxyservice.TorProxyService(self.name, self.port, self.q, tor_key_dir=self.tor_key_dir_val)
        # self.x = copy.deepcopy(self.valid_obj)
        self.mock_tor_data_dir_path = 'tests/data/tor_data/' + self.x.name
        self.x.key_file_path = MagicMock(return_value=self.mock_tor_data_dir_path)
        self.remove_mock_tor_key_file()

    def remove_mock_tor_key_file(self):
        if os.path.exists(self.mock_tor_data_dir_path):
            os.remove(self.mock_tor_data_dir_path)

    def create_mock_tor_key_file(self):
        with open(self.mock_tor_data_dir_path, 'a'):
            pass

    def test_instance(self):
        self.assertIsInstance(self.x, torproxyservice.TorProxyService)

    def test_name_attribute_set(self):
        self.assertEqual(self.x.name, self.name)

    def test_queue_attribute_set(self):
        self.assertEqual(self.x.queue, self.q)

    def test_port_attribute_set(self):
        self.assertEqual(self.x.port, self.port)

    def test_tor_key_dir_attr_set(self):
        self.assertEqual(self.x.tor_key_dir, self.tor_key_dir_val)

    def test_running_attribute_set(self):
        self.assertTrue(self.x.running)

    def test_controller_port_attribute_set(self):
        target = settings.port_tor_controller
        self.assertEqual(self.x.controller_port, target)

    def test_onion_address_obj_attribute_set_none(self):
        self.assertIsNone(self.x.onion_address_obj)

    def test_start_method_attribute(self):
        name = 'start'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_build_address_string_builds_and_returns_onion_address_string(self):
        mock_addr_obj = types.SimpleNamespace(service_id='service_id_string')
        self.x.onion_address_obj = mock_addr_obj
        suffix = '.onion'
        target = mock_addr_obj.service_id + suffix
        result = self.x.build_address_string()
        self.assertEqual(target, result)

    def test_build_payload_method_builds_payload_from_arg(self):
        target_string = 'hello'
        target_dict = dict(desc=self.x.name, address=target_string)

        result = self.x.build_payload(target_string)
        self.assertEqual(result, target_dict)

    def test_put_to_queue_method_puts_build_payload_result_to_queue(self):
        target_string = 'hello'
        target_method = self.x.queue = MagicMock()
        arg_targ = self.x.build_payload(target_string)
        self.x.put_to_queue(target_string)
        target_method.put.assert_called_with(arg_targ)

    def test_build_error_payload_method_builds_error_payload_from_arg(self):
        target_string = 'error_message_string'
        target_dict = dict(desc=constants.command_list.Tor_Proxy_Error, name=self.x.name, error=target_string)
        result = self.x.build_error_payload(target_string)
        self.assertEqual(result, target_dict)

    def test_put_error_to_queue_method_puts_build_error_payload_result_to_queue(self):
        target_string = 'hello'
        target_method = self.x.queue = MagicMock()
        arg_targ = self.x.build_error_payload(target_string)
        self.x.put_error_to_queue(target_string)
        target_method.put.assert_called_with(arg_targ)

    ##########################
    #  Refactor Method Tests #
    ##########################

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_get_controller_calls_control_from_port_with_args(self, sock, controller):
        result = self.x.get_controller()
        controller.from_port.assert_called_with(port=self.x.controller_port)

    @patch('torproxy.torproxyservice.stem.socket')
    def test_get_controller_returns_controller_on_valid(self, sock):
        result = self.x.get_controller()
        self.assertIsInstance(result, stem.control.Controller)

    @patch.object(torproxyservice.Controller, 'from_port')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_get_controller_calls_error_method_returns_none_on_error(self, sock, port):
        port.side_effect = stem.SocketError
        target = self.x.put_error_to_queue = MagicMock()
        result = self.x.get_controller()
        self.assertIsNone(result)
        self.assertTrue(target.called)

    def test_authenticate_controller_method_calls_authenticate_returns_controller(self):
        put_method = self.x.put_to_queue = MagicMock()
        target = self.x.controller = MagicMock()
        result = self.x.authenticate_controller()
        target.authenticate.assert_called_with()
        self.assertTrue(put_method.called)
        self.assertEqual(result, self.x.controller)

    def test_authenticate_controller_calls_error_method_returns_none_on_error(self):
        target = self.x.controller = MagicMock()
        target.authenticate = MagicMock(side_effect=stem.connection.IncorrectSocketType('mock error message'))
        err_method = self.x.put_error_to_queue = MagicMock()
        result = self.x.authenticate_controller()
        self.assertTrue(err_method.called)
        self.assertIsNone(result)

    def test_create_ephemeral_address_returns_onion_obj_on_valid(self):
        put_method = self.x.put_to_queue = MagicMock()
        controller = self.x.controller = MagicMock()
        target_method = controller.create_ephemeral_hidden_service = MagicMock(return_value=True)
        result = self.x.create_ephemeral_address()
        target_method.assert_called_with(self.x.port)
        self.assertTrue(put_method.called)
        self.assertIsNotNone(result)

    def test_create_ephemeral_address_calls_error_method_returns_none_on_error(self):
        err_method = self.x.put_to_queue = MagicMock()
        controller = self.x.controller = MagicMock()
        target_method = controller.create_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        result = self.x.create_ephemeral_address()
        self.assertTrue(err_method.called)
        self.assertIsNone(result)

    def test_remove_ephemeral_address_calls_remove_method_on_valid(self):
        put_method = self.x.put_to_queue = MagicMock()
        controller = self.x.controller = MagicMock()
        self.x.onion_address_obj = MagicMock()
        target_method = controller.remove_ephemeral_hidden_service = MagicMock(return_value=True)
        result = self.x.remove_ephemeral_address(self.x.onion_address_obj.service_id)
        self.assertTrue(put_method.called)
        target_method.assert_called_with(self.x.onion_address_obj.service_id)

    def test_remove_ephemeral_address_calls_error_method_on_error(self):
        err_method = self.x.put_error_to_queue = MagicMock()
        controller = self.x.controller = MagicMock()
        self.x.onion_address_obj = MagicMock()
        target_method = controller.remove_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        result = self.x.remove_ephemeral_address(self.x.onion_address_obj.service_id)
        self.assertTrue(err_method.called)
        target_method.assert_called_with(self.x.onion_address_obj.service_id)

    def test_resume_persistent_address_returns_onion_obj_on_valid(self):
        put_method = self.x.put_to_queue = MagicMock()
        controller = self.x.controller = MagicMock()
        target_method = controller.create_ephemeral_hidden_service = MagicMock(return_value=True)
        key_type = MagicMock()
        key_content = MagicMock()
        result = self.x.resume_persistent_address(key_type, key_content)
        target_method.assert_called_with(self.x.port, key_type=key_type, key_content=key_content)
        self.assertTrue(put_method.called)
        self.assertIsNotNone(result)

    def test_resume_persisstent_address_calls_error_method_returns_none_on_error(self):
        err_method = self.x.put_to_queue = MagicMock()
        controller = self.x.controller = MagicMock()
        target_method = controller.create_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        key_type = MagicMock()
        key_content = MagicMock()
        result = self.x.resume_persistent_address(key_type, key_content)
        self.assertTrue(err_method.called)
        self.assertIsNone(result)

    #######################
    #  Start Method Tests #
    #######################

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_calls_control_from_port_with_args(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        self.x.start()
        controller.from_port.assert_called_with(port=self.x.controller_port)

    @patch.object(torproxyservice.Controller, 'remove_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'create_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'authenticate')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_calls_controller_authenticate(self, socket, authenticate, create_ephemeral, remove):
        sub = self.x.run_check = MagicMock()
        self.x.start()
        authenticate.assert_called_with()

    @patch.object(torproxyservice.Controller, 'remove_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'create_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'authenticate')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_calls_controller_create_ephemeral_sets_address(self, socket, authenticate, create_ephemeral, remove):
        sub = self.x.run_check = MagicMock()
        mock_addr_obj = types.SimpleNamespace(service_id='service_id_string')
        self.x.onion_address_obj = mock_addr_obj
        create_ephemeral.return_value = mock_addr_obj
        self.x.start()
        create_ephemeral.assert_called_with(self.x.port)
        self.assertEqual(self.x.onion_address_obj, create_ephemeral.return_value)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_calls_put_to_queue_with_build_address_string(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        target = self.x.put_to_queue = MagicMock()
        val = 'hellp'
        target_arg = self.x.build_address_string = MagicMock(return_value=val)
        self.x.start()
        target.assert_any_call(target_arg.return_value)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_calls_run_check(self, socket, controller):
        target = self.x.run_check = MagicMock()
        self.x.start()
        target.assert_called_with()

    @patch.object(torproxyservice.Controller, 'remove_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'create_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'authenticate')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_calls_controller_remove_ephemeral_when_run_false(self, socket, authenticate, create_ephemeral, remove):
        sub = self.x.run_check = MagicMock(return_value=None)
        mock_addr_obj = types.SimpleNamespace(service_id='service_id_string')
        self.x.onion_address_obj = mock_addr_obj
        create_ephemeral.return_value = mock_addr_obj
        self.x.start()
        create_ephemeral.assert_called_with(self.x.port)
        self.assertTrue(remove.called)
        remove.assert_called_with(self.x.onion_address_obj.service_id)

    def test_stop_method_sets_running_false(self):
        self.x.stop()
        self.assertFalse(self.x.running)

    def test_run_check_returns_if_running_false(self):
        self.x.running = False
        result = self.x.run_check()
        self.assertIsNone(result)

    ######################################
    #  Start Method ERROR HANDLING Tests #
    ######################################

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_catches_socket_error_exception_on_control_from_port_with_args(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        controller.from_port.side_effect = stem.SocketError()
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start()
        self.assertTrue(target.called)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_catches_authentication_failure_exception_on_control_from_port_with_args(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        import stem.connection
        auth_sub = controller.from_port().authenticate = MagicMock(side_effect=stem.connection.IncorrectSocketType('msg'))
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start()
        self.assertTrue(target.called)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_catches_controller_error_create_ephemeral(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        import stem.connection
        auth_sub = controller.from_port().create_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start()
        self.assertTrue(target.called)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_method_catches_controller_error_remove_ephemeral(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        import stem.connection
        auth_sub = controller.from_port().remove_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start()
        self.assertTrue(target.called)

    ##################################
    #  Start Persistent Method Tests #
    ##################################

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_calls_control_from_port_with_args(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        self.x.start_persistent()
        controller.from_port.assert_called_with(port=self.x.controller_port)

    @patch.object(torproxyservice.Controller, 'remove_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'create_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'authenticate')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_calls_controller_authenticate(self, socket, authenticate, create_ephemeral, remove):
        sub = self.x.run_check = MagicMock()
        sub_write = self.x._write_key_file = MagicMock()

        self.x.start_persistent()
        authenticate.assert_called_with()

    @patch.object(torproxyservice.Controller, 'remove_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'create_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'authenticate')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_calls_controller_create_ephemeral_sets_address_writes_to_file_if_file_does_not_exist(self, socket, authenticate, create_ephemeral, remove):
        sub = self.x.run_check = MagicMock()
        mock_addr_obj = types.SimpleNamespace(service_id='service_id_string',
                                              private_key_type='private_key_type_string',
                                              private_key='private_key_string')
        self.x.onion_address_obj = mock_addr_obj
        create_ephemeral.return_value = mock_addr_obj
        self.x.start_persistent()
        create_ephemeral.assert_called_with(self.x.port)
        self.assertEqual(self.x.onion_address_obj, create_ephemeral.return_value)
        self.assertTrue(os.path.exists(self.mock_tor_data_dir_path))
        with open(self.mock_tor_data_dir_path) as key_file:
            key_type, key_content = key_file.read().split(':', 1)
        self.assertEqual(key_type, mock_addr_obj.private_key_type)
        self.assertEqual(key_content, mock_addr_obj.private_key)
        self.remove_mock_tor_key_file()

    @patch.object(torproxyservice.Controller, 'remove_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'create_ephemeral_hidden_service')
    @patch.object(torproxyservice.Controller, 'authenticate')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_calls_controller_create_ephemeral_sets_address_with_data_from_key_file_if_file_exists(self, socket, authenticate, create_ephemeral, remove):
        sub = self.x.run_check = MagicMock()
        mock_addr_obj = types.SimpleNamespace(service_id='service_id_string',
                                              private_key_type='private_key_type_string',
                                              private_key='private_key_string')

        with open(self.mock_tor_data_dir_path, 'w') as key_file:
            key_file.write('{}:{}'.format(mock_addr_obj.private_key_type, mock_addr_obj.private_key))

        self.x.onion_address_obj = mock_addr_obj
        create_ephemeral.return_value = mock_addr_obj
        self.x.start_persistent()
        self.assertIn(self.x.port, create_ephemeral.call_args[0])

        target_dict = dict(key_type=mock_addr_obj.private_key_type,
                           key_content=mock_addr_obj.private_key)
        self.assertEqual(create_ephemeral.call_args[1], target_dict)
        self.assertEqual(self.x.onion_address_obj, create_ephemeral.return_value)


    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_calls_put_to_queue_with_build_address_string(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        target = self.x.put_to_queue = MagicMock()
        val = 'hellp'
        target_arg = self.x.build_address_string = MagicMock(return_value=val)
        self.x.start_persistent()
        target.assert_any_call(target_arg.return_value)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_calls_run_check(self, socket, controller):
        target = self.x.run_check = MagicMock()
        sub = self.x._write_key_file = MagicMock()
        self.x.start_persistent()
        target.assert_called_with()

    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_calls_controller_remove_ephemeral_when_run_false(self, socket):
        sub = self.x.run_check = MagicMock(return_value=None)
        controller = self.x.controller = MagicMock()
        auth = self.x.authenticate_controller = MagicMock(return_value = True)
        create = self.x.create_ephemeral_address = MagicMock()
        mock_addr_obj = types.SimpleNamespace(service_id='service_id_string',
                                              private_key_type='private_key_type_string',
                                              private_key='private_key_string')
        self.x.onion_address_obj = mock_addr_obj
        remove = self.x.remove_ephemeral_address = MagicMock()
        sub = self.x._write_key_file = MagicMock()
        self.x.start_persistent()
        self.assertTrue(remove.called)
        remove.assert_called_with(self.x.onion_address_obj.service_id)

    def test_key_file_path_name_mock(self):
        result = self.x.key_file_path()
        self.assertEqual(result, self.mock_tor_data_dir_path)

    def test_key_file_path_builds_string_from_arg_val(self):
        val = 'xxx/'
        suffix = '_Key'
        key_file_name = self.name + suffix
        proxy = torproxyservice.TorProxyService(self.name, self.port, self.q, tor_key_dir=val)
        result = proxy.key_file_path()
        self.assertEqual(result, val + key_file_name)


    #################################################
    #  Start PERSISTENT Method ERROR HANDLING Tests #
    #################################################

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_catches_socket_error_exception_on_control_from_port_with_args(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        controller.from_port.side_effect = stem.SocketError()
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start_persistent()
        self.assertTrue(target.called)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_catches_authentication_failure_exception_on_control_from_port_with_args(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        import stem.connection
        auth_sub = controller.from_port().authenticate = MagicMock(side_effect=stem.connection.IncorrectSocketType('msg'))
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start_persistent()
        self.assertTrue(target.called)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persisten_method_catches_controller_error_create_ephemeral(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        sub_write = self.x._write_key_file = MagicMock()

        import stem.connection
        auth_sub = controller.from_port().create_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start_persistent()
        self.assertTrue(target.called)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persisten_method_catches_controller_error_create_ephemeral_when_key_exists(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        mock_addr_obj = types.SimpleNamespace(service_id='service_id_string',
                                              private_key_type='private_key_type_string',
                                              private_key='private_key_string')

        with open(self.mock_tor_data_dir_path, 'w') as key_file:
            key_file.write('{}:{}'.format(mock_addr_obj.private_key_type, mock_addr_obj.private_key))


        import stem.connection
        auth_sub = controller.from_port().create_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start_persistent()
        self.assertTrue(target.called)

    @patch.object(torproxyservice, 'Controller')
    @patch('torproxy.torproxyservice.stem.socket')
    def test_start_persistent_method_catches_controller_error_remove_ephemeral(self, socket, controller):
        sub = self.x.run_check = MagicMock()
        sub_write = self.x._write_key_file = MagicMock()
        auth_sub = controller.from_port().remove_ephemeral_hidden_service = MagicMock(side_effect=stem.ControllerError)
        target = self.x.put_error_to_queue = MagicMock()
        self.x.start_persistent()
        self.assertTrue(target.called)


class TestTorProxyServiceThread(unittest.TestCase):

    def setUp(self):
        self.name = 'ServiceName'
        self.port = 1234
        self.q = queue.Queue()
        self.key_dir_val = None
        self.x = torproxyservice.TorProxyServiceThread(self.name, self.port, self.q, persistent=False, tor_key_dir=self.key_dir_val)

    def test_instance(self):
        self.assertIsInstance(self.x, torproxyservice.TorProxyServiceThread)

    def test_instance_thread(self):
        self.assertIsInstance(self.x, threading.Thread)
        self.assertEqual(self.x.name, self.name)

    def test_persistent_attribute_set_default(self):
        self.assertEqual(self.x.persistent, False)

    def test_tor_key_dir_attribute_set_default(self):
        self.assertEqual(self.x.tor_key_dir, None)

    def test_daemon_true(self):
        self.assertTrue(self.x.daemon)

    def test_creates_instance_proxy_service_with_args(self):
        self.assertIsInstance(self.x.proxy, torproxyservice.TorProxyService)
        self.assertEqual(self.name, self.x.proxy.name)
        self.assertEqual(self.port, self.x.proxy.port)
        self.assertEqual(self.q, self.x.proxy.queue)
        self.assertEqual(self.key_dir_val, self.x.proxy.tor_key_dir)

    def test_run_method_calls_start_on_proxy_if_persistent_is_false(self):
        target = self.x.proxy = MagicMock()
        self.x.run()
        target.start.assert_called_with()

    def test_run_method_calls_start_persistent_on_proxy_if_persistent_is_true(self):
        dir_val = 'tor_key_dir_string'
        self.x = torproxyservice.TorProxyServiceThread(self.name, self.port, self.q, persistent=True, tor_key_dir=dir_val)
        self.x.proxy.tor_key_dir = dir_val
        target = self.x.proxy = MagicMock(spec=self.x.proxy)
        self.x.run()
        target.start_persistent.assert_called_with()
        self.assertEqual(target.tor_key_dir, self.x.proxy.tor_key_dir)

    def test_quit_method_calls_stop_on_proxy(self):
        target = self.x.proxy = MagicMock()
        self.x.quit()
        target.stop.assert_called_with()
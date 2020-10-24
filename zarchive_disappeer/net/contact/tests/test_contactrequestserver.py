"""
test_contactrequestserver.py

Test suite for the ContactRequestServer module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net.contact import contactrequestserver
import socketserver
from disappeer.net.bases import abstractserverfactory
from disappeer.net.contact import contactprotocol
from disappeer import settings
from disappeer.constants import constants
from disappeer.net.contact import contactrequestfactory
from disappeer.net.contact import contactrequestvalidator
import copy


class TestImportsAndModuleVars(unittest.TestCase):

    def test_socketserver(self):
        self.assertEqual(socketserver, contactrequestserver.socketserver)

    def test_abstractserverfactory(self):
        self.assertEqual(abstractserverfactory, contactrequestserver.abstractserverfactory)

    def test_settings(self):
        self.assertEqual(settings, contactrequestserver.settings)

    def test_contactprotocol(self):
        self.assertEqual(contactprotocol, contactrequestserver.contactprotocol)

    def test_constants(self):
        self.assertEqual(constants, contactrequestserver.constants)

    def test_command_list(self):
        self.assertEqual(constants.command_list, contactrequestserver.command_list)

    def test_contactrequestvalidator(self):
        self.assertEqual(contactrequestvalidator, contactrequestserver.contactrequestvalidator)


class TestThreadedTCPServerBasics(unittest.TestCase):

    def setUp(self):
        self.server_address = MagicMock()
        self.req_handler_class = MagicMock()
        self.x = contactrequestserver.ThreadedTCPServer
        self.base_list = self.x.__bases__

    def test_class_self(self):
        self.assertEqual(self.x, contactrequestserver.ThreadedTCPServer)

    def test_threading_mixin_base(self):
        self.assertIn(socketserver.ThreadingMixIn, self.base_list)

    def test_tcpserver_base(self):
        self.assertIn(socketserver.TCPServer, self.base_list)

    def test_allow_reuse_address_true(self):
        self.assertTrue(self.x.allow_reuse_address)


class TestContactRequestServerFactory(unittest.TestCase):

    def setUp(self):
        self.queue = MagicMock()
        self.x = contactrequestserver.ContactRequestServerFactory(self.queue)

    def test_instance(self):
        self.assertIsInstance(self.x, contactrequestserver.ContactRequestServerFactory)

    def test_instance_abstractserverfactory(self):
        self.assertIsInstance(self.x, abstractserverfactory.AbstractServerFactory)

    def test_queue_method_set_by_metaclass(self):
        self.assertEqual(self.queue, self.x.queue)

    def test_host_property(self):
        target = 'localhost'
        self.assertEqual(target, self.x.host)

    def test_name_property(self):
        target = 'Contact_Request_Server'
        self.assertEqual(target, self.x.name)
        with self.assertRaises(AttributeError):
            self.x.name = 'ssss'

    def test_port_property(self):
        target = settings.port_contact_request_server
        self.assertEqual(target, self.x.port)

    def test_request_handler_obj_property(self):
        target = contactrequestserver.ContactRequestServerRequestHandler
        self.assertEqual(target, self.x.request_handler_obj)

    def test_server_obj_property(self):
        target = contactrequestserver.ThreadedTCPServer
        self.assertEqual(target, self.x.server_obj)


class TestContactRequestServerRequestHandler(unittest.TestCase):
    x_class = contactrequestserver.ContactRequestServerRequestHandler
    base_list = x_class.__bases__
    request = MagicMock()
    client_address = MagicMock()
    server = MagicMock()
    host_address = '192.168.X.X'
    key_dir = 'tests/data/keys'
    passphrase = 'passphrase'
    factory = contactrequestfactory.ContactRequestFactory(host_address, key_dir, passphrase)
    valid_req_dict = factory.build()
    valid_req_validator = contactrequestvalidator.ContactRequestValidator(valid_req_dict)
    target_file = settings.gpg_host_pubkey

    def setUp(self):
        self.req_validator = copy.deepcopy(self.valid_req_validator)
        self.mocked_contact_protocol = contactrequestserver.contactprotocol.ContactProtocol = MagicMock(spec=contactprotocol.ContactProtocol(self.request))
        self.x = contactrequestserver.ContactRequestServerRequestHandler(self.request, self.client_address, self.server)

    def test_class_self(self):
        self.assertEqual(self.x_class, contactrequestserver.ContactRequestServerRequestHandler)

    def test_BaseRequestHandler_base(self):
        self.assertIn(socketserver.BaseRequestHandler, self.base_list)

    def test_has_handle_method(self):
        check = hasattr(self.x_class, 'handle')
        self.assertTrue(check)

    @patch('disappeer.net.contact.contactprotocol.ContactProtocol')
    def test_setup_method_sets_protocol(self, target):
        self.x.setup()
        self.assertTrue(target.called)

    def test_handle_method_calls_process_incoming(self):
        sub = self.x.set_protocol = MagicMock()
        target = self.x.protocol = MagicMock()
        self.x.handle()
        self.assertTrue(target.process_incoming.called)

    def test_handle_method_returns_false_if_process_incoming_returns_false(self):
        sub = self.x.protocol.process_incoming = MagicMock(return_value=False)
        result = self.x.handle()
        self.assertFalse(result)

    def test_handle_method_calls_validate_result_with_result(self):
        val = dict(data='hello')
        target_dict = dict(data='hello', desc=constants.command_list.New_Contact_Req)
        sub = self.x.protocol.process_incoming = MagicMock(return_value=val)
        target = self.x.validate_result = MagicMock()
        self.x.handle()
        target.assert_called_with(sub.return_value)

    def test_validate_result_calls_handle_valid_result_with_result_dict_on_valid(self):
        check = self.req_validator #contactrequestvalidator.ContactRequestValidator(self.valid_req_dict)
        target = self.x.handle_valid_result = MagicMock()
        self.x.validate_result(self.valid_req_dict)
        target.assert_called_with(check.result_dict)

    def test_handle_valid_result_calls_send_response(self):
        target = self.x.send_response = MagicMock()
        self.x.handle_valid_result(self.req_validator.result_dict)
        target.assert_called_with(self.req_validator.result_dict)

    def test_handle_valid_result_calls_put_to_queue(self):
        target = self.x.put_to_queue = MagicMock()
        self.x.handle_valid_result(self.req_validator.result_dict)
        target.assert_called_with(self.req_validator.result_dict)

    def test_put_to_queue_method_adds_desc_to_result_dict_for_queue(self):
        target = self.req_validator.result_dict
        target['desc'] = constants.command_list.New_Contact_Req
        server = self.x.server = MagicMock()
        self.x.put_to_queue(self.req_validator.result_dict)
        server.queue.put.assert_called_with(target)

    def test_read_file_method_returns_file_contents(self):
        with open(self.target_file, 'r') as f:
            check = f.read()
        result = self.x.read_file(self.target_file)
        self.assertEqual(result, check)

    def test_build_response_dict_builds_dict(self):
        target = dict(gpg_pub_key=self.x.read_file(settings.gpg_host_pubkey),
                      nonce=self.req_validator.result_dict['nonce'],
                      desc='ACK')
        result = self.x.build_response_dict(self.req_validator.result_dict)
        self.assertEqual(result, target)

    def test_send_response_calls_protocol_send_ack_with_response_dict(self):
        response_dict = self.x.build_response_dict(self.req_validator.result_dict)
        target = self.x.protocol = MagicMock()
        self.x.send_response(self.req_validator.result_dict)
        target.send_ack.assert_called_with(response_dict)




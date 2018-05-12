"""
test_contactresponseserver.py

Test suite for the ContactResponseServer module and classes

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net.contactresponse import contactresponseserver
from disappeer.net.contact import contactprotocol
import socketserver
import ssl
from disappeer import settings
from disappeer.net.bases import abstractserverfactory
from disappeer.models.db import dbpendingcontactresponsetable
from disappeer.models.db import dbserversynctable
from disappeer.constants import constants


class TestImports(unittest.TestCase):

    def test_socketserver(self):
        self.assertEqual(socketserver, contactresponseserver.socketserver)

    def test_ssl(self):
        self.assertEqual(ssl, contactresponseserver.ssl)

    def test_settings(self):
        self.assertEqual(settings, contactresponseserver.settings)

    def test_abstract_server_factory(self):
        self.assertEqual(abstractserverfactory, contactresponseserver.abstractserverfactory)

    def test_contactprotocl(self):
        self.assertEqual(contactprotocol, contactresponseserver.contactprotocol)

    def test_dbpendingcontactresponsetable(self):
        self.assertEqual(dbpendingcontactresponsetable, contactresponseserver.dbpendingcontactresponsetable)

    def test_command_list(self):
        self.assertEqual(constants.command_list, contactresponseserver.command_list)

    def test_dbserversynctable(self):
        self.assertEqual(dbserversynctable, contactresponseserver.dbserversynctable)


class TestSSLThreadedContactResponseTCPServer(unittest.TestCase):

    def setUp(self):
        self.server_address = MagicMock()
        self.req_handler_class = MagicMock()
        self.x_class = contactresponseserver.SSLThreadedContactResponseTCPServer
        self.base_list = self.x_class.__bases__
        contactresponseserver.SSLThreadedContactResponseTCPServer.server_bind = MagicMock()
        contactresponseserver.SSLThreadedContactResponseTCPServer.process_request = MagicMock()
        self.x = contactresponseserver.SSLThreadedContactResponseTCPServer(self.server_address,
                                                                           self.req_handler_class)

    def tearDown(self):
        self.x.socket.close()

    def test_class_self(self):
        self.assertEqual(self.x_class, contactresponseserver.SSLThreadedContactResponseTCPServer)

    def test_threading_mixin_base(self):
        self.assertIn(socketserver.ThreadingMixIn, self.base_list)

    def test_tcpserver_base(self):
        self.assertIn(socketserver.TCPServer, self.base_list)

    def test_allow_reuse_address_true(self):
        self.assertTrue(self.x.allow_reuse_address)

    def test_bind_and_activate_true(self):
        self.assertTrue(self.x.server_bind.called)

    @patch.object(contactresponseserver.ssl, 'wrap_socket')
    @patch.object(contactresponseserver.socketserver.socket.socket, 'accept')
    def test_get_request_method_calls_socket_accept(self, accept, wrap):
        accept.return_value = (0, 1)
        result = self.x.get_request()
        self.assertTrue(accept.called)

    def test_get_sync_db_path_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            contactresponseserver.SSLThreadedContactResponseTCPServer.get_sync_db_path()


class TestSSLContactResponseRequestHandler(unittest.TestCase):

    @patch('net.contactresponse.contactresponseserver.dbserversynctable.DBServerSyncTable')
    def setUp(self, db_patch):
        self.request = MagicMock()
        self.client_address = MagicMock()
        self.server = MagicMock()
        self.mocked_contact_protocol = contactresponseserver.contactprotocol.ContactProtocol = MagicMock(spec=contactprotocol.ContactProtocol(self.request))
        self.x = contactresponseserver.SSLContactResponseRequestHandler(self.request, self.client_address, self.server)

    def test_instance(self):
        self.assertIsInstance(self.x, contactresponseserver.SSLContactResponseRequestHandler)

    def test_parent_instance(self):
        self.assertIsInstance(self.x, socketserver.BaseRequestHandler)

    def test_handle_method(self):
        check = hasattr(self.x, 'handle')
        self.assertTrue(check)

    def test_setup_method(self):
        check = hasattr(self.x, 'setup')
        self.assertTrue(check)

    @patch.object(contactresponseserver.dbserversynctable.DBServerSyncTable, 'execute')
    def test_setup_sets_db_server_sync_table_attribute_with_server_sync_method_result(self, db_patch_1):
        val = 'xxx'
        target_method = self.x.server.get_sync_db_path = MagicMock(return_value=val)
        self.x.setup()
        self.assertIsInstance(self.x.db_server_sync_table, dbserversynctable.DBServerSyncTable)
        self.assertEqual(target_method.return_value, self.x.db_server_sync_table.database)

    @patch('disappeer.net.contactresponse.contactresponseserver.dbserversynctable.DBServerSyncTable')
    @patch('disappeer.net.contact.contactprotocol.ContactProtocol')
    def test_setup_method_sets_protocol(self, target, db_patch):
        self.x.setup()
        self.assertTrue(target.called)
        self.assertIsNotNone(self.x.protocol)

    def test_handle_method_calls_process_incoming(self):
        sub = self.x.set_protocol = MagicMock()
        target = self.x.protocol = MagicMock()
        self.x.protocol.response_string = 'RES'
        self.x.handle()
        self.assertTrue(target.process_incoming.called)
        target.process_incoming.assert_called_with('RES')

    def test_handle_method_returns_false_if_process_incoming_returns_false(self):
        sub = self.x.protocol.process_incoming = MagicMock(return_value=False)
        result = self.x.handle()
        self.assertIs(result, False)

    def test_check_dict_keys_returns_true_on_valid_input(self):
        target_list = ['ciphertext', 'request_nonce', 'response_nonce']
        valid_dict = dict(ciphertext='',
                          request_nonce='',
                          response_nonce='')
        result = self.x.dict_keys_are_valid(valid_dict)
        self.assertIs(result, True)

    def test_check_dict_keys_returns_false_on_invalid_input(self):
        invalid_dict = dict(xxx='',
                          request_nonce='',
                          response_nonce='')
        result = self.x.dict_keys_are_valid(invalid_dict)
        self.assertIs(result, False)

    def test_check_dict_keys_returns_false_on_bad_input(self):
        bad = 'xxx'
        result = self.x.dict_keys_are_valid(bad)
        self.assertIs(result, False)

    def test_nonce_is_valid_returns_true_on_valid_input(self):
        nonce_list = ['aaa', 'bbb']
        sub = self.x.db_server_sync_table.fetch_all_nonces = MagicMock(return_value=nonce_list)
        valid_dict = dict(ciphertext='',
                          request_nonce=nonce_list[0],
                          response_nonce='')
        result = self.x.is_nonce_valid(valid_dict)
        self.assertIs(result, True)

    def test_nonce_is_valid_returns_false_on_invalid_input(self):
        nonce_list = ['aaa', 'bbb']
        sub = self.x.db_server_sync_table.fetch_all_nonces = MagicMock(return_value=nonce_list)
        valid_dict = dict(ciphertext='',
                          request_nonce='',
                          response_nonce='')
        result = self.x.is_nonce_valid(valid_dict)
        self.assertIs(result, False)

    def test_nonce_is_valid_returns_false_on_bad_dict(self):
        nonce_list = ['aaa', 'bbb']
        sub = self.x.db_server_sync_table.fetch_all_nonces = MagicMock(return_value=nonce_list)
        invalid_dict = dict(ciphertext='',
                          xxxxx='',
                          response_nonce='')
        result = self.x.is_nonce_valid(invalid_dict)
        self.assertIs(result, False)

    def test_nonce_is_valid_returns_false_on_no_dict(self):
        nonce_list = ['aaa', 'bbb']
        sub = self.x.db_server_sync_table.fetch_all_nonces = MagicMock(return_value=nonce_list)
        bad = 'xxx'
        result = self.x.is_nonce_valid(bad)
        self.assertIs(result, False)

    def test_is_result_valid_calls_dict_keys_are_valid_with_args(self):
        result_dict = MagicMock()
        target = self.x.dict_keys_are_valid = MagicMock()
        self.x.is_result_valid(result_dict)
        target.assert_called_with(result_dict)

    def test_is_result_valid_calls_is_nonce_valid_with_args(self):
        result_dict = MagicMock()
        target = self.x.is_nonce_valid = MagicMock()
        self.x.is_result_valid(result_dict)
        target.assert_called_with(result_dict)

    def test_is_result_valid_returns_true_if_all_checks_true(self):
        mock_input = MagicMock()
        sub1 = self.x.is_nonce_valid = MagicMock(return_value=True)
        sub2 = self.x.dict_keys_are_valid = MagicMock(return_value=True)
        result = self.x.is_result_valid(mock_input)
        self.assertIs(result, True)

    def test_is_result_valid_returns_false_if_not_all_checks_true(self):
        mock_input = MagicMock()
        sub1 = self.x.is_nonce_valid = MagicMock(return_value=False)
        sub2 = self.x.dict_keys_are_valid = MagicMock(return_value=True)
        result = self.x.is_result_valid(mock_input)
        self.assertIs(result, False)

    def test_handle_calls_handle_valid_result_if_is_result_valid_returns_true(self):
        target = self.x.handle_valid_result = MagicMock()
        sub = self.x.is_result_valid = MagicMock(return_value=True)
        sub1 = self.x.protocol.process_incoming = MagicMock(return_value=dict())
        self.x.handle()
        target.assert_called_with(sub1.return_value)

    def test_handle_valid_result_calls_send_response(self):
        mock_result = dict()
        target = self.x.send_response = MagicMock()
        self.x.handle_valid_result(mock_result)
        target.assert_called_with(mock_result)

    def test_handle_valid_result_calls_put_to_queue(self):
        mock_result = dict()
        target = self.x.put_to_queue = MagicMock()
        sub = self.x.send_response = MagicMock()
        self.x.handle_valid_result(mock_result)
        target.assert_called_with(mock_result)

    def test_build_response_dict_builds_dict(self):
        mock_input = dict(response_nonce='xxx')
        target = dict(nonce=mock_input['response_nonce'],
                      desc='ACK')
        result = self.x.build_response_dict(mock_input)
        self.assertEqual(result, target)

    def test_send_response_calls_protocol_send_ack_with_response_dict(self):
        mock_input = dict(response_nonce='xxx')
        response_dict = self.x.build_response_dict(mock_input)
        target = self.x.protocol = MagicMock()
        self.x.send_response(mock_input)
        target.send_ack.assert_called_with(response_dict)

    def test_put_to_queue_method_adds_desc_to_result_dict_for_queue(self):
        target = dict(one=1)
        target['desc'] = constants.command_list.New_Contact_Res
        server = self.x.server = MagicMock()
        self.x.put_to_queue(target)
        server.queue.put.assert_called_with(target)


class TestContactResponseServerFactory(unittest.TestCase):

    def setUp(self):
        self.queue = MagicMock()
        self.x = contactresponseserver.ContactResponseServerFactory(self.queue)

    def test_instance(self):
        self.assertIsInstance(self.x, contactresponseserver.ContactResponseServerFactory)

    def test_instance_abstractserverfactory(self):
        self.assertIsInstance(self.x, abstractserverfactory.AbstractServerFactory)

    def test_queue_attribute_set(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_name_property(self):
        target = 'Contact_Response_Server'
        self.assertEqual(target, self.x.name)
        with self.assertRaises(AttributeError):
            self.x.name = 'ssss'

    def test_host_property(self):
        target = 'localhost'
        self.assertEqual(target, self.x.host)

    def test_port_property(self):
        target = settings.port_contact_response_server
        self.assertEqual(target, self.x.port)

    def test_request_handler_obj_property(self):
        target = contactresponseserver.SSLContactResponseRequestHandler
        self.assertEqual(target, self.x.request_handler_obj)

    def test_server_obj_property(self):
        target = contactresponseserver.SSLThreadedContactResponseTCPServer
        self.assertEqual(target, self.x.server_obj)

"""
test_contactrequestclient.py

Test suite for the ContactRequestClient class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch, PropertyMock
from disappeer.net.contact import contactrequestclient
from disappeer.net.bases import abstractclient
from disappeer.net.bases import baseprotocol
from disappeer.net.contact import contactprotocol
from types import SimpleNamespace
from disappeer.constants import constants


class FakeSocket(MagicMock):

    def __init__(self, payload_data):
        super().__init__()
        self.msg = bytes(payload_data, 'utf-8')

    def recv(self, num_bytes):
        target = self.msg[:num_bytes]
        self.msg = self.msg[num_bytes:]
        return target


class TestImports(unittest.TestCase):

    def test_abstractclient(self):
        self.assertEqual(abstractclient, contactrequestclient.abstractclient)

    def test_contactprotocol(self):
        self.assertEqual(contactprotocol, contactrequestclient.contactprotocol)

    def test_constants(self):
        self.assertEqual(constants, contactrequestclient.constants)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.payload = 'Hello World'
        self.socket = FakeSocket(self.payload)
        self.argnamespace = SimpleNamespace()
        self.argnamespace.test = 'test'
        self.argnamespace.payload_dict = MagicMock()
        self.argnamespace.command = 'REQ'
        self.argnamespace.host = 'host'
        self.argnamespace.port = 'port'
        self.argnamespace.nonce = 'nonce'
        self.argnamespace.queue = MagicMock()
        self.x = contactrequestclient.ContactRequestClient(self.argnamespace)

    def test_instance(self):
        self.assertIsInstance(self.x, contactrequestclient.ContactRequestClient)

    def test_instance_abstractclient(self):
        self.assertIsInstance(self.x, abstractclient.AbstractClient)

    def test_parent_class_sets_argnamespace_attribute(self):
        self.assertEqual(self.x.argnamespace, self.argnamespace)

    def test_set_protocol_method_sets_protocol_attribute(self):
        result = self.x.set_protocol()
        self.assertIsInstance(self.x.protocol, contactprotocol.ContactProtocol)

    def test_wrap_socket_method_does_nothing(self):
        result = self.x.wrap_socket()
        self.assertIsNone(result)

    def test_send_method_calls_configure_transport_method(self):
        target = self.x.configure_transport = MagicMock()
        sub = self.x.protocol = MagicMock()
        self.x.send()
        target.assert_called_with()

    def test_send_method_returns_error_if_error(self):
        sub = self.x.configure_transport = MagicMock()
        self.x.error = ConnectionRefusedError()
        result = self.x.send()
        self.assertEqual(result, self.x.error)

    def test_send_method_calls_report_error_if_error(self):
        sub = self.x.configure_transport = MagicMock()
        target = self.x.report_error = MagicMock()
        self.x.error = ConnectionRefusedError()
        result = self.x.send()
        target.assert_called_with()

    def test_send_method_calls_protocol_send_request_with_no_error(self):
        sub = self.x.configure_transport = MagicMock()
        target = self.x.protocol = MagicMock()
        self.x.send()
        target.send_request.assert_called_with(self.x.payload_dict, self.x.command)

    def test_send_method_calls_handle_response_method(self):
        sub = self.x.configure_transport = MagicMock()
        sub1 = self.x.protocol = MagicMock()
        target = self.x.handle_response = MagicMock()
        self.x.send()
        target.assert_called_with()

    def test_handle_response_method_calls_handle_response_on_protocol(self):
        target = self.x.protocol = MagicMock()
        self.x.handle_response()
        target.handle_response.assert_called_with()

    def test_handle_response_method_calls_report_result(self):
        val_dict = dict()
        target = self.x.report_result = MagicMock()
        sub = self.x.protocol = MagicMock(return_value=val_dict)
        self.x.handle_response()
        target.assert_called_with(sub.handle_response.return_value)

    def test_report_result_calls_build_result_dict(self):
        val = dict()
        target = self.x.build_result_dict = MagicMock()
        self.x.report_result(val)
        target.assert_called_with(val)

    def test_report_result_puts_result_dict_to_queue(self):
        val = dict()
        sub = self.x.build_result_dict = MagicMock(return_value=val)
        self.x.report_result(val)
        self.x.queue.put.assert_called_with(sub.return_value)

    def test_build_result_dict_returns_correct_dict_valid_nonce(self):
        input_dict = dict(desc='ACK', nonce='nonce', gpg_pubkey='gpg_pubkey')
        target = dict(desc=constants.command_list.New_Contact_Req_Client_Res,
                      result=input_dict,
                      nonce=self.x.nonce,
                      nonce_valid=True,
                      host=self.x.host)
        result = self.x.build_result_dict(input_dict)
        self.assertEqual(result, target)

    def test_build_result_dict_returns_correct_dict_NO_nonce(self):
        input_dict = dict(desc='ACK', gpg_pubkey='gpg_pubkey')
        target = dict(desc=constants.command_list.New_Contact_Req_Client_Res,
                      result=input_dict,
                      nonce=self.x.nonce,
                      nonce_valid=False,
                      host=self.x.host)
        result = self.x.build_result_dict(input_dict)
        self.assertEqual(result, target)

    def test_build_result_dict_returns_correct_dict_not_valid_nonce(self):
        input_dict = dict(desc='ACK', nonce='', gpg_pubkey='gpg_pubkey')
        target = dict(desc=constants.command_list.New_Contact_Req_Client_Res,
                      result=input_dict,
                      nonce=self.x.nonce,
                      nonce_valid=False,
                      host=self.x.host)
        result = self.x.build_result_dict(input_dict)
        self.assertEqual(result, target)

    def test_build_error_dict_returns_correct_dict(self):
        self.x.error = 'error'
        desc = constants.command_list.New_Contact_Req_Client_Err
        target = dict(desc=desc,
                      error=self.x.error,
                      host=self.x.host,
                      port=self.x.port)
        result = self.x.build_error_dict()
        self.assertEqual(result, target)

    def test_report_error_calls_build_error_dict(self):
        val = 'xxx'
        target = self.x.build_error_dict = MagicMock(return_value=val)
        self.x.report_error()
        target.assert_called_with()

    def test_report_error_puts_error_dict_to_queue(self):
        val = 'xxx'
        sub = self.x.build_error_dict = MagicMock(return_value=val)
        self.x.report_error()
        self.x.queue.put.assert_called_with(sub.return_value)


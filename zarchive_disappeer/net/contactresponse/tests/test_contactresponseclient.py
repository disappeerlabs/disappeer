"""
test_contactresponseclient.py

Test suite for ContactResponseClient class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net.contactresponse import contactresponseclient
from disappeer.net.bases import abstractclient
from disappeer.net.contact import contactprotocol
from types import SimpleNamespace
import ssl
import tempfile
from disappeer.constants import constants


class TestImports(unittest.TestCase):

    def test_abstract_client(self):
        self.assertEqual(abstractclient, contactresponseclient.abstractclient)

    def test_ssl(self):
        self.assertEqual(ssl, contactresponseclient.ssl)

    def test_tempfile(self):
        self.assertEqual(tempfile, contactresponseclient.tempfile)

    def test_contactprotocol(self):
        self.assertEqual(contactprotocol, contactresponseclient.contactprotocol)

    def test_constants(self):
        self.assertEqual(constants, contactresponseclient.constants)


class FakeSocket:
    def __init__(self, payload_data):
        self.msg = bytes(payload_data, 'utf-8')

    def recv(self, num_bytes):
        target = self.msg[:num_bytes]
        self.msg = self.msg[num_bytes:]
        return target


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.payload = 'Hello World'
        self.socket = FakeSocket(self.payload)
        self.argnamespace = SimpleNamespace()
        self.argnamespace.test = 'test'
        self.argnamespace.payload_dict = dict()
        self.argnamespace.command = 'RES'
        self.argnamespace.host = 'host'
        self.argnamespace.port = 'port'
        self.argnamespace.nonce = 'nonce'
        self.argnamespace.queue = MagicMock()
        self.argnamespace.request_nonce = 'request_nonce_string'
        self.x = contactresponseclient.ContactResponseClient(self.argnamespace)

    def test_instance(self):
        self.assertIsInstance(self.x, contactresponseclient.ContactResponseClient)

    def test_instance_abstractclient(self):
        self.assertIsInstance(self.x, abstractclient.AbstractClient)

    def test_parent_class_sets_argnamespace_attribute(self):
        self.assertEqual(self.x.argnamespace, self.argnamespace)

    def test_nonce_attribute_set(self):
        self.assertEqual(self.argnamespace.nonce, self.x.nonce)

    def test_request_nonce_attribute_set(self):
        self.assertEqual(self.argnamespace.request_nonce, self.x.request_nonce)

    def test_set_protocol_sets_protocol_attribute_to_contact_protocol(self):
        result = self.x.set_protocol()
        self.assertIsNotNone(self.x.protocol)

    def test_send_method_calls_config_transport(self):
        sub = self.x.protocol = MagicMock()
        target = self.x.configure_transport = MagicMock()
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

    def test_build_error_dict_returns_correct_dict(self):
        self.x.error = 'error'
        desc = constants.command_list.New_Contact_Res_Client_Err
        target = dict(desc=desc,
                      error=self.x.error,
                      host=self.x.host,
                      port=self.x.port,
                      request_nonce=self.x.request_nonce)
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
        input_dict = dict(desc='ACK', nonce='nonce')
        target = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                      result=input_dict,
                      nonce=self.x.nonce,
                      nonce_valid=True,
                      request_nonce=self.x.request_nonce)
        result = self.x.build_result_dict(input_dict)
        self.assertEqual(result, target)

    def test_build_result_dict_returns_correct_dict_NO_nonce(self):
        input_dict = dict(desc='ACK')
        target = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                      result=input_dict,
                      nonce=self.x.nonce,
                      nonce_valid=False,
                      request_nonce=self.x.request_nonce)
        result = self.x.build_result_dict(input_dict)
        self.assertEqual(result, target)

    def test_build_result_dict_returns_correct_dict_not_valid_nonce(self):
        input_dict = dict(desc='ACK', nonce='', gpg_pubkey='gpg_pubkey')
        target = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                      result=input_dict,
                      nonce=self.x.nonce,
                      nonce_valid=False,
                      request_nonce=self.x.request_nonce)
        result = self.x.build_result_dict(input_dict)
        self.assertEqual(result, target)
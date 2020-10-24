"""
test_clientfactory.py

Test suite for ClientFactory module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.net.bases import clientfactory
from disappeer.net.contact import contactrequestclient
from types import SimpleNamespace
from disappeer.net.contactresponse import contactresponseclient
from disappeer.net.message import messageclient


class TestImports(unittest.TestCase):

    def test_contactrequestclient(self):
        self.assertEqual(contactrequestclient, clientfactory.contactrequestclient)

    def test_contactresponseclient(self):
        self.assertEqual(contactresponseclient, clientfactory.contactresponseclient)

    def test_messageclient(self):
        self.assertEqual(messageclient, clientfactory.messageclient)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.client_type = 'client_type'
        self.host = 'localhost'
        self.port = 10001
        self.que = 'queue'
        self.ssl_key = 'ssl_key'
        self.argnamespace = SimpleNamespace(host=self.host,
                                            port=self.port,
                                            queue=self.que,
                                            request_nonce='111')
        self.x = clientfactory.ClientFactory(self.client_type, self.argnamespace)

    def test_instance(self):
        self.assertIsInstance(self.x, clientfactory.ClientFactory)

    def test_client_type_attribute_set(self):
        self.assertEqual(self.x.client_type, self.client_type)

    def test_argnamespace_attribute_set(self):
        self.assertEqual(self.x.argnamespace, self.argnamespace)

    def test_name_attr_set_to_client_type_val(self):
        self.assertEqual(self.x.name, self.client_type)

    def test_build_method_for_contact_calls_create_contact_client(self):
        self.x.client_type = 'contact_request'
        target = self.x.create_contact_request_client = MagicMock()
        self.x.build()
        target.assert_called_with()

    def test_build_method_for_contact_request_returns_contact_request_client(self):
        self.x.client_type = 'contact_request'
        result = self.x.build()
        self.assertIsInstance(result, contactrequestclient.ContactRequestClient)

    def test_create_contact_request_client_returns_contact_request_client(self):
        result = self.x.create_contact_request_client()
        self.assertIsInstance(result, contactrequestclient.ContactRequestClient)

    def test_create_contact_request_client_passes_argnamespace_to_client(self):
        result = self.x.create_contact_request_client()
        self.assertEqual(result.argnamespace, self.argnamespace)

    def test_create_contact_request_client_adds_req_command_to_client_argnamespace(self):
        result = self.x.create_contact_request_client()
        target = 'REQ'
        self.assertEqual(target, result.command)

    def test_build_method_for_contact_response_returns_contact_response_client(self):
        self.x.client_type = 'contact_response'
        result = self.x.build()
        self.assertIsInstance(result, contactresponseclient.ContactResponseClient)

    def test_create_contact_response_client_returns_contact_response_client(self):
        result = self.x.create_contact_response_client()
        self.assertIsInstance(result, contactresponseclient.ContactResponseClient)

    def test_create_contact_response_client_passes_argnamespace_to_client(self):
        result = self.x.create_contact_response_client()
        self.assertEqual(result.argnamespace, self.argnamespace)

    def test_build_method_for_message_client_returns_message_client(self):
        self.x.client_type = 'send_message'
        result = self.x.build()
        self.assertIsInstance(result, messageclient.MessageClient)

    def test_create_message_client_returns_message_client(self):
        result = self.x.create_message_client()
        self.assertIsInstance(result, messageclient.MessageClient)

    def test_create_message_client_passes_argnamespace_to_client(self):
        result = self.x.create_message_client()
        self.assertEqual(result.argnamespace, self.argnamespace)

"""
test_networkservers.py

Test suite for NetworkServers module and class object, which holds references and control methods for network servers

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net import networkservers
from disappeer.net.contact import contactrequestserver
from disappeer.net.contactresponse import contactresponseserver
from disappeer.net.message import messageserver
from disappeer.net.bases import servercontroller
from disappeer.net.bases import threadmanagers


class TestImports(unittest.TestCase):

    def test_contactrequestserver(self):
        self.assertEqual(contactrequestserver, networkservers.contactrequestserver)

    def test_contactresponseserver(self):
        self.assertEqual(contactresponseserver, networkservers.contactresponseserver)

    def test_messageserver(self):
        self.assertEqual(messageserver, networkservers.messageserver)

    def test_servercontroller(self):
        self.assertEqual(servercontroller, networkservers.servercontroller)

    def test_threadmanager(self):
        self.assertEqual(threadmanagers, networkservers.threadmanagers)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.queue = MagicMock()
        self.x = networkservers.NetworkServers(self.queue)

    def test_instance(self):
        self.assertIsInstance(self.x, networkservers.NetworkServers)

    def test_queue_attr(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_contact_req_server_att_is_server_controller(self):
        self.assertIsInstance(self.x.contact_request_server, servercontroller.ServerController)

    def test_contact_req_server_att_has_contact_req_factory(self):
        self.assertIsInstance(self.x.contact_request_server.factory, contactrequestserver.ContactRequestServerFactory)

    def test_contact_req_server_att_has_server_thread_manager(self):
        self.assertIsInstance(self.x.contact_request_server.server, threadmanagers.ServerThreadManager)

    def test_contact_req_server_queue_attribute_is_class_queue(self):
        self.assertEqual(self.x.queue, self.x.contact_request_server.queue)

    def test_contact_res_server_att_is_server_controller(self):
        self.assertIsInstance(self.x.contact_response_server, servercontroller.ServerController)

    def test_contact_res_server_att_has_contact_res_factory(self):
        self.assertIsInstance(self.x.contact_response_server.factory, contactresponseserver.ContactResponseServerFactory)

    def test_contact_res_server_att_has_server_thread_manager(self):
        self.assertIsInstance(self.x.contact_response_server.server, threadmanagers.ServerThreadManager)

    def test_contact_res_server_queue_attribute_is_class_queue(self):
        self.assertEqual(self.x.queue, self.x.contact_response_server.queue)

    def test_message_server_att_is_server_controller(self):
        self.assertIsInstance(self.x.message_server, servercontroller.ServerController)

    def test_message_server_att_has_contact_req_factory(self):
        self.assertIsInstance(self.x.message_server.factory, messageserver.MessageServerFactory)

    def test_message_server_att_has_server_thread_manager(self):
        self.assertIsInstance(self.x.message_server.server, threadmanagers.ServerThreadManager)

    def test_message_server_queue_attribute_is_class_queue(self):
        self.assertEqual(self.x.queue, self.x.message_server.queue)

    def test_start_network_services_calls_start_on_contact_req_server(self):
        sub = self.x.message_server = MagicMock()
        sub1 = self.x.contact_response_server = MagicMock()
        self.x.contact_request_server = MagicMock()
        self.x.start_network_services()
        self.assertTrue(self.x.contact_request_server.start.called)

    def test_start_network_services_calls_start_on_contact_res_server(self):
        sub = self.x.contact_request_server = MagicMock()
        sub_1 = self.x.message_server = MagicMock()
        target = self.x.contact_response_server = MagicMock()
        self.x.start_network_services()
        self.assertTrue(target.start.called)

    def test_start_network_services_calls_start_on_message_server(self):
        sub = self.x.contact_request_server = MagicMock()
        sub_1 = self.x.contact_response_server = MagicMock()
        target = self.x.message_server = MagicMock()
        self.x.start_network_services()
        self.assertTrue(target.start.called)

    def test_stop_network_services_calls_stop_on_contact_req_server(self):
        sub = self.x.contact_response_server = MagicMock()
        sub1 = self.x.message_server = MagicMock()
        self.x.contact_request_server = MagicMock()
        self.x.stop_network_services()
        self.assertTrue(self.x.contact_request_server.stop.called)

    def test_stop_network_services_calls_stop_on_contact_res_server(self):
        sub = self.x.contact_request_server = MagicMock()
        sub1 = self.x.message_server = MagicMock()
        target = self.x.contact_response_server = MagicMock()
        self.x.stop_network_services()
        self.assertTrue(target.stop.called)

    def test_stop_network_services_calls_stop_on_message_server(self):
        sub = self.x.contact_response_server = MagicMock()
        self.x.contact_request_server = MagicMock()
        target = self.x.message_server = MagicMock()
        self.x.stop_network_services()
        self.assertTrue(target.stop.called)

    def test_are_running_returns_true_if_all_servers_status_true(self):
        self.x.contact_request_server.status.set(True)
        self.x.contact_response_server.status.set(True)
        self.x.message_server.status.set(True)
        result = self.x.are_running()
        self.assertIs(result, True)

    def test_are_running_returns_false_if_NOT_all_servers_status_true(self):
        self.x.contact_request_server.status.set(False)
        self.x.contact_response_server.status.set(True)
        self.x.message_server.status.set(True)
        result = self.x.are_running()
        self.assertIs(result, False)



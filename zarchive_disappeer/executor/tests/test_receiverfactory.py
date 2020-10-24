"""
test_receiverfactory.py

Test suite for ReceiverFactory module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock

from disappeer.constants import constants
from disappeer.executor import receiverfactory
from disappeer.executor.receivers import checksanityreceiver
from disappeer.executor.receivers.newcontactresponseclientresponsereceiver import NewContactResponseClientResponseReceiver
from disappeer.executor.receivers.sendnewmessageclientresponsereceiver import SendNewMessageClientResponseReceiver
from disappeer.executor.receivers.newcontactrequestclientresponsereceiver import NewContactRequestClientResponseReceiver
from disappeer.executor.receivers.newcontactresponsereceiver import NewContactResponseReceiver
from disappeer.executor.receivers.sendnewmessagereceiver import SendNewMessageReceiver
from disappeer.executor.receivers.receivednewmessagereceiver import ReceivedNewMessageReceiver
from disappeer.models.db import databasefacade
from disappeer.models import gpgdatacontext
from disappeer.requests import requestscontroller
from disappeer.messages import messagescontroller
import inspect
import copy


class TestImports(unittest.TestCase):

    def test_constants(self):
        self.assertEqual(constants, receiverfactory.constants)

    def test_checksanityreceiver(self):
        self.assertEqual(checksanityreceiver, receiverfactory.checksanityreceiver)

    def test_handlenewcontactresponseclientresreceiver(self):
        self.assertEqual(NewContactResponseClientResponseReceiver, receiverfactory.NewContactResponseClientResponseReceiver)

    def test_inspect(self):
        self.assertEqual(inspect, receiverfactory.inspect)

    def test_handlesendnewmessageclientresponsereceiver(self):
        self.assertEqual(SendNewMessageClientResponseReceiver, receiverfactory.SendNewMessageClientResponseReceiver)

    def test_NewContactRequestClientResponseReceiver(self):
        self.assertEqual(NewContactRequestClientResponseReceiver, receiverfactory.NewContactRequestClientResponseReceiver)

    def test_NewContactResponseReceiver(self):
        self.assertEqual(NewContactResponseReceiver, receiverfactory.NewContactResponseReceiver)

    def test_SendNewMessageReceiver(self):
        self.assertEqual(SendNewMessageReceiver, receiverfactory.SendNewMessageReceiver)

    def test_ReceivedNewMessageReceiver(self):
        self.assertEqual(ReceivedNewMessageReceiver, receiverfactory.ReceivedNewMessageReceiver)


def func(nonsense):
    return 'data/databases/'


class MockMediatorWithObjects:
    """This may not be necessary for testing, and it takes a long time to initialize"""

    def __init__(self):
        self.gpg_datacontext = gpgdatacontext.GPGDataContext('tests/data/keys')
        self.database_facade = databasefacade.DatabaseFacade(self.gpg_datacontext.host_key_observer, func)
        self.requests_controller = requestscontroller.RequestsController(MagicMock(), MagicMock(), MagicMock() )
        self.message_controller = messagescontroller.MessagesController(MagicMock(), MagicMock())


class MockMediator:

    def __init__(self):
        self.gpg_datacontext = MagicMock()
        self.tor_datacontext = MagicMock()
        self.database_facade = MagicMock()
        self.requests_controller = MagicMock()
        self.message_controller = MagicMock()
        self.console_controller = MagicMock()
        self.root_params = MagicMock()


class TestReceiverFactoryClassBasics(unittest.TestCase):

    command_list = constants.command_list

    def setUp(self):
        self.controller_mediator = MockMediator()
        self.x = receiverfactory.ReceiverFactory(self.controller_mediator)

    def test_instance(self):
        self.assertIsInstance(self.x, receiverfactory.ReceiverFactory)

    def test_command_list_attr(self):
        self.assertEqual(self.x.command_list, constants.command_list)

    def test_controller_mediator_attr_set(self):
        self.assertEqual(self.x.controller_mediator, self.controller_mediator)

    def test_build_method_raises_error_with_unhandled_command(self):
        with self.assertRaises(NotImplementedError):
            result = self.x.build('wvevwewe')

    def test_build_method_builds_receiver_for_check_sanity(self):
        command_name = self.command_list.Check_Sanity
        result = self.x.build(command_name)
        self.assertIsInstance(result, checksanityreceiver.CheckSanityReceiver)

    def test_generate_kwarg_dict_returns_correct_kwarg_dict_for_HandleNewContactResponseClientResponseReceiver(self):
        kwarg_keys = NewContactResponseClientResponseReceiver.kwarg_keys
        target_dict = self._helper_generate_method_kwarg_keys_test_double(kwarg_keys)
        result = self.x.generate_methods_kwarg_dict(kwarg_keys)
        self.assertEqual(result, target_dict)

    def _helper_generate_method_kwarg_keys_test_double(self, kwarg_keys):
        target_dict = {}
        for item in self.controller_mediator.__dict__:
            current_mediator_obj = getattr(self.controller_mediator, item)
            for item in inspect.getmembers(current_mediator_obj, predicate=inspect.ismethod):
                if item[0] in kwarg_keys:
                    target_dict[item[0]] = item[1]
        return target_dict

    def test_build_method_builds_receiver_for_NewContactResponseClientResponseReceiver(self):
        command_name = self.command_list.New_Contact_Res_Client_Res
        result = self.x.build(command_name)
        self.assertIsInstance(result, NewContactResponseClientResponseReceiver)

    def test_generate_attrs_kwarg_dict(self):
        kwarg_keys = {'database_facade'}
        result = self.x.generate_attrs_kwarg_dict(kwarg_keys)
        self.assertIn('database_facade', result)
        self.assertNotIn('gpg_datacontext', result)

    def test_build_method_builds_receiver_for_SendNewMessageClientResponseReceiver(self):
        command_name = self.command_list.Send_New_Message_Client_Res
        result = self.x.build(command_name)
        self.assertIsInstance(result, SendNewMessageClientResponseReceiver)

    def test_build_method_builds_receiver_for_NewContactRequestClientResponseReceiver(self):
        command_name = self.command_list.New_Contact_Req_Client_Res
        result = self.x.build(command_name)
        self.assertIsInstance(result, NewContactRequestClientResponseReceiver)

    def test_build_method_builds_receiver_for_NewContactResponseReceiver(self):
        command_name = self.command_list.New_Contact_Res
        result = self.x.build(command_name)
        self.assertIsInstance(result, NewContactResponseReceiver)

    def test_build_method_builds_receiver_for_SendNewMessageReceiver(self):
        command_name = self.command_list.Send_New_Message
        result = self.x.build(command_name)
        self.assertIsInstance(result, SendNewMessageReceiver)

    def test_build_method_builds_receiver_for_ReceivedNewMessageReceiver(self):
        command_name = self.command_list.Received_New_Message
        result = self.x.build(command_name)
        self.assertIsInstance(result, ReceivedNewMessageReceiver)




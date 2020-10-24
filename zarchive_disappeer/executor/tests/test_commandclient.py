"""
test_commandclient.py

Test suite for command pattern command client, to run commands . . .

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock

from disappeer.constants import constants
from disappeer.executor import commandclient
from disappeer.executor import invoker
from disappeer.executor import receiverfactory
from disappeer.executor.commands import checksanitycommand
from disappeer.executor.commands.newcontactresponseclientresponsecommand import NewContactResponseClientResponseCommand
from disappeer.executor.commands.sendnewmessageclientresponsecommand import SendNewMessageClientResponseCommand
from disappeer.executor.commands.newcontactrequestclientresponsecommand import NewContactRequestClientResponseCommand
from disappeer.executor.commands.newcontactresponsecommand import NewContactResponseCommand
from disappeer.executor.commands.sendnewmessagecommand import SendNewMessageCommand
from disappeer.executor.commands.receivednewmessagecommand import ReceivedNewMessageCommand


class TestImports(unittest.TestCase):

    def test_invoker(self):
        self.assertEqual(invoker, commandclient.invoker)

    def test_receiverfactory(self):
        self.assertEqual(receiverfactory, commandclient.receiverfactory)

    def test_constants(self):
        self.assertEqual(constants, commandclient.constants)

    def test_command(self):
        self.assertEqual(checksanitycommand, commandclient.checksanitycommand)

    def test_HandleNewContactResponseClientResponseCommand(self):
        self.assertEqual(NewContactResponseClientResponseCommand, commandclient.NewContactResponseClientResponseCommand)

    def test_HandleSendNewMessageClientResponseCommand(self):
        self.assertEqual(SendNewMessageClientResponseCommand, commandclient.SendNewMessageClientResponseCommand)

    def test_NewContactRequestClientResponseCommand(self):
        self.assertEqual(NewContactRequestClientResponseCommand, commandclient.NewContactRequestClientResponseCommand)

    def test_NewContactResponseCommand(self):
        self.assertEqual(NewContactResponseCommand, commandclient.NewContactResponseCommand)

    def test_SendNewMessageCommand(self):
        self.assertEqual(SendNewMessageCommand, commandclient.SendNewMessageCommand)

    def test_ReceivedNewMessageCommand(self):
        self.assertEqual(ReceivedNewMessageCommand, commandclient.ReceivedNewMessageCommand)


class CommandClientSetupClass(unittest.TestCase):

    command_list = constants.command_list

    def setUp(self):
        self.controller_mediator = MagicMock()
        self.x = commandclient.CommandClient(self.controller_mediator)


class TestClassBasics(CommandClientSetupClass):

    def test_instance(self):
        self.assertIsInstance(self.x, commandclient.CommandClient)

    def test_command_list_attr(self):
        self.assertEqual(self.x.command_list, constants.command_list)

    def test_invoker_attr_is_invoker(self):
        self.assertIsInstance(self.x.invoker, invoker.Invoker)

    def test_controller_mediator_attr_set(self):
        self.assertEqual(self.x.controller_mediator, self.controller_mediator)

    def test_receiver_factory_attr_set_called_with_controller_mediator(self):
        self.assertIsInstance(self.x.receiver_factory, receiverfactory.ReceiverFactory)
        self.assertEqual(self.x.receiver_factory.controller_mediator, self.x.controller_mediator)

    def test_build_command_raises_error_with_unkown_command(self):
        with self.assertRaises(NotImplementedError):
            result = self.x.build_command('wvevwewe')

    def test_build_command_builds_check_sanity_command_from_command_name(self):
        target_name = self.command_list.Check_Sanity
        kwargs = dict(message='hello')
        result = self.x.build_command(target_name, **kwargs)
        self.assertIsInstance(result, checksanitycommand.CheckSanity)
        self.assertEqual(type(result.receiver), type(self.x.build_receiver(target_name)))

    def test_build_command_builds_New_Contact_Res_Client_Res_command_from_command_name(self):
        target_name = self.command_list.New_Contact_Res_Client_Res
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        result = self.x.build_command(target_name, **kwargs)
        self.assertIsInstance(result, NewContactResponseClientResponseCommand)

    def test_build_receiver_builds_check_sanity_receiver_from_command_name(self):
        command_name = self.command_list.Check_Sanity
        result = self.x.build_receiver(command_name)
        self.assertEqual(type(result), type(self.x.receiver_factory.build(command_name)))

    def test_build_command_builds_Send_New_Message_Client_Res_command_from_command_name(self):
        target_name = self.command_list.Send_New_Message_Client_Res
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        result = self.x.build_command(target_name, **kwargs)
        self.assertIsInstance(result, SendNewMessageClientResponseCommand)

    def test_build_command_builds_New_Contact_Request_Client_Res_command_from_command_name(self):
        target_name = self.command_list.New_Contact_Req_Client_Res
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        result = self.x.build_command(target_name, **kwargs)
        self.assertIsInstance(result, NewContactRequestClientResponseCommand)

    def test_build_command_builds_NewContactResponseCommand_from_command_name(self):
        target_name = self.command_list.New_Contact_Res
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        result = self.x.build_command(target_name, **kwargs)
        self.assertIsInstance(result, NewContactResponseCommand)

    def test_build_command_builds_SendNewMessageCommand_from_command_name(self):
        target_name = self.command_list.Send_New_Message
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        result = self.x.build_command(target_name, **kwargs)
        self.assertIsInstance(result, SendNewMessageCommand)

    def test_build_command_builds_ReceivedNewMessageCommand_from_command_name(self):
        target_name = self.command_list.Received_New_Message
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        result = self.x.build_command(target_name, **kwargs)
        self.assertIsInstance(result, ReceivedNewMessageCommand)


class TestCommandClientRunMethod(CommandClientSetupClass):

    def test_run_check_sanity(self):
        invoker_target = self.x.invoker.execute = MagicMock()
        kwargs = dict(message='hello')
        self.x.run(self.command_list.Check_Sanity, **kwargs)
        first_call_arg = invoker_target.call_args[0][0]
        self.assertEqual(first_call_arg.name, self.command_list.Check_Sanity)

    def test_run_New_Contact_Res_Client_Res(self):
        invoker_target = self.x.invoker.execute = MagicMock()
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        sub_1 = self.x.build_command = MagicMock()
        self.x.run(self.command_list.New_Contact_Res_Client_Res, **kwargs)
        self.assertTrue(invoker_target.called)

    def test_run_Send_New_Message_Client_Res(self):
        invoker_target = self.x.invoker.execute = MagicMock()
        kwargs = dict(payload='hello')
        sub = self.x.build_receiver = MagicMock()
        sub_1 = self.x.build_command = MagicMock()
        self.x.run(self.command_list.Send_New_Message_Client_Res, **kwargs)
        self.assertTrue(invoker_target.called)

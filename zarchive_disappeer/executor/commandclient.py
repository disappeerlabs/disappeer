"""
commandclient.py

Module for command pattern CommandClient, command runner

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.executor import invoker
from disappeer.executor import receiverfactory
from disappeer.executor.commands import checksanitycommand
from disappeer.executor.commands.newcontactresponseclientresponsecommand import NewContactResponseClientResponseCommand
from disappeer.executor.commands.sendnewmessageclientresponsecommand import SendNewMessageClientResponseCommand
from disappeer.executor.commands.newcontactrequestclientresponsecommand import NewContactRequestClientResponseCommand
from disappeer.executor.commands.newcontactresponsecommand import NewContactResponseCommand
from disappeer.executor.commands.sendnewmessagecommand import SendNewMessageCommand
from disappeer.executor.commands.receivednewmessagecommand import ReceivedNewMessageCommand


class CommandClient:

    command_list = constants.command_list

    def __init__(self, controller_mediator):
        self.controller_mediator = controller_mediator
        self.receiver_factory = receiverfactory.ReceiverFactory(self.controller_mediator)
        self.invoker = invoker.Invoker()

    def run(self, command_name, **kwargs):
        target_command = self.build_command(command_name, **kwargs)
        self.invoker.execute(target_command)

    def build_command(self, command_name, **kwargs):
        if command_name == self.command_list.Check_Sanity:
            target = checksanitycommand.CheckSanity(self.build_receiver(command_name), **kwargs)

        elif command_name == self.command_list.New_Contact_Res_Client_Res:
            target = NewContactResponseClientResponseCommand(self.build_receiver(command_name), **kwargs)

        elif command_name == self.command_list.Send_New_Message_Client_Res:
            target = SendNewMessageClientResponseCommand(self.build_receiver(command_name), **kwargs)

        elif command_name == self.command_list.New_Contact_Req_Client_Res:
            target = NewContactRequestClientResponseCommand(self.build_receiver(command_name), **kwargs)

        elif command_name == self.command_list.New_Contact_Res:
            target = NewContactResponseCommand(self.build_receiver(command_name), **kwargs)

        elif command_name == self.command_list.Send_New_Message:
            target = SendNewMessageCommand(self.build_receiver(command_name), **kwargs)

        elif command_name == self.command_list.Received_New_Message:
            target = ReceivedNewMessageCommand(self.build_receiver(command_name), **kwargs)

        else:
            raise NotImplementedError("Command client received unknown command: {}".format(command_name))

        return target

    def build_receiver(self, command_name):
        return self.receiver_factory.build(command_name)

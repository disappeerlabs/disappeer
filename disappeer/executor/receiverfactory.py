"""
receiverfactory.py

Module for ReceiverFactory class object, to build command receivers

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.executor.receivers import checksanityreceiver
from disappeer.executor.receivers.newcontactresponseclientresponsereceiver import NewContactResponseClientResponseReceiver
from disappeer.executor.receivers.newcontactrequestclientresponsereceiver import NewContactRequestClientResponseReceiver
from disappeer.executor.receivers.sendnewmessageclientresponsereceiver import SendNewMessageClientResponseReceiver
from disappeer.executor.receivers.newcontactresponsereceiver import NewContactResponseReceiver
from disappeer.executor.receivers.sendnewmessagereceiver import SendNewMessageReceiver
from disappeer.executor.receivers.receivednewmessagereceiver import ReceivedNewMessageReceiver
import inspect
from disappeer.utilities.logger import log


class ReceiverFactory:

    command_list = constants.command_list

    def __init__(self, controller_mediator):
        self.controller_mediator = controller_mediator

    def build(self, command_name):
        return self._build_receiver_from_command_name(command_name)

    def _build_receiver_from_command_name(self, command_name):
        if command_name == self.command_list.Check_Sanity:
            return checksanityreceiver.CheckSanityReceiver()

        elif command_name == self.command_list.New_Contact_Res_Client_Res:
            class_obj = NewContactResponseClientResponseReceiver

        elif command_name == self.command_list.Send_New_Message_Client_Res:
            class_obj = SendNewMessageClientResponseReceiver

        elif command_name == self.command_list.New_Contact_Req_Client_Res:
            class_obj = NewContactRequestClientResponseReceiver

        elif command_name == self.command_list.New_Contact_Res:
            class_obj = NewContactResponseReceiver

        elif command_name == self.command_list.Send_New_Message:
            class_obj = SendNewMessageReceiver

        elif command_name == self.command_list.Received_New_Message:
            class_obj = ReceivedNewMessageReceiver

        else:
            raise NotImplementedError("Receiver factory received unknown command: {}".format(command_name))

        kwarg_keys = class_obj.kwarg_keys
        key_dict = self.generate_attrs_kwarg_dict(kwarg_keys)
        receiver = class_obj(**key_dict)
        return receiver

    def generate_attrs_kwarg_dict(self, kwarg_keys):
        result_dict = {}
        for item in kwarg_keys:
            # if item in self.controller_mediator.__dict__:
            attr = getattr(self.controller_mediator, item)
            result_dict[item] = attr
        return result_dict

    def generate_methods_kwarg_dict(self, kwarg_keys):
        result_dict = {}
        for item in self.controller_mediator.__dict__:
            current_mediator_obj = getattr(self.controller_mediator, item)
            for item in inspect.getmembers(current_mediator_obj, predicate=inspect.ismethod):
                if item[0] in kwarg_keys:
                    result_dict[item[0]] = item[1]
        return result_dict

"""
sendnewmessageclientresponsecommand.py

Module for SendNewMessageClientResponseCommand class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


from disappeer.constants import constants
from disappeer.executor.commands import abstractcommand
command_list = constants.command_list


class SendNewMessageClientResponseCommand(abstractcommand.AbstractCommand):

    def __init__(self, receiver, **kwargs):
        super().__init__(receiver, **kwargs)

    @property
    def name(self):
        return command_list.Send_New_Message_Client_Res

    @property
    def valid_kwarg_keys(self):
        return {'payload'}

    def execute(self):
        self.receiver.execute(self.payload)


"""
newcontactresponseclientrescommand.py

Module for command pattern concrete command newcontactresponseclientrescommand

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.executor.commands import abstractcommand

command_list = constants.command_list


class NewContactResponseClientResponseCommand(abstractcommand.AbstractCommand):

    def __init__(self, receiver, **kwargs):
        super().__init__(receiver, **kwargs)

    @property
    def name(self):
        return command_list.New_Contact_Res_Client_Res

    @property
    def valid_kwarg_keys(self):
        return {'payload'}

    def execute(self):
        self.receiver.execute(self.payload)

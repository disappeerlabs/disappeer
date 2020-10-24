"""
checksanitycommand.py

Module for command pattern CheckSanityCommand class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


from disappeer.constants import constants
from disappeer.executor.commands import abstractcommand

command_list = constants.command_list


class CheckSanity(abstractcommand.AbstractCommand):

    def __init__(self, receiver, **kwargs):
        super().__init__(receiver, **kwargs)
        self.message = kwargs['message']

    @property
    def name(self):
        return command_list.Check_Sanity

    @property
    def valid_kwarg_keys(self):
        return {'message'}

    def execute(self):
        self.receiver.log_message(self.message)

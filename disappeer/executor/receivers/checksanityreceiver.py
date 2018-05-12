"""
checksanityreceiver.py

Module for command pattern check sanity receiver object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.utilities.logger import log

command_list = constants.command_list


class CheckSanityReceiver(abstractreceiver.AbstractReceiver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        suffix = 'Receiver'
        return command_list.Check_Sanity + suffix

    @property
    def valid_kwarg_keys(self):
        return set()

    def execute(self):
        pass

    def log_message(self, message):
        log.debug("Check Sanity Receiver: {}.".format(message))

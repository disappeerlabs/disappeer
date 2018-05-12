"""
controllermediator.py

Module for ControllerMediator mediator object for controllers

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


class ControllerMediator:

    def __init__(self,
                 database_facade,
                 gpg_data_context,
                 tor_datacontext,
                 requests_controller,
                 message_controller,
                 console_controller,
                 root_params):
        self.database_facade = database_facade
        self.gpg_datacontext = gpg_data_context
        self.tor_datacontext = tor_datacontext
        self.requests_controller = requests_controller
        self.message_controller = message_controller
        self.console_controller = console_controller
        self.root_params = root_params


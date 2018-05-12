"""
clientcontroller.py

Module for the ClientController class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.net.bases import clientfactory
from disappeer.net.bases import threadmanagers


class ClientController:

    def __init__(self, client_type, argnamespace):
        self.client_factory = clientfactory.ClientFactory(client_type, argnamespace)
        self.client = threadmanagers.ClientThreadManager(self.client_factory)

    def start(self):
        self.client.start()

    def stop(self):
        self.client.stop()

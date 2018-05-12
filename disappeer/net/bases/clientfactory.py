"""
clientfactory.py

Module for the ClientFactory class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.net.contact import contactrequestclient
from disappeer.net.contactresponse import contactresponseclient
from disappeer.net.message import messageclient


class ClientFactory:

    def __init__(self, client_type, argnamespace):
        self.client_type = client_type
        self.name = self.client_type
        self.argnamespace = argnamespace

    def build(self):
        if self.client_type == 'contact_request':
            return self.create_contact_request_client()
        elif self.client_type == 'contact_response':
            return self.create_contact_response_client()
        elif self.client_type == 'send_message':
            return self.create_message_client()

    def create_contact_request_client(self):
        # TODO: Should command be hardcoded into the Client class object itself?
        self.argnamespace.command = 'REQ'
        client = contactrequestclient.ContactRequestClient(self.argnamespace)
        return client

    def create_contact_response_client(self):
        client = contactresponseclient.ContactResponseClient(self.argnamespace)
        return client

    def create_message_client(self):
        client = messageclient.MessageClient(self.argnamespace)
        return client

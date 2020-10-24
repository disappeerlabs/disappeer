"""
networkservers.py

Module for NetworkServers class object, contains references to and controls for network servers

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.net.contact import contactrequestserver
from disappeer.net.contactresponse import contactresponseserver
from disappeer.net.message import messageserver
from disappeer.net.bases import servercontroller
from disappeer.net.bases import threadmanagers


class NetworkServers:

    def __init__(self, queue):
        self.queue = queue
        self.contact_request_server = servercontroller.ServerController(self.queue,
                                                                        contactrequestserver.ContactRequestServerFactory,
                                                                        threadmanagers.ServerThreadManager)
        self.contact_response_server = servercontroller.ServerController(self.queue,
                                                                         contactresponseserver.ContactResponseServerFactory,
                                                                         threadmanagers.ServerThreadManager)
        self.message_server = servercontroller.ServerController(self.queue,
                                                                messageserver.MessageServerFactory,
                                                                threadmanagers.ServerThreadManager)

    def start_network_services(self):
        self.contact_request_server.start()
        self.contact_response_server.start()
        self.message_server.start()

    def stop_network_services(self):
        self.contact_request_server.stop()
        self.contact_response_server.stop()
        self.message_server.stop()

    def are_running(self):
        request = self.contact_request_server.get_status()
        response = self.contact_response_server.get_status()
        message = self.message_server.get_status()
        result = all([request, response, message])
        return result


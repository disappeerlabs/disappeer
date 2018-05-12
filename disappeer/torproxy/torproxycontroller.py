"""
tornetcontroller.py

Module for TorNetController class object, to control tor proxy service threads, access addresses etc.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.torproxy import torproxyservice
from disappeer.constants import constants
from disappeer import settings


class TorProxyController:

    def __init__(self, queue):
        self.queue = queue
        self.request_proxy_thread = None
        self.response_proxy_thread = None
        self.message_proxy_thread = None

    def start_request_proxy(self, persistent=False, tor_key_dir=None):
        name = constants.command_list.Tor_Proxy_Request_Server
        port = settings.port_contact_request_server
        self.request_proxy_thread = torproxyservice.TorProxyServiceThread(name, port, self.queue, persistent=persistent, tor_key_dir=tor_key_dir)
        self.request_proxy_thread.start()

    def start_response_proxy(self, persistent=False, tor_key_dir=None):
        name = constants.command_list.Tor_Proxy_Response_Server
        port = settings.port_contact_response_server
        self.response_proxy_thread = torproxyservice.TorProxyServiceThread(name, port, self.queue, persistent=persistent, tor_key_dir=tor_key_dir)
        self.response_proxy_thread.start()

    def start_message_proxy(self, persistent=False, tor_key_dir=None):
        name = constants.command_list.Tor_Proxy_Message_Server
        port = settings.port_message_server
        self.message_proxy_thread = torproxyservice.TorProxyServiceThread(name, port, self.queue, persistent=persistent, tor_key_dir=tor_key_dir)
        self.message_proxy_thread.start()

    def start_all_proxies(self, persistent=False, tor_key_dir=None):
        self.start_request_proxy(persistent=persistent, tor_key_dir=tor_key_dir)
        self.start_response_proxy(persistent=persistent, tor_key_dir=tor_key_dir)
        self.start_message_proxy(persistent=persistent, tor_key_dir=tor_key_dir)

    def stop_all_proxies(self):
        if self.request_proxy_thread is not None:
            self.request_proxy_thread.quit()
        if self.response_proxy_thread is not None:
            self.response_proxy_thread.quit()
        if self.message_proxy_thread is not None:
            self.message_proxy_thread.quit()

    def is_any_alive(self):
        try:
            req = self.request_proxy_thread.is_alive()
        except AttributeError:
            req = False

        try:
            res = self.response_proxy_thread.is_alive()
        except AttributeError:
            res = False

        try:
            msg = self.message_proxy_thread.is_alive()
        except AttributeError:
            msg = False

        result = any([req, res, msg])
        return result

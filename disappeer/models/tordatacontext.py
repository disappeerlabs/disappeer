"""
tordatacontext.py

Module for TorDataContext class object, to hold observables for onion addresses

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import observable


class TorDataContext:

    def __init__(self, get_user_tor_keys_dir_method):
        self.get_user_tor_keys_dir_method = get_user_tor_keys_dir_method
        self.tor_request_proxy_addr = observable.Observable('None...')
        self.tor_response_proxy_addr = observable.Observable('None...')
        self.tor_message_proxy_addr = observable.Observable('None...')

    def get_tor_request_proxy_addr(self):
        result = self.tor_request_proxy_addr.get()
        return result

    def set_tor_request_proxy_addr(self, data):
        self.tor_request_proxy_addr.set(data)

    def get_tor_response_proxy_addr(self):
        result = self.tor_response_proxy_addr.get()
        return result

    def set_tor_response_proxy_addr(self, data):
        self.tor_response_proxy_addr.set(data)

    def get_tor_message_proxy_addr(self):
        result = self.tor_message_proxy_addr.get()
        return result

    def set_tor_message_proxy_addr(self, data):
        self.tor_message_proxy_addr.set(data)

    def add_tor_request_proxy_addr_observer(self, observer):
        self.tor_request_proxy_addr.add_observer(observer)

    def add_tor_response_proxy_addr_observer(self, observer):
        self.tor_response_proxy_addr.add_observer(observer)

    def add_tor_message_proxy_addr_observer(self, observer):
        self.tor_message_proxy_addr.add_observer(observer)

    def get_user_tor_keys_dir(self, keyid_name):
        result = self.get_user_tor_keys_dir_method(keyid_name)
        return result

"""
rootparamesters.py

Module for RootParameters object, for encapsulating root params to be passed into controllers.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import observable


class RootParameters:

    def __init__(self, root_obj, root_view, root_queue, database_facade, host_key_observer):
        self.root = root_obj
        self.root_view = root_view
        self.root_queue = root_queue
        self.database_facade = database_facade
        self.host_key_observer = host_key_observer
        self.tor_proxy_running_observable = observable.Observable(False)
        self.host_key_session_passphrase_observable = observable.Observable()

    def get_tor_net_frame(self):
        return self.root_view.left_panel.tor_net_frame

    def get_requests_frame(self):
        return self.root_view.left_panel.requests_frame

    def get_gpg_frame(self):
        return self.root_view.left_panel.gpg_frame

    def get_messages_frame(self):
        return self.root_view.left_panel.messages_frame

    def get_console_frame(self):
        return self.root_view.right_panel.console_frame

    def get_root_menubar(self):
        return self.root_view.root_menubar

    def get_app_menu_obj(self):
        return self.root_view.app_menu

    def get_file_menu_obj(self):
        return self.root_view.file_menu

    def get_gpg_menu_obj(self):
        return self.root_view.gpg_menu

    def get_host_key_id(self):
        key_vals = self.host_key_observer.get()
        split = key_vals.split(',')
        key_id = split.pop().strip()
        return key_id

    def set_tor_proxy_running_observable(self, val):
        self.tor_proxy_running_observable.set(val)

    def get_tor_proxy_running_observable(self):
        return self.tor_proxy_running_observable.get()

    def set_session_passphrase_observable(self, val):
        self.host_key_session_passphrase_observable.set(val)

    def get_session_passphrase_observable(self):
        result = self.host_key_session_passphrase_observable.get()
        return result

    def add_session_passphrase_observable_callback(self, func):
        self.host_key_session_passphrase_observable.add_callback(func)

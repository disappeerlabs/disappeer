"""
torproxyservice.py

Module for TorProxyService and TorProxyServiceThread class objects.
For running ephemeral hidden services.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import threading
import stem
from stem.control import Controller
import time
from disappeer import settings
import os
from disappeer.constants import constants


class TorProxyService:

    def __init__(self, name, port, queue, tor_key_dir=None):
        self.name = name
        self.port = port
        self.queue = queue
        self.tor_key_dir = tor_key_dir
        self.controller_port = settings.port_tor_controller
        self.running = True
        self.onion_address_obj = None

    def get_controller(self):
        try:
            controller = Controller.from_port(port=self.controller_port)
            return controller
        except stem.SocketError as err:
            self.put_error_to_queue(err)
            return None

    def authenticate_controller(self):
        self.put_to_queue('Authenticating...')
        try:
            self.controller.authenticate()
            return self.controller
        except stem.connection.IncorrectSocketType as err:
            self.put_error_to_queue(err)
            return None

    def create_ephemeral_address(self):
        self.put_to_queue('Creating...')
        try:
            onion_address_obj = self.controller.create_ephemeral_hidden_service(self.port)
            return onion_address_obj
        except stem.ControllerError as err:
            self.put_error_to_queue(err)
            return None

    def resume_persistent_address(self, key_type, key_content):
        self.put_to_queue('Resuming persistent...')
        try:
            self.onion_address_obj = self.controller.create_ephemeral_hidden_service(self.port,
                                                                                     key_type=key_type,
                                                                                     key_content=key_content)
            return self.onion_address_obj
        except stem.ControllerError as err:
            self.put_error_to_queue(err)
            return None

    def remove_ephemeral_address(self, service_id):
        self.put_to_queue('Exiting...')
        try:
            self.controller.remove_ephemeral_hidden_service(service_id)
        except stem.ControllerError as err:
            self.put_error_to_queue(err)
            return None

    def run_check(self):
        while self.running:
            time.sleep(3)

    def put_to_queue(self, msg_string):
        payload = self.build_payload(msg_string)
        self.queue.put(payload)

    def build_payload(self, addr_msg_string):
        payload = dict(desc=self.name, address=addr_msg_string)
        return payload

    def put_error_to_queue(self, error_msg):
        payload = self.build_error_payload(error_msg)
        self.queue.put(payload)

    def build_error_payload(self, error_msg):
        payload = dict(desc=constants.command_list.Tor_Proxy_Error, name=self.name, error=error_msg)
        return payload

    def build_address_string(self):
        suffix = '.onion'
        target_address = self.onion_address_obj.service_id + suffix
        return target_address

    def stop(self):
        self.put_to_queue("Stopping...")
        self.running = False

    def key_file_path(self):
        suffix = '_Key'
        key_file_name = self.name + suffix
        key_file_path = self.tor_key_dir + key_file_name
        return key_file_path

    def start(self):
        self.controller = self.get_controller()
        if self.controller is None:
            return

        with self.controller:
            if not self.authenticate_controller():
                return None

            self.onion_address_obj = self.create_ephemeral_address()
            if self.onion_address_obj is None:
                return None

            self.put_to_queue(self.build_address_string())

            self.run_check()

            self.remove_ephemeral_address(self.onion_address_obj.service_id)
            self.put_to_queue('Done')

    def start_persistent(self):
        self.controller = self.get_controller()
        if self.controller is None:
            return

        with self.controller:

            if not self.authenticate_controller():
                return None

            if not os.path.exists(self.key_file_path()):
                self.onion_address_obj = self.create_ephemeral_address()
                if self.onion_address_obj is None:
                    return None

                self._write_key_file()

            else:
                key_type, key_content = self._read_key_file()

                self.onion_address_obj = self.resume_persistent_address(key_type, key_content)
                if self.onion_address_obj is None:
                    return None

            self.put_to_queue(self.build_address_string())
            self.run_check()

            self.remove_ephemeral_address(self.onion_address_obj.service_id)
            self.put_to_queue('Done')

    def _write_key_file(self):
        self.put_to_queue('Creating persistent...')
        with open(self.key_file_path(), 'w') as key_file:
            key_file.write('{}:{}'.format(self.onion_address_obj.private_key_type,
                                          self.onion_address_obj.private_key))

    def _read_key_file(self):
        with open(self.key_file_path()) as key_file:
            key_type, key_content = key_file.read().split(':', 1)
        return key_type, key_content


class TorProxyServiceThread(threading.Thread):

    def __init__(self, name, port, queue, persistent=False, tor_key_dir=None):
        threading.Thread.__init__(self, name=name, daemon=True)
        self.persistent = persistent
        self.tor_key_dir = tor_key_dir
        self.proxy = TorProxyService(name, port, queue, tor_key_dir=self.tor_key_dir)

    def run(self):
        if self.persistent:
            self.proxy.start_persistent()
        else:
            self.proxy.start()

    def quit(self):
        self.proxy.stop()


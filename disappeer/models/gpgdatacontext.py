"""
gpgdatacontext.py

Module for GPGDataContext class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import observable
from disappeer.gpg.helpers import keylistobservable
from disappeer.gpg.helpers import hostkeyobservable
from disappeer import settings
import os
from disappeer.gpg.agents import keyring


class GPGDataContext:

    def __init__(self, key_home_path):
        self.key_home_path = key_home_path
        self.home_dir_observable = self.config_home_dir_observable()
        self.key_ring = self.config_key_ring()
        self.key_list_observable = self.config_key_list_observable()
        self.host_key_observable = self.config_host_key_observable()
        self.home_dir_observer = self.config_home_dir_observer()
        self.host_key_observer = self.config_host_key_observer()

    def config_home_dir_observable(self):
        home_dir_observable = observable.Observable()
        self.set_permissions(self.key_home_path)
        home_dir_observable.set(self.key_home_path)
        return home_dir_observable

    def config_key_ring(self):
        key_ring = keyring.KeyRing(self.home_dir_observable.get())
        self.home_dir_observable.add_observer(key_ring)
        return key_ring

    def config_key_list_observable(self):
        key_list_observable = keylistobservable.KeyListObservable(self.key_ring)
        self.home_dir_observable.add_observer(key_list_observable)
        return key_list_observable

    def config_host_key_observable(self):
        host_key_observable = hostkeyobservable.HostKeyObservable(self.key_ring)
        self.home_dir_observable.add_observer(host_key_observable)
        return host_key_observable

    def set_home_dir(self, new_home_path):
        self.set_permissions(new_home_path)
        self.home_dir_observable.set(new_home_path)

    def get_home_dir(self):
        return self.home_dir_observable.get()

    def add_home_dir_observer(self, observer):
        self.home_dir_observable.add_observer(observer)

    def set_key_list(self):
        self.key_list_observable.set(None)

    def get_raw_key_list(self):
        return self.key_ring.get_raw_key_list()

    def add_key_list_observer(self, observer):
        self.key_list_observable.add_observer(observer)

    def add_host_key_observer(self, observer):
        self.host_key_observable.add_observer(observer)

    def set_host_key(self):
        self.host_key_observable.set(None)

    def get_host_key(self):
        result = self.host_key_observable.get()
        return result

    def get_host_key_id(self):
        """
        Pop the keyid from the end of the host key return val
        """
        key_vals = self.get_host_key()
        split = key_vals.split(',')
        return split.pop().strip()

    def get_host_key_fingerprint(self):
        keyid = self.get_host_key_id()
        key_dict = self.get_key_dict_by_identifier(keyid)
        fingerprint = key_dict['fingerprint']
        return fingerprint

    def import_gpg_pub_key_to_key_ring(self, pub_key):
        self.key_ring.import_key(pub_key)

    def export_pubkey_from_key_ring(self, identifier):
        result = self.key_ring.export_key(identifier)
        return result

    def get_key_dict_by_identifier(self, identifier):
        key_list = self.get_raw_key_list()
        for key in key_list:
            if key['fingerprint'] == identifier:
                return key
            elif key['keyid'] == identifier:
                return key
        return None

    def set_permissions(self, path):
        os.chmod(path, 0o700)

    ####################
    # OBSERVER OBJECTS #
    ####################

    def config_home_dir_observer(self):
        home_dir_observer = observable.Observable()
        self.add_home_dir_observer(home_dir_observer)
        return home_dir_observer

    def get_home_dir_observer(self):
        return self.home_dir_observer

    def config_host_key_observer(self):
        host_key_observer = observable.Observable()
        self.add_host_key_observer(host_key_observer)
        return host_key_observer

    def get_host_key_observer(self):
        return self.host_key_observer


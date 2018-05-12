"""
gpgpubkeyvalidator.py

Module for GPGPubKeyValidator class object.
Object takes gpg pubkey as input, imports to tempdir, validates with keyring

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import keyring
import tempfile


class GPGPubKeyValidator:

    def __init__(self, gpg_pub_key):
        self.target_pubkey = gpg_pub_key
        self.temp_dir = self.create_temp_dir()
        self.temp_dir_name = self.temp_dir.name
        self.key_ring = keyring.KeyRing(self.temp_dir_name)
        self.result = None
        self.valid = None
        self.key_dict = None
        self.validate()

    def validate(self):
        self.import_pubkey_to_keyring()
        if self.result.count == 1:
            self.valid = True
            self.key_dict = self.key_ring.get_raw_key_list()[0]
        else:
            self.valid = False

    def import_pubkey_to_keyring(self):
        self.result = self.key_ring.import_key(self.target_pubkey)
        return self.result

    def create_temp_dir(self):
        temp_dir = tempfile.TemporaryDirectory()
        return temp_dir

    def close_temp_dir(self):
        self.temp_dir.cleanup()

    def __del__(self):
        try:
            self.close_temp_dir()
        except (AttributeError, FileNotFoundError):
            pass

"""
keyring.py

Module for the GPG KeyRing class.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import gpgagent


class KeyRing(gpgagent.GPGAgent):

    def __init__(self, key_dir):
        super().__init__(key_dir)

    def get_raw_key_list(self, secret=False):
        result = self.gpg.list_keys(secret=secret)
        return result

    def export_key(self, identifier):
        result = self.gpg.export_keys(identifier)
        return result

    def import_key(self, pub_key):
        result = self.gpg.import_keys(pub_key)
        return result

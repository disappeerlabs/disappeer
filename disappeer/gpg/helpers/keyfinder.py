"""
keyfinder.py

Module for KeyFinder class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


class KeyFinder:

    def __init__(self, key_ring):
        self.key_ring = key_ring

    def find(self, identifier):
        key_list = self.key_ring.get_raw_key_list()
        search = self._search_list(key_list, identifier)
        return search

    def find_secret(self, identifier):
        key_list = self.key_ring.get_raw_key_list(secret=True)
        search = self._search_list(key_list, identifier)
        return search

    def _search_list(self, key_list, identifier):
        for key in key_list:
            if key['fingerprint'] == identifier:
                return key
            elif key['keyid'] == identifier:
                return key
        return None

    def get_fingerprint_by_keyid(self, keyid):
        key = self.find(keyid)
        if key is None:
            return None
        else:
            fingerprint = key['fingerprint']
            return fingerprint

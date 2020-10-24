"""
keydeleter.py

Module for KeyDeleter class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import gpgagent


class KeyDeleter(gpgagent.GPGAgent):

    def __init__(self, keydir):
        super().__init__(keydir)

    def execute(self, key_fingerprint_list):
        # TODO: investigate: Delete secret key fails without passphrase
        #           - True flag allows to delete secret key
        #           - but python-gnupg does not provide interface for passphrase
        # prep = self.gpg.delete_keys(key_fingerprint_list, True)
        result = self.gpg.delete_keys(key_fingerprint_list)
        return result

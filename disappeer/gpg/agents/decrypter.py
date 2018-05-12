"""
decrypter.py

Module for Decrypter gpg agent class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import gpgagent


class Decrypter(gpgagent.GPGAgent):

    def __init__(self, key_dir):
        super().__init__(key_dir)

    def execute(self, ciphertext, passphrase):
        result = self.gpg.decrypt(ciphertext, passphrase=passphrase)
        return result

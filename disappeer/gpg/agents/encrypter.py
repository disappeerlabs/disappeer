"""
encrypter.py

Module for the Encrypter class gpg agent.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import gpgagent


class Encrypter(gpgagent.GPGAgent):

    def __init__(self, key_dir):
        super().__init__(key_dir)

    def execute(self, plaintext, fingerprint):
        result = self.gpg.encrypt(plaintext, fingerprint, always_trust=True)
        return result


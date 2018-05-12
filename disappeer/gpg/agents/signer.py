"""
signer.py

Module for Signer gpg agent class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import gpgagent


class Signer(gpgagent.GPGAgent):

    def __init__(self, key_dir):
        super().__init__(key_dir)

    def execute(self, message, fingerprint, passphrase, detach=False):
        result = self.gpg.sign(message,
                               keyid=fingerprint,
                               passphrase=passphrase,
                               detach=detach)
        return result

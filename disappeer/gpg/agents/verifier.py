"""
verifier.py

Module for the Verifier gpg agent class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import gpgagent


class Verifier(gpgagent.GPGAgent):

    def __init__(self, keydir):
        super().__init__(keydir)

    def execute(self, message):
        result = self.gpg.verify(message)
        return result


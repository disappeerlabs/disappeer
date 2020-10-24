"""
passphrasevalidator.py

Module for PassphraseValidator class object.
Takes homedir, host key id, and passphrase, verifies passphrase against a sig.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import signer
from disappeer.gpg.agents import verifier


class PassphraseValidator:

    def __init__(self, homedir, host_key_id, passphrase):
        self.home_dir = homedir
        self.host_key_id = host_key_id
        self.passphrase = passphrase
        self.msg = 'hello world'
        self.result = None

    def sign(self):
        sign_agent = signer.Signer(self.home_dir)
        result = sign_agent.execute(self.msg, self.host_key_id, self.passphrase)
        return result

    def verify(self, msg):
        verify_agent = verifier.Verifier(self.home_dir)
        result = verify_agent.execute(msg)
        return result

    def validate(self):
        sig = self.sign()
        self.result = self.verify(str(sig))
        return self.result.valid

    def get_error_msg(self):
        try:
            msg = self.result.stderr
        except AttributeError as err:
            return None
        return msg


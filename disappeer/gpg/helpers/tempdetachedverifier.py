"""
tempdetachedverifier.py

Module for TempDetachedVerifier class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.helpers import tempkeyring
from disappeer.gpg.agents import detachedverifier
import tempfile


class TempDetachedVerifier(tempkeyring.TempKeyRing):

    def __init__(self, gpg_pub_key, sig_dict):
        super().__init__()
        self.detached_verifier = detachedverifier.DetachedVerifier(self.temp_dir_name)
        self.gpg_pub_key = gpg_pub_key
        self.sig_dict = sig_dict
        self.error = None
        self.valid = None
        self.run()

    def run(self):
        self.is_key_valid()
        if self.error is not None:
            return
        self.is_sig_dict_valid()
        if self.error is not None:
            return
        self.verify_sig()

    def verify_sig(self):
        sig_bytes = bytes(self.sig_dict['sig'], 'utf-8')
        data_bytes = bytes(self.sig_dict['data'], 'utf-8')

        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(sig_bytes)
            tmp_file.seek(0)
            verify_detached = self.detached_verifier.execute(tmp_file.name, data_bytes)
            if not verify_detached.valid:
                self.set_error(verify_detached.stderr)
            self.valid = verify_detached.valid
            return verify_detached.valid

    def is_sig_dict_valid(self):
        target_list = ['sig', 'data']
        if all(name in target_list for name in self.sig_dict):
            return True
        else:
            msg = 'Error: sig dict is false: ' + str(self.sig_dict)
            self.set_error(msg)
            return False

    def is_key_valid(self):
        result = self.key_ring.import_key(self.gpg_pub_key)
        if result.count == 0:
            self.set_error(result.stderr)
            return False
        else:
            return True

    def set_error(self, err_msg):
        self.error = err_msg
        self.valid = False




"""
hostkeyobservable.py

Module for HostKeyObservable class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import observable
from disappeer.gpg.helpers import keylistformatter
from disappeer import settings


class HostKeyObservable(observable.Observable):
    """
    Adapted observable to keep track of key list,
    while keeping it formatted.
    """

    def __init__(self, keyring):
        super().__init__()
        self.key_ring = keyring
        self.key_formatter = keylistformatter.KeyListFormatter()
        self.key_list = self._run_ops()

    def get(self):
        if len(self.key_list) == 0:
            return "No Private Key in Ring"
        else:
            return self.key_list[0]

    def set(self, param):
        self.key_list = self._run_ops()
        self.run_callbacks()
        self.write_pub_key_to_file()

    def _run_ops(self):
        raw_list = self.key_ring.get_raw_key_list(secret=True)[:1]
        result = self.key_formatter.format(raw_list)
        return result

    def get_pub_key(self):
        current_key_id = self.get().split(', ').pop()
        result = self.key_ring.export_key(current_key_id)
        return result

    def write_pub_key_to_file(self):
        text = self.get_pub_key()
        with open(settings.gpg_host_pubkey, 'w') as f:
            f.write(text)

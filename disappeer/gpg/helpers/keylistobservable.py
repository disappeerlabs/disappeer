"""
keylistobservable.py

Module for the KeyListObservable class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import observable
from disappeer.gpg.helpers import keylistformatter


class KeyListObservable(observable.Observable):
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
        return self.key_list

    def set(self, param):
        self.key_list = self._run_ops()
        self.run_callbacks()

    def _run_ops(self):
        raw_list = self.key_ring.get_raw_key_list()
        result = self.key_formatter.format(raw_list)
        return result

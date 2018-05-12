"""
tempkeyring.py

Module for TempKeyRing class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import keyring
import tempfile


class TempKeyRing:

    def __init__(self):
        self.temp_dir = self.create_temp_dir()
        self.temp_dir_name = self.temp_dir.name
        self.key_ring = keyring.KeyRing(self.temp_dir_name)

    def create_temp_dir(self):
        temp_dir = tempfile.TemporaryDirectory()
        return temp_dir

    def close_temp_dir(self):
        self.temp_dir.cleanup()

    def __del__(self):
        try:
            self.close_temp_dir()
        except (AttributeError, FileNotFoundError):
            pass

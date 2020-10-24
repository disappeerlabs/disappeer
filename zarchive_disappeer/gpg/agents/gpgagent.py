"""
gpgagent.py

Module for GPGAgent base class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import gnupg


class GPGAgent:

    def __init__(self, key_dir):
        self.home = key_dir
        self.gpg = self.get_gpg_obj()

    def get_gpg_obj(self):
        """Create a new gpg obj at self,home and return it"""
        gpg_obj = gnupg.GPG(gnupghome=self.home)
        gpg_obj.encoding = 'utf-8'
        return gpg_obj

    def set(self, key_dir):
        self.home = key_dir
        self.gpg = self.get_gpg_obj()
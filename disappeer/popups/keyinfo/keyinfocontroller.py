"""
keyinfocontroller.py

Module for KeyInfoController popup controller

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.keyinfo import keyinfoview
from disappeer.popups.bases import basepopupcontroller


class KeyInfoController(basepopupcontroller.BasePopupController):

    def __init__(self, root, key_dict):
        super().__init__(root)
        self.key_dict = key_dict
        self.view = keyinfoview.KeyInfoView(self.window, self.key_dict)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Key Info'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.close_window)

    def close_window(self, event):
        self.set_output_and_close(self.key_dict)

"""
getsessionpassphrasecontroller.py

Module for the popup GetSessionPassphraseController

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.getsessionpassphrase import getsessionpassphraseview


class GetSessionPassphraseController(basepopupcontroller.BasePopupController):

    def __init__(self, root):
        super().__init__(root)
        self.view = getsessionpassphraseview.GetSessionPassphraseView(self.window)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Enter Session Passphrase'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.submit_button.bind("<ButtonRelease-1>", self.submit_button_clicked)
        self.view.passphrase_entry.focus_force()

    def submit_button_clicked(self, event):
        user_input = self.view.passphrase_entry.get()
        self.set_output_and_close(user_input)




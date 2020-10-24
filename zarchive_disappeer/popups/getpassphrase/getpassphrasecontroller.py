"""
getpassphrasecontroller.py

Module for popup GetPassphraseController class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.getpassphrase import getpassphraseview
from disappeer.popups.bases import basepopupcontroller


class GetPassphraseController(basepopupcontroller.BasePopupController):

    def __init__(self, root):
        super().__init__(root)
        self.view = getpassphraseview.GetPassphraseView(self.window)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Enter Passphrase'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.submit_button.bind("<ButtonRelease-1>", self.submit_button_clicked)
        self.view.passphrase_entry.focus_force()

    def submit_button_clicked(self, event):
        user_input = self.view.passphrase_entry.get()
        self.set_output_and_close(user_input)


"""
peercontactcontroller.py

Module for PeerContactController module and class object for PeerContact popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.peercontact import peercontactview
from disappeer.gpg.helpers import gpgpubkeyvalidator


class PeerContactController(basepopupcontroller.BasePopupController):

    def __init__(self, root, data_record):
        super().__init__(root)
        self.data_record = data_record
        self.pubkey_validator = gpgpubkeyvalidator.GPGPubKeyValidator(self.data_record.gpg_pub_key)

        if self.pubkey_validator.valid:
            self.view = peercontactview.PeerContactView(self.window, self.pubkey_validator.key_dict)
            self.config_event_bindings()
        else:
            self.handle_invalid_data_record()

    @property
    def title(self):
        return 'Peer Contact'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.send_button.bind("<ButtonRelease-1>", self.send_button_clicked)
        self.view.delete_button.bind("<ButtonRelease-1>", self.delete_button_clicked)

    def handle_invalid_data_record(self):
        self.set_output_and_close('invalid')

    def send_button_clicked(self, event):
        self.set_output_and_close('send')

    def delete_button_clicked(self, event):
        self.set_output_and_close('delete')


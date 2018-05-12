"""
displaysentrequestcontroller.py

Module for popup DisplaySentRequestController, to display info in popup on click of sent request item.
Display host address and pubkey info

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.displaysentrequest import displaysentrequestview
from disappeer.popups.bases import basepopupcontroller
from disappeer.gpg.helpers import gpgpubkeyvalidator


class DisplaySentRequestController(basepopupcontroller.BasePopupController):

    def __init__(self, root, gpg_pub_key_string, onion_address):
        super().__init__(root)
        self.gpg_pub_key = gpg_pub_key_string
        self.address = onion_address
        self.pubkey_validator = gpgpubkeyvalidator.GPGPubKeyValidator(self.gpg_pub_key)
        if self.pubkey_validator.valid:
            self.view = displaysentrequestview.DisplaySentRequestView(self.window,
                                                                      self.pubkey_validator.key_dict,
                                                                      self.address)
            self.config_event_bindings()
        else:
            pass
            # TODO: ADD ELSE CLAUSE FOR INVALID KEY

    @property
    def title(self):
        return 'Sent Request Peer Info'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)



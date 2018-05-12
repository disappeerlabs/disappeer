"""
peerconnectcontroller.py

Module for controller for PeerConnect popup window.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.peerconnect import peerconnectview
from disappeer.popups.bases import basepopupcontroller
import tkinter


class PeerConnectController(basepopupcontroller.BasePopupController):

    def __init__(self, root):
        super().__init__(root)
        self.view = peerconnectview.PeerConnectView(self.window)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Peer Connect'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.connect_button.bind("<ButtonRelease-1>", self.connect_button_clicked)

    def connect_button_clicked(self, event):
        host = self.view.host_entry_var.get()
        port = self.view.port_entry_var.get()
        result = (host, port)
        self.set_output_and_close(result)

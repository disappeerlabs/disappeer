"""
peerconnectview.py

View module for the PeerConnect popup window

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import constants
from disappeer.constants import styling
from disappeer.utilities import helpers
import logging

log = logging.getLogger(constants.title)


class PeerConnectView:
    """
    View for Peer Connect popup window.
    """

    def __init__(self, window):
        self.window = window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=0)

        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_form_elements()
        self.config_form_buttons()
        self.set_default_vals()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, background=styling.background_color, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Form elements frame row
        self.main_frame.rowconfigure(0, weight=0)

        # Form buttons frame row
        self.main_frame.rowconfigure(1, weight=0)

    def config_form_elements(self):
        """
        For each item in key info ordered fields list, create label and entry.
        Label is from ordered field list. Entry is corresponding val from self.key_dict.
        """
        elements_frame = tkinter.Frame(self.main_frame, **styling.new_key_elements_frame)
        elements_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

        # column for labels
        elements_frame.columnconfigure(0, weight=0)
        # column for entries
        elements_frame.columnconfigure(1, weight=1)
        # row for host
        elements_frame.rowconfigure(0, weight=0)
        # row for port
        elements_frame.rowconfigure(1, weight=0)

        host_label = tkinter.Label(elements_frame, text="Host:", **styling.label_args)
        host_label.grid(row=0, column=0, sticky='E', padx=(0, 5), pady=(5, 5))

        self.host_entry_var = tkinter.StringVar()
        host_entry = tkinter.Entry(elements_frame, textvariable=self.host_entry_var, **styling.entry_field_args)
        host_entry.grid(row=0, column=1, sticky=styling.sticky_ew, ipady=1)

        port_label = tkinter.Label(elements_frame, text="Port:", **styling.label_args)
        port_label.grid(row=1, column=0, sticky='E', padx=(0, 5), pady=(5, 5))

        self.port_entry_var = tkinter.StringVar()
        port_entry = tkinter.Entry(elements_frame, textvariable=self.port_entry_var,  **styling.entry_field_args)
        port_entry.grid(row=1, column=1, sticky=styling.sticky_ew, ipady=1)

    def config_form_buttons(self):
        button_frame = tkinter.Frame(self.main_frame, relief='flat', background='yellow')
        button_frame.grid(row=1, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.connect_button = ttk.Button(button_frame, text='Send')
        self.connect_button.grid(row=0, column=0, sticky=styling.sticky_ew)

        self.cancel_button = ttk.Button(button_frame, text='Cancel')
        self.cancel_button.grid(row=0, column=1, sticky=styling.sticky_ew)

    def set_default_vals(self, host='localhost', port=16661):
        self.host_entry_var.set(host)
        self.port_entry_var.set(port)
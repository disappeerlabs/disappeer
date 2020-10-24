"""
getpassphraseview.py

Module for GetPassphraseView popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling


class GetPassphraseView:
    """
    GUI view for get password popup window.
    Should only be loaded by GetPassController object.
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

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, **styling.new_key_elements_frame)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Form elements frame row
        self.main_frame.rowconfigure(0, weight=0)

        # Form buttons frame row
        self.main_frame.rowconfigure(1, weight=0)

    def config_form_elements(self):
        """
        Frame containing the form's entry field
        """
        # TODO: Add check button to show or hide the passphrase as it is typed
        elements_frame = tkinter.Frame(self.main_frame)
        elements_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

        elements_frame.rowconfigure(0, weight=0)
        elements_frame.columnconfigure(0, weight=1)

        self.passphrase_entry = tkinter.Entry(elements_frame,
                                              font=styling.font_big,
                                              insertbackground='white',
                                              background='grey10',
                                              foreground=styling.foreground_color,
                                              show='*'
                                              )
        self.passphrase_entry.grid(row=0, column=0, sticky=styling.sticky_ew)

    def config_form_buttons(self):
        """
        Button frame with two buttons: submit or cancel
        """
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background='yellow')
        button_frame.grid(row=1, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.submit_button = ttk.Button(button_frame, text='Submit')
        self.submit_button.grid(row=0, column=0, sticky=styling.sticky_ew)

        self.cancel_button = ttk.Button(button_frame, text='Cancel')
        self.cancel_button.grid(row=0, column=1, sticky=styling.sticky_ew)
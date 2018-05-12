"""
deletekeyview.py

View for the delete key popup.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling
from disappeer.constants import constants
import logging

log = logging.getLogger(constants.title)


class DeleteKeyView:
    """
    GUI view for new key form popup window.
    Should only be loaded by NewKeyController object.
    """

    def __init__(self, window, key_list):
        # Configure window
        self.window = window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=0)

        # Raw gpg key list, i.e. list of key dicts
        self.key_list = key_list

        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_form_elements()
        self.config_form_buttons()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window,
                                        background=styling.background_color,
                                        padx=20,
                                        pady=20)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Form elements frame row
        self.main_frame.rowconfigure(0, weight=0)

        # Form buttons frame row
        self.main_frame.rowconfigure(1, weight=0)

    def config_form_elements(self):
        """
        Frame containing the form's check button fields with corresponding text values.
        Each item is provided an int var, which is appended to the class list.
        """
        elements_frame = tkinter.Frame(self.main_frame, **styling.new_key_elements_frame)
        elements_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

        # column for labels
        elements_frame.columnconfigure(0, weight=0)

        # column for entries
        elements_frame.columnconfigure(1, weight=1)

        self.int_vars = []
        for idx, item in enumerate(self.key_list):
            v = tkinter.IntVar()
            text_label = item['uids'][0] + " " + item['keyid']

            check_button = tkinter.Checkbutton(elements_frame,
                                               text=text_label,
                                               variable=v,
                                               **styling.check_button_styling
                                               )
            check_button.grid(row=idx, column=0, sticky=('W'), pady=5)
            self.int_vars.append(v)

    def config_form_buttons(self):
        """
        Button frame with two buttons: delete key or cancel
        """
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background='yellow')
        button_frame.grid(row=1, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.delete_key_button = ttk.Button(button_frame, text='Delete')
        self.delete_key_button.grid(row=0, column=0, sticky=styling.sticky_ew)

        self.cancel_button = ttk.Button(button_frame, text='Cancel')
        self.cancel_button.grid(row=0, column=1, sticky=styling.sticky_ew)
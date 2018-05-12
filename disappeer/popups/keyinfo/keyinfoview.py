"""
keyinfoview.py

View for key info button popup.

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


class KeyInfoView:
    """
    View for Key Info popup window. Takes raw key_dict to populate forms.
    """

    def __init__(self, window, key_dict):
        self.key_dict = key_dict

        self.window = window
        # self.window.wm_geometry("550x550")

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_form_elements()
        self.config_form_buttons()

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

        for idx, item in enumerate(constants.key_info_ordered_field_labels):
            elements_frame.rowconfigure(idx, weight=0)

            label = tkinter.Label(elements_frame, text=item + ":", **styling.label_args)
            label.grid(row=idx, column=0, sticky='E', pady=3)

            dynamic_label = tkinter.Entry(elements_frame, width=66, **styling.entry_field_label_clone_copy_paste_args)
            dynamic_label.grid(row=idx, column=1, sticky=styling.sticky_ew, padx=(7, 0), pady=3)

            if item in ['date', 'expires']:
                stamp = helpers.get_date_time_stamp(self.key_dict[item])
                dynamic_label.insert(0, stamp)
            elif item == 'uids':
                dynamic_label.insert(0, self.key_dict[item][0])
            else:
                dynamic_label.insert(0, self.key_dict[item])
            dynamic_label.configure(state='readonly')


    def config_form_buttons(self):
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background='yellow')
        button_frame.grid(row=1, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)

        self.cancel_button = ttk.Button(button_frame, text='OK')
        self.cancel_button.grid(row=0, column=0, sticky=styling.sticky_ew)

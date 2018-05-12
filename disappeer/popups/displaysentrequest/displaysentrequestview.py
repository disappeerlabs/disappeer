"""
displaysentrequestview.py

View for DisplaySentRequest popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import constants
from disappeer.constants import styling
from disappeer.utilities import helpers
import logging


class DisplaySentRequestView:
    """
    View for DisplaySentRequest popup window. Takes raw key_dict and host address to populate forms.
    """

    def __init__(self, window, key_dict, address):
        self.key_dict = key_dict
        self.address = address

        self.window = window

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=0)

        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_key_elements()
        self.config_form_buttons()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, background=styling.background_color, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Key elements frame row
        self.main_frame.rowconfigure(0, weight=0)

        # Form buttons frame row
        self.main_frame.rowconfigure(1, weight=0)

    def config_key_elements(self):
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

        row_counter = 0

        for idx, item in enumerate(constants.key_info_ordered_field_labels):
            row_counter += 1

            label = tkinter.Label(elements_frame, text=item + ":", **styling.label_args)
            label.grid(row=idx, column=0, sticky='E', pady=3)

            dynamic_label = tkinter.Label(elements_frame, **styling.label_args)
            dynamic_label.grid(row=idx, column=1, sticky='W', padx=(7, 0), pady=3)

            if item in ['date', 'expires']:
                stamp = helpers.get_date_time_stamp(self.key_dict[item])
                dynamic_label.configure(text=stamp)
            elif item == 'uids':
                dynamic_label.configure(text=self.key_dict[item][0])
            else:
                dynamic_label.configure(text=self.key_dict[item])

        label = tkinter.Label(elements_frame, text="Address:", **styling.label_args)
        label.grid(row=row_counter+1, column=0, sticky='E', pady=3)

        dynamic_label = tkinter.Label(elements_frame, text=self.address, **styling.label_args)
        dynamic_label.grid(row=row_counter+1, column=1, sticky='W', padx=(7, 0), pady=3)

    def config_form_buttons(self):
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background='yellow')
        button_frame.grid(row=1, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)

        self.cancel_button = ttk.Button(button_frame, text='OK')
        self.cancel_button.grid(row=0, column=0, sticky=styling.sticky_ew)



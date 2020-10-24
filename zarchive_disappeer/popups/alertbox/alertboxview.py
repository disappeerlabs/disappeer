"""
alertboxview.py

View module for AlertBox popup window

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import constants
from disappeer.constants import styling
import logging

log = logging.getLogger(constants.title)


class AlertBoxView:
    """
    View for Key Info popup window. Takes raw key_dict to populate forms.
    """

    def __init__(self, window, message):
        self.message = message
        self.window = window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_form_elements()
        self.config_form_buttons()
        self.print_to_message_viewer(self.message)
        self.resize()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, background=styling.background_color, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Form elements frame row
        self.main_frame.rowconfigure(0, weight=1)

        # Form buttons frame row
        self.main_frame.rowconfigure(1, weight=0)

    def config_form_elements(self):
        """
        For each item in key info ordered fields list, create label and entry.
        Label is from ordered field list. Entry is corresponding val from self.key_dict.
        """
        elements_frame = tkinter.Frame(self.main_frame, **styling.alert_box_elements_frame)
        elements_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

        elements_frame.columnconfigure(0, weight=1)
        elements_frame.rowconfigure(0, weight=1)

        self.alert_text_box = tkinter.Text(elements_frame, **styling.alert_box_text_area_args)
        self.alert_text_box.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 5))

    def config_form_buttons(self):
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background='yellow')
        button_frame.grid(row=1, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)

        self.cancel_button = ttk.Button(button_frame, text='OK')
        self.cancel_button.grid(row=0, column=0, sticky=styling.sticky_ew)

    def print_to_message_viewer(self, msg):
        self.alert_text_box.delete('1.0', 'end')
        self.alert_text_box.insert('1.0', msg + "\n")

    def resize(self):
        num_lines = int(self.alert_text_box.index('end-1c').split('.')[0])
        if num_lines > 30:
            num_lines = 30
        self.alert_text_box.configure(height=num_lines)

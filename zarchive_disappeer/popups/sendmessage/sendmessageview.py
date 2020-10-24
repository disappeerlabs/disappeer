"""
sendmessageview.py

Module for the SendMessageView popup view

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import constants
from disappeer.constants import styling


class SendMessageView:
    """
    View for SendMessageController popup window.
    """

    def __init__(self, window, recipient_text, message_text):
        self.recipient_text = recipient_text
        self.message_text = message_text
        self.window = window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_info_frame()
        self.config_text_area()
        self.config_form_buttons()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, background=styling.background_color, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Recipient Info frame row
        self.main_frame.rowconfigure(0, weight=0)

        # Text Area frame row
        self.main_frame.rowconfigure(1, weight=1)

        # Button Area frame row
        self.main_frame.rowconfigure(2, weight=0)

    def config_info_frame(self):
        info_frame = tkinter.Frame(self.main_frame, background=styling.background_color)
        info_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

        # Only one row
        info_frame.rowconfigure(0, weight=0)

        # column for labels
        info_frame.columnconfigure(0, weight=0)

        # column for entries
        info_frame.columnconfigure(1, weight=1)

        send_to_label = tkinter.Label(info_frame, text="Send to:", **styling.label_args)
        send_to_label.grid(row=0, column=0, sticky='E', padx=(0, 5), pady=(5, 5))

        recip_info_label = tkinter.Label(info_frame, text=self.recipient_text, **styling.label_args)
        recip_info_label.grid(row=0, column=1, sticky='W', padx=(0, 0), pady=(5, 5))

    def config_text_area(self):
        self.text_box = tkinter.Text(self.main_frame, **styling.debug_text_area)
        self.text_box.grid(row=1, column=0, sticky=styling.sticky_all)
        self.print_msg(self.message_text)

    def config_form_buttons(self):
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background='yellow')
        button_frame.grid(row=2, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.cancel_button = ttk.Button(button_frame, text='Cancel')
        self.cancel_button.grid(row=0, column=0, sticky=styling.sticky_ew)

        self.send_button = ttk.Button(button_frame, text='Send Message')
        self.send_button.grid(row=0, column=1, sticky=styling.sticky_ew)

    def print_msg(self, msg):
        """
        Clear debug text box and insert msg.
        """
        self.text_box.delete('1.0', 'end')
        self.text_box.insert('1.0', msg + "\n")

    def get_text_area(self):
        """
        :return: all current contents of text area
        """
        result = self.text_box.get('1.0', 'end')
        return result

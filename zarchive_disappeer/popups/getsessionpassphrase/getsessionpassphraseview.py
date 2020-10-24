"""
getsessionpassphraseview.py

Popup view module for the GetSessionPassphraseView

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling


class GetSessionPassphraseView:
    """
    GUI view for get password popup window.
    Should only be loaded by GetSessionPassController object.
    """

    def __init__(self, window):
        self.window = window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_label_elements()
        self.config_entry_elements()
        self.config_form_buttons()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, **styling.new_key_elements_frame)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Textbox message frame row
        self.main_frame.rowconfigure(0, weight=0)

        # Entry frame row
        self.main_frame.rowconfigure(1, weight=0)

        # Form buttons frame row
        self.main_frame.rowconfigure(2, weight=0)

    def config_label_elements(self):
        """
        Frame containing the message box
        """
        message_frame = tkinter.Frame(self.main_frame, **styling.alert_box_elements_frame)
        message_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 0))

        message_frame.columnconfigure(0, weight=1)
        message_frame.rowconfigure(0, weight=1)

        self.message_text_box = tkinter.Text(message_frame, **styling.alert_box_text_area_args)
        self.message_text_box.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 5))

        msg = "A session passphrase is necessary for automatic signing and decryption of messages with your host key.\n"
        self.print_to_message_viewer(msg)
        self.resize()
        self.message_text_box.configure(state=tkinter.DISABLED)

    def print_to_message_viewer(self, msg):
        self.message_text_box.delete('1.0', 'end')
        self.message_text_box.insert('1.0', msg + "\n")

    def resize(self):
        num_lines = int(self.message_text_box.index('end-1c').split('.')[0])
        if num_lines > 30:
            num_lines = 30
        self.message_text_box.configure(height=num_lines)

    def config_entry_elements(self):
        """
        Frame containing the form's entry field
        """
        # TODO: Add check button to show or hide the passphrase as it is typed
        elements_frame = tkinter.Frame(self.main_frame)
        elements_frame.grid(row=1, column=0, sticky=styling.sticky_all, pady=(20, 20))

        elements_frame.rowconfigure(0, weight=0)
        elements_frame.columnconfigure(0, weight=1)

        self.passphrase_entry = tkinter.Entry(elements_frame, show='*', **styling.entry_field_args)
        self.passphrase_entry.grid(row=0, column=0, sticky=styling.sticky_ew)

    def config_form_buttons(self):
        """
        Button frame with two buttons: submit or cancel
        """
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background='yellow')
        button_frame.grid(row=2, column=0, sticky=styling.sticky_ew)

        button_frame.rowconfigure(0, weight=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.submit_button = ttk.Button(button_frame, text='Submit')
        self.submit_button.grid(row=0, column=0, sticky=styling.sticky_ew)

        self.cancel_button = ttk.Button(button_frame, text='Cancel')
        self.cancel_button.grid(row=0, column=1, sticky=styling.sticky_ew)


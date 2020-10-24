"""
displaymessageview.py

Module for the view for the DisplayMessage popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling


class DisplayMessageView:

    def __init__(self, window, argnamespace):
        self.window = window
        self.argnamespace = argnamespace
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_infobox_frame()
        self.config_messagebox_frame()
        self.config_button_frame()
        self.resize()

    def config_main_frame(self):
        """
        Main frame, config rows and cols
        """
        self.main_frame = tkinter.Frame(self.window, background=styling.background_color, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=0)

    def config_infobox_frame(self):
        infobox_frame = tkinter.Frame(self.main_frame, **styling.display_message_infobox_frame)
        infobox_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

        # column for labels
        infobox_frame.columnconfigure(0, weight=0)

        # column for entries
        infobox_frame.columnconfigure(1, weight=1)

        # Message type
        infobox_frame.rowconfigure(0, weight=0)

        type_label = tkinter.Label(infobox_frame, text="Type:", **styling.label_args_small_font)
        type_label.grid(row=0, column=0, sticky='E', pady=0)

        type_entry = tkinter.Entry(infobox_frame, **styling.entry_field_label_clone_copy_paste_args_font_small)
        type_entry.grid(row=0, column=1, sticky=styling.sticky_ew, padx=(3, 0))
        type_entry.insert(0, self.argnamespace.message_type)
        type_entry.configure(state='readonly')

        # Message TO
        infobox_frame.rowconfigure(1, weight=0)

        to_label = tkinter.Label(infobox_frame, text="To:", **styling.label_args_small_font)
        to_label.grid(row=1, column=0, sticky='E', pady=0)

        to_entry = tkinter.Entry(infobox_frame, **styling.entry_field_label_clone_copy_paste_args_font_small)
        to_entry.grid(row=1, column=1, sticky=styling.sticky_ew, padx=(3, 0))
        to_entry.insert(0, self.argnamespace.message_to)
        to_entry.configure(state='readonly')

        # Message FROM
        infobox_frame.rowconfigure(2, weight=0)

        from_label = tkinter.Label(infobox_frame, text="From:", **styling.label_args_small_font)
        from_label.grid(row=2, column=0, sticky='E', pady=0)

        from_entry = tkinter.Entry(infobox_frame, **styling.entry_field_label_clone_copy_paste_args_font_small)
        from_entry.grid(row=2, column=1, sticky=styling.sticky_ew, padx=(3, 0))
        from_entry.insert(0, self.argnamespace.message_from)
        from_entry.configure(state='readonly')

    def config_messagebox_frame(self):
        textbox_frame = tkinter.Frame(self.main_frame, **styling.display_message_infobox_frame)
        textbox_frame.grid(row=1, column=0, sticky=styling.sticky_all, pady=(0, 10))

        textbox_frame.rowconfigure(0, weight=1)
        textbox_frame.columnconfigure(0, weight=1)

        self.text_box = tkinter.Text(textbox_frame, **styling.display_message_text_area_args)
        self.text_box.grid(row=0, column=0, sticky=styling.sticky_all)
        self.print_msg(self.argnamespace.message_text)

    def config_button_frame(self):
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background=styling.background_color)
        button_frame.grid(row=2, column=0, sticky=styling.sticky_all)

        button_frame.rowconfigure(0, weight=0)
        button_frame.rowconfigure(1, weight=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.cancel_button = ttk.Button(button_frame, text='Close')
        self.cancel_button.grid(row=0, column=0, columnspan=2, sticky=styling.sticky_ew, padx=(0, 0), pady=(5, 0))

        self.delete_button = ttk.Button(button_frame, text='Delete')
        self.delete_button.grid(row=1, column=0, sticky=styling.sticky_ew, padx=(0, 5), pady=(5, 5))

        self.inspect_button = ttk.Button(button_frame, text='Inspect')
        self.inspect_button.grid(row=1, column=1, sticky=styling.sticky_ew, padx=(0, 0), pady=(5, 5))

    def print_msg(self, msg):
        """
        Clear debug text box and insert msg.
        """
        self.text_box.delete('1.0', 'end')
        self.text_box.insert('1.0', msg + "\n")

    def resize(self):
        num_lines = int(self.text_box.index('end-1c').split('.')[0])
        if num_lines > 30:
            num_lines = 30
        # TODO: if message has small number of new lines, but those lines are long, IT WILL NOT RESIZE
        #    - must do resize depending on length of message too
        self.text_box.configure(height=num_lines)
        self.text_box.configure(state=tkinter.DISABLED)

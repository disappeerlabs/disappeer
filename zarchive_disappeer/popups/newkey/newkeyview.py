"""
newkeyview.py

View for the new key popup.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling
from disappeer.constants import constants
from disappeer.utilities import helpers


class NewKeyView:
    """
    GUI view for new key form popup window.
    Should only be loaded by NewKeyController object.
    """

    def __init__(self, window):
        self.string_vars = []
        self.window = window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.setup()

    def setup(self):
        styling.config_ttk_styling()
        self.config_main_frame()
        self.config_image()
        self.config_form_elements()
        self.config_form_buttons()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, **styling.new_key_elements_frame)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)

        # Image row
        self.main_frame.rowconfigure(0, weight=0)

        # Form elements frame row
        self.main_frame.rowconfigure(1, weight=0)

        # Form buttons frame row
        self.main_frame.rowconfigure(2, weight=0)

    def config_image(self):
        if constants.display_images:
            image_path = helpers.get_images_dir_path()
            key_path = image_path + "crypto_key.png"
            image = tkinter.PhotoImage(file=key_path)
            label = tkinter.Label(self.main_frame, image=image, background=styling.background_color)
            label.photo = image
            label.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

    def config_form_elements(self):
        """
        Frame containing the form's entry fields with corresponding labels and entry values.
        Each entry is provided a string var, which is appended to the class list.
        """
        elements_frame = tkinter.Frame(self.main_frame, background=styling.background_color)
        elements_frame.grid(row=1, column=0, sticky=styling.sticky_all, pady=(0, 10))

        # column for labels
        elements_frame.columnconfigure(0, weight=0)

        # column for entries
        elements_frame.columnconfigure(1, weight=1)

        for idx, item in enumerate(constants.new_key_ordered_field_labels):
            label = tkinter.Label(elements_frame, text=item + ":", **styling.label_args)
            label.grid(row=idx, column=0, sticky='E', padx=(0, 5), pady=(5, 5))

            v = tkinter.StringVar()
            entry = tkinter.Entry(elements_frame, textvariable=v, **styling.entry_field_args)
            entry.grid(row=idx, column=1, sticky=styling.sticky_ew, ipady=1)
            entry.insert("0", constants.new_key_default_vals_dict[item])
            self.string_vars.append(v)

    def reset_entry_vals(self):
        """
        Iterate over ordered field labels. Set corresponding entry string var to current constant val.
        """
        for idx, item in enumerate(constants.new_key_ordered_field_labels):
            self.string_vars[idx].set(constants.new_key_default_vals_dict[item])

    def config_form_buttons(self):
        """
        Button frame with three buttons: create new key, cancel, reset
        """
        button_frame = tkinter.Frame(self.main_frame, relief='raised', background=styling.background_color)
        button_frame.grid(row=2, column=0, sticky=styling.sticky_ew)
        button_frame.rowconfigure(0, weight=0)
        button_frame.rowconfigure(1, weight=0)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.create_new_key_button = ttk.Button(button_frame, text='Create')
        self.create_new_key_button.grid(row=0, column=0, sticky=styling.sticky_ew, padx=(0, 5), pady=(5, 5))

        self.cancel_button = ttk.Button(button_frame, text='Cancel')
        self.cancel_button.grid(row=0, column=1, sticky=styling.sticky_ew, padx=(0, 0), pady=(5, 5))

        self.reset_button = ttk.Button(button_frame, text='Reset')
        self.reset_button.grid(row=1, columnspan=2, sticky=styling.sticky_ew, padx=(0, 0), pady=(5, 0))


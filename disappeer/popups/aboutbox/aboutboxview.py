"""
aboutboxview.py

View module for AboutBox popup window

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import constants
from disappeer.constants import styling
import logging
from disappeer import metainfo
from disappeer.utilities import helpers

log = logging.getLogger(constants.title)


class AboutBoxView:
    """
    AboutBox popup view
    """

    def __init__(self, window):
        self.window = window
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.geometry('500x300')
        self.window.minsize(width=500, height=300)
        self.window.maxsize(width=500, height=300)
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_form_elements()

    def config_main_frame(self):
        """
        Main frame, two rows, one column.
        """
        self.main_frame = tkinter.Frame(self.window, background=styling.background_color, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def config_form_elements(self):
        """
        For each item in key info ordered fields list, create label and entry.
        Label is from ordered field list. Entry is corresponding val from self.key_dict.
        """
        elements_frame = tkinter.Frame(self.main_frame, **styling.alert_box_elements_frame)
        elements_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))

        elements_frame.columnconfigure(0, weight=1)
        elements_frame.rowconfigure(0, weight=1)
        elements_frame.rowconfigure(1, weight=1)
        elements_frame.rowconfigure(2, weight=1)
        elements_frame.rowconfigure(3, weight=1)
        elements_frame.rowconfigure(4, weight=1)

        if constants.display_images:
            image_path = helpers.get_images_dir_path()
            logo_path = image_path + "logo_64x64.gif"
            image = tkinter.PhotoImage(file=logo_path)
            label = tkinter.Label(elements_frame, image=image, background=styling.background_color)
            label.photo = image
            label.grid(row=0, column=0, sticky=styling.sticky_all)

        name = tkinter.Label(elements_frame, text=metainfo.title + " " + metainfo.version, **styling.label_args)
        name.grid(row=1, column=0, sticky=styling.sticky_all,  ipady=1)

        gpl = tkinter.Label(elements_frame, text="License: " + metainfo.license, **styling.label_args)
        gpl.grid(row=2, column=0, sticky=styling.sticky_all,  ipady=1)

        github = tkinter.Label(elements_frame, text="Source: " + metainfo.github, **styling.label_args)
        github.grid(row=3, column=0, sticky=styling.sticky_all, ipady=1)

        email = tkinter.Label(elements_frame, text="Contact: " + metainfo.email, **styling.label_args)
        email.grid(row=4, column=0, sticky=styling.sticky_all, ipady=1)


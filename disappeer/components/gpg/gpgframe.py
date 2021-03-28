"""
gpgframe.py

View module for GPG Widget

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import tkinter
from dptools.static import styling


class GPGFrame(tkinter.Frame):

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, background=styling.background_color, padx=10, pady=15)
        self.parent = parent
        self.home_dir_entry = None
        self.home_dir_entry_var = None
        self.setup()

    def setup(self):
        self.columnconfigure(0, weight=1)
        self.config_home_dir_frame()

    def config_home_dir_frame(self):
        # Row for Home Key Dir LabelFrame
        self.rowconfigure(0, weight=0)

        home_dir_frame = tkinter.LabelFrame(self, text="Home Directory", **styling.label_frame_args)
        home_dir_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 20))
        home_dir_frame.rowconfigure(0, weight=0)
        home_dir_frame.rowconfigure(1, weight=0)
        home_dir_frame.rowconfigure(2, weight=0)

        home_dir_frame.columnconfigure(0, weight=0)
        home_dir_frame.columnconfigure(1, weight=1)

        # Home dir label
        home_dir_label = tkinter.Label(home_dir_frame, text='Home:', **styling.label_args)
        home_dir_label.grid(row=0, column=0, sticky='E', padx=(0, 5))

        # Home dir entry
        self.home_dir_entry_var = tkinter.StringVar()
        self.home_dir_entry_var.set("Default Text Input")
        self.home_dir_entry = tkinter.Entry(home_dir_frame,
                                            textvariable=self.home_dir_entry_var,
                                            state='readonly',
                                            **styling.entry_field_readonly_args)
        self.home_dir_entry.grid(row=0, column=1, sticky=styling.sticky_ew, ipady=1)

    def bind_home_dir_entry(self, command, function):
        self.home_dir_entry.bind(command, function)

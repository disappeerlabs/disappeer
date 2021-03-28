"""
gpgcontroller.py

Controller module for the GPG widget

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import tkinter 
from tkinter import filedialog


class GPGController:
    button_release_1 = '<ButtonRelease-1>'

    
    def __init__(self, root, view, model):
        self.root = root
        self.view = view
        self.model = model
        self.config_data_context()
        self.config_event_bindings()

    def config_data_context(self):
        self.model.add_home_dir_observer(self.view.home_dir_entry_var)

    def config_event_bindings(self):
        self.view.bind_home_dir_entry(self.button_release_1, self.home_dir_entry_clicked)

    def home_dir_entry_clicked(self, event):
        result = filedialog.askdirectory(initialdir=self.model.get_home_dir_observable())
        if result == ():
            return 

        self.model.set_home_dir_observable(result)



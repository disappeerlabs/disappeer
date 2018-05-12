"""
basepopupcontroller.py

Module for BasePopupController, abstract base for all popup controller classes.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import abc


class BasePopupController(abc.ABC):

    def __init__(self, root):
        self.root = root
        self.window = tkinter.Toplevel(self.root)
        self.window.title(self.title)
        self.output = None

    def show(self):
        self.window.transient(self.root)
        self.window.grab_set()
        self.window.deiconify()
        self.window.wait_window()
        return self.output

    def cancel_button_clicked(self, event):
        self.window.destroy()

    def set_output_and_close(self, output):
        self.output = output
        self.window.destroy()

    @abc.abstractmethod
    def config_event_bindings(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def title(self):
        return 'Default Base Title'


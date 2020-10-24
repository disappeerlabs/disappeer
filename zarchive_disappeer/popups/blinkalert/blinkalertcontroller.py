"""
blinkalertcontroller.py

Module for BlinkAlertController popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.blinkalert import blinkalertview
import tkinter


class BlinkAlertController(basepopupcontroller.BasePopupController):

    def __init__(self, root, message):
        super().__init__(root)
        self.message = message
        self.set_window_attributes()
        self.window.geometry('250x100-0+0')
        self.view = blinkalertview.BlinkAlertView(self.window, self.message)
        self.blink_count = 0

    @property
    def title(self):
        return 'Alert!'

    def set_window_attributes(self):
        self.window.attributes()
        self.window.attributes("-alpha", 0.0)

    def config_event_bindings(self):
        pass

    def show(self):
        self.fade_in()

    def fade_in(self):
        if self.blink_count >= 3:
            self.cancel_button_clicked(None)
            return None

        try:
            alpha = self.window.attributes("-alpha")
        except tkinter.TclError as err:
            return None

        if alpha < 1:
            alpha += .03
            self.window.attributes("-alpha", alpha)
            self.root.after(50, self.fade_in)
        else:
            self.blink_count += 1
            self.root.after(2000, self.fade_away)

    def fade_away(self):
        try:
            alpha = self.window.attributes("-alpha")
        except tkinter.TclError as err:
            return None

        if alpha > 0:
            alpha -= .1
            self.window.attributes("-alpha", alpha)
            self.root.after(50, self.fade_away)
        else:
            self.fade_in()
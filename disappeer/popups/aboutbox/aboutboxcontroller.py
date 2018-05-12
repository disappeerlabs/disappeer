"""
aboutboxcontroller.py

Module for the AboutBoxController popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.aboutbox import aboutboxview


class AboutBoxController(basepopupcontroller.BasePopupController):

    def __init__(self, root):
        super().__init__(root)
        self.view = aboutboxview.AboutBoxView(self.window)
        self.config_event_bindings()

    @property
    def title(self):
        return 'About'

    def config_event_bindings(self):
        pass


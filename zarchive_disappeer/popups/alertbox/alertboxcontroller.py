"""
alertboxcontroller.py

Module for AlertBoxController popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.alertbox import alertboxview
from disappeer.popups.bases import basepopupcontroller


class AlertBoxController(basepopupcontroller.BasePopupController):

    def __init__(self, root, message):
        super().__init__(root)
        self.message = message
        self.view = alertboxview.AlertBoxView(self.window, self.message)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Alert!'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)

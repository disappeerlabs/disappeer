"""
displaymessagecontroller.py

Module for DisplayMessageController popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.displaymessage import displaymessageview


class DisplayMessageController(basepopupcontroller.BasePopupController):

    def __init__(self, root, argnamespace):
        """

        :param root:
        :param argnamespace: must contain: .message_type, .message_to, .message_from, .message_text
        """
        super().__init__(root)
        self.argnamespace = argnamespace
        self.view = displaymessageview.DisplayMessageView(self.window, self.argnamespace)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Message'

    def config_event_bindings(self):
        command_button_release_1 = "<ButtonRelease-1>"
        self.view.cancel_button.bind(command_button_release_1, self.cancel_button_clicked)
        self.view.delete_button.bind(command_button_release_1, self.delete_button_clicked)
        self.view.inspect_button.bind(command_button_release_1, self.inspect_button_clicked)

    def delete_button_clicked(self, event):
        self.set_output_and_close('delete')

    def inspect_button_clicked(self, event):
        self.set_output_and_close('inspect')

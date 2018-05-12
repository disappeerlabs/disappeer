"""
sendmessagecontroller.py

Module for the SendMessageController popup class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.sendmessage import sendmessageview
from disappeer.popups.bases import basepopupcontroller


class SendMessageController(basepopupcontroller.BasePopupController):

    def __init__(self, root, recipient_data_record, console_text):
        super().__init__(root)
        self.recipient_data_record = recipient_data_record
        self.console_text = console_text
        self.view = sendmessageview.SendMessageView(self.window,
                                                    self.recipient_data_record.gpg_uid,
                                                    self.console_text)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Send Message'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.send_button.bind("<ButtonRelease-1>", self.send_button_clicked)

    def send_button_clicked(self, event):
        message = self.view.get_text_area()
        self.set_output_and_close(message)


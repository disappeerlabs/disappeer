"""
contactrequestcontroller.py

Module for ContactRequestController class object, for contact request popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.contactrequest import contactrequestview
from disappeer.net.contact import contactrequestvalidator


class ContactRequestController(basepopupcontroller.BasePopupController):

    def __init__(self, root, request_record):
        super().__init__(root)
        self.request_record = request_record
        self.data_dict = self.construct_contact_req_dict(self.request_record)
        self.validator = contactrequestvalidator.ContactRequestValidator(self.data_dict)
        if self.validator.valid:
            self.view = contactrequestview.ContactRequestView(self.window, self.validator.key_dict)
            self.config_event_bindings()
        else:
            self.handle_invalid_request()

    @property
    def title(self):
        return 'New Contact Request'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.accept_button.bind("<ButtonRelease-1>", self.accept_button_clicked)
        self.view.reject_button.bind("<ButtonRelease-1>", self.reject_button_clicked)

    def construct_contact_req_dict(self, request_record):
        result = dict(sig=request_record.sig, data=request_record.data)
        return result

    def handle_invalid_request(self):
        self.set_output_and_close('invalid')

    def accept_button_clicked(self, event):
        self.set_output_and_close('accept')

    def reject_button_clicked(self, event):
        self.set_output_and_close('reject')

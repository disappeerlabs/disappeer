"""
newkeycontroller.py

Contains NewKeyController, controller class for new key popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.newkey import newkeyview
from disappeer.constants import constants


class NewKeyController(basepopupcontroller.BasePopupController):

    def __init__(self, root):
        super().__init__(root)
        self.view = newkeyview.NewKeyView(self.window)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Create New Key'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.reset_button.bind("<ButtonRelease-1>", self.reset_button_clicked)
        self.view.create_new_key_button.bind("<ButtonRelease-1>", self.create_new_key_button_clicked)

    def reset_button_clicked(self, event):
        self.view.reset_entry_vals()

    def create_new_key_button_clicked(self, event):
        vals = self.get_view_string_var_vals()
        zipped_dict = self.zip_key_dict(vals)
        final = self.prepare_output_dict(zipped_dict)
        self.set_output_and_close(final)
        return final

    def get_view_string_var_vals(self):
        vals = [x.get() for x in self.view.string_vars]
        return vals

    def zip_key_dict(self, vals):
        form_field_vals_dict = dict(zip(constants.new_key_ordered_field_labels, vals))
        return form_field_vals_dict

    def prepare_output_dict(self, zipped_key_dict):
        output_dict = {}
        for item in constants.new_key_ordered_field_labels:
            key = constants.new_key_input_dict[item]
            val = zipped_key_dict[item]
            output_dict[key] = val
        return output_dict
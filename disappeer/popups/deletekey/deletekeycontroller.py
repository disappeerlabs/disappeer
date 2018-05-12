"""
deletekeycontroller.py

Module for popup DeleteKeyController class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.deletekey import deletekeyview
from disappeer.popups.bases import basepopupcontroller


class DeleteKeyController(basepopupcontroller.BasePopupController):

    def __init__(self, root, key_list):
        super().__init__(root)
        self.key_list = key_list
        self.view = deletekeyview.DeleteKeyView(self.window, self.key_list)
        self.config_event_bindings()

    @property
    def title(self):
        return 'Delete Keys'

    def config_event_bindings(self):
        self.view.cancel_button.bind("<ButtonRelease-1>", self.cancel_button_clicked)
        self.view.delete_key_button.bind("<ButtonRelease-1>", self.delete_button_clicked)

    def delete_button_clicked(self, event):
        packed_val_tuple_list = self.read_check_button_vals_and_pack_list()
        targets = self.build_deletion_targets_list(packed_val_tuple_list)
        if len(targets) > 0:
            self.set_output_and_close(targets)

    def read_check_button_vals_and_pack_list(self):
        result_list = []
        for idx, item in enumerate(self.key_list):
            uid = item['uids']
            fingerprint = item['fingerprint']
            val = self.view.int_vars[idx].get()
            pack = (val, fingerprint, uid)
            result_list.append(pack)
        return result_list

    def build_deletion_targets_list(self, packed_val_tuple_list):
        targets = []
        for item in packed_val_tuple_list:
            if item[0]:
                targets.append(item[1])
        return targets

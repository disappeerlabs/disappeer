"""
consolecontroller.py

Module for the ConsoleController class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter.filedialog
from disappeer.gpg.agents import gpgclient
from disappeer.popups import popuplauncher
import functools


class ConsoleController:

    func_list = ['Encrypt', 'Decrypt', 'Import', 'Export', 'Sign', 'Verify']

    def __init__(self, root_params, gpg_data_context):
        self.root_params = root_params
        self.root = self.root_params.root
        self.view = self.root_params.get_console_frame()
        self.root_queue = self.root_params.root_queue
        self.gpg_data_context = gpg_data_context
        self.gpg_client = gpgclient.GPGClient(self.gpg_data_context.get_home_dir())
        self.config_data_context()
        self.config_event_bindings()
        self.config_menubar()
        self.running_job = False

    def config_menubar(self):
        file_menu = self.root_params.get_file_menu_obj()
        file_menu.add_command(label='Open', command=functools.partial(self.open_button_clicked, None))
        file_menu.add_command(label='Save', command=functools.partial(self.save_button_clicked, None))

    def config_data_context(self):
        self.gpg_data_context.add_key_list_observer(self.view.key_info_dropdown_handler)
        self.gpg_data_context.add_home_dir_observer(self.gpg_client)
        self.view.console_function_dropdown_handler.set(self.func_list)

    def config_event_bindings(self):
        self.view.save_button.bind("<ButtonRelease-1>", self.save_button_clicked)
        self.view.open_button.bind("<ButtonRelease-1>", self.open_button_clicked)
        self.view.clear_button.bind("<ButtonRelease-1>", self.clear_button_clicked)
        self.view.run_button.bind("<ButtonRelease-1>", self.run_button_clicked)

    def run_button_clicked(self, event):
        selected_function = self.get_selected_function()
        if self.running_job:
            msg = 'Job already running. Please wait.'
            popuplauncher.launch_alert_box_popup(self.root, msg)
        elif selected_function not in self.func_list:
            msg = 'You must select a function from the dropdown menu.'
            popuplauncher.launch_alert_box_popup(self.root, msg)
        elif selected_function == 'Encrypt':
            self.run_encrypt()
        elif selected_function == 'Decrypt':
            self.run_decrypt()
        elif selected_function == 'Export':
            self.run_export()
        elif selected_function == 'Import':
            self.run_import()
        elif selected_function == 'Sign':
            self.run_sign()
        elif selected_function == 'Verify':
            self.run_verify()

    def run_verify(self):
        message = self.get_console_text()
        result = self.gpg_client.verify(message)
        if result.valid:
            msg = "Success! Signature is valid.\nUser: {}\nFingerprint: {}\n\n".format(result.username, result.fingerprint)
        else:
            msg = result.stderr
        popuplauncher.launch_alert_box_popup(self.root, msg)

    def run_sign(self):
        selected_key_id = self.get_selected_key()
        if selected_key_id is None:
            return None
        passphrase = popuplauncher.launch_get_passphrase_popup(self.root)
        if passphrase is None:
            msg = 'Sign cancelled.'
            popuplauncher.launch_alert_box_popup(self.root, msg)
            return None
        text = self.get_console_text()
        result = self.gpg_client.sign(text, selected_key_id, passphrase)
        if result.fingerprint is None:
            popuplauncher.launch_alert_box_popup(self.root, result.stderr)
        else:
            self.print_to_console(result)

    def run_import(self):
        pub_key = self.get_console_text()
        result = self.gpg_client.import_key(pub_key)
        if result.imported == 0:
            popuplauncher.launch_alert_box_popup(self.root, result.stderr)
        else:
            msg = "Success! Key imported.\n\n"
            msg += result.stderr
            popuplauncher.launch_alert_box_popup(self.root, msg)
            self.gpg_data_context.set_key_list()

    def run_export(self):
        selected_key_id = self.get_selected_key()
        if selected_key_id is None:
            return None
        result = self.gpg_client.export_key(selected_key_id)
        if result == '':
            msg = 'Export error with key: {}'.format(selected_key_id)
            popuplauncher.launch_alert_box_popup(self.root, msg)
            return None
        else:
            self.print_to_console(result)

    def run_decrypt(self):
        passphrase = popuplauncher.launch_get_passphrase_popup(self.root)
        if passphrase is None:
            msg = 'Decrypt cancelled.'
            popuplauncher.launch_alert_box_popup(self.root, msg)
            return None
        ciphertext = self.get_console_text()
        result = self.gpg_client.decrypt(ciphertext, passphrase)
        if result.ok:
            self.print_to_console(result)
        else:
            popuplauncher.launch_alert_box_popup(self.root, result.stderr)

    def run_encrypt(self):
        selected_key_id = self.get_selected_key()
        if selected_key_id is None:
            return None
        plaintext = self.get_console_text()
        result = self.gpg_client.encrypt(plaintext, selected_key_id)
        if result is None:
            msg = 'Error: no such key in keyring.'
            popuplauncher.launch_alert_box_popup(self.root, msg)
        elif result.ok:
            self.print_to_console(result)
        else:
            popuplauncher.launch_alert_box_popup(self.root, result.stderr)

    def get_console_text(self):
        return self.view.get_console_text()

    def get_selected_key(self):
        result = self.view.console_key_option_var.get()
        target_keyid = result.split()[-1]
        if target_keyid == 'Keys':
            msg = 'Must select key from dropdown menu.'
            popuplauncher.launch_alert_box_popup(self.root, msg)
            return None
        else:
            return target_keyid

    def get_selected_function(self):
        return self.view.console_function_option_var.get()

    def print_to_console(self, msg):
        self.view.print_to_console_text_box(msg)

    def clear_button_clicked(self, event):
        self.view.clear_console_text_box()

    def open_button_clicked(self, event):
        file = tkinter.filedialog.askopenfile(mode='r', title='Open File')
        if file is None:
            return
        text = file.read()
        file.close()
        self.view.print_to_console_text_box(text)

    def save_button_clicked(self, event):
        console_text = self.view.get_console_text()
        file_path = tkinter.filedialog.asksaveasfile(mode='w', title='Save File')
        if file_path is None:
            return
        # UNTESTED
        file_path.write(console_text)
        file_path.close()

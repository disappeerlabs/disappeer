"""
gpgcontroller.py

Main controller for gpg frame and related methods

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import logging
import tkinter.filedialog
from disappeer.constants import constants
from disappeer.gpg.agents import keycreator
from disappeer.gpg.agents import keydeleter
from disappeer.popups import popuplauncher
from disappeer.gpg.helpers import keyfinder
from disappeer.utilities import queueconsumer
from disappeer.gpg.helpers import passphrasevalidator
import functools

log = logging.getLogger(constants.title)


class GPGController(queueconsumer.QueueConsumer):

    command_list = constants.command_list

    def __init__(self, root_params, data_context):
        super().__init__(root_params.root)
        self.root_params = root_params
        self.view = self.root_params.get_gpg_frame()
        self.root_queue = self.root_params.root_queue
        self.gpg_data_context = data_context
        self.config_data_context()
        self.config_event_bindings()
        self.config_menubar()
        self.creating_new_key = False

    def config_data_context(self):
        self.gpg_data_context.add_home_dir_observer(self.view.home_dir_entry_var)
        self.gpg_data_context.add_key_list_observer(self.view.key_info_dropdown_handler)
        self.gpg_data_context.add_host_key_observer(self.view.host_key_entry_var)
        self.root_params.set_session_passphrase_observable(None)

    def config_menubar(self):
        gpg_menu = self.root_params.get_gpg_menu_obj()
        gpg_menu.add_command(label='Create New Key', command=functools.partial(self.new_key_button_clicked, None))
        gpg_menu.add_command(label='Delete Key', command=functools.partial(self.delete_key_button_clicked, None))
        gpg_menu.add_command(label='Change Host', command=functools.partial(self.homedir_entry_clicked, None))

    def handle_queue_payload(self, payload):
        desc = payload['desc']
        if desc == self.command_list.Create_New_Key:
            self.handle_create_new_key_result(payload)

    def config_event_bindings(self):
        command = '<ButtonRelease-1>'
        self.view.home_dir_entry.bind(command, self.homedir_entry_clicked)
        self.view.key_info_button.bind(command, self.key_info_button_clicked)
        self.view.new_key_button.bind(command, self.new_key_button_clicked)
        self.view.delete_key_button.bind(command, self.delete_key_button_clicked)
        self.view.set_passphrase_button.bind(command, self.set_passphrase_button_clicked)

    def set_passphrase_button_clicked(self, event):
        self.start_set_passphrase_routine()

    def homedir_entry_clicked(self, event):
        if self.is_tor_proxy_running():
            return False

        result = tkinter.filedialog.askdirectory()
        if result == "" or result == ():
            return None
        else:
            self.gpg_data_context.set_home_dir(result)
            self.start_set_passphrase_routine()

    def start_set_passphrase_routine(self):
        # Set passphrase to none
        self.root_params.set_session_passphrase_observable(None)
        # If we have a private key
        if self.home_dir_has_private_key():
            # Get the session passphrase
            self.launch_get_session_passphrase()
        else:
            msg = "Your home dir has no secret key. You must create a host key."
            self.launch_alert_log(msg)
            self.new_key_button_clicked(None)

    def launch_get_session_passphrase(self):
        result = popuplauncher.launch_get_session_passphrase_popup(self.root)
        if result is None:
            self.root_params.set_session_passphrase_observable(None)
            return None
        else:
            self.verify_session_passphrase(result)

    def verify_session_passphrase(self, passphrase_val):
        validator = passphrasevalidator.PassphraseValidator(self.gpg_data_context.get_home_dir(),
                                                            self.gpg_data_context.get_host_key_id(),
                                                            passphrase_val)
        result = validator.validate()
        if result is True:
            self.root_params.set_session_passphrase_observable(passphrase_val)
        else:
            self.launch_alert_log(validator.result.stderr)
            self.launch_get_session_passphrase()

    def home_dir_has_private_key(self):
        no_key_msg = "No Private Key in Ring"
        host_key_val = self.gpg_data_context.get_host_key_id()
        if host_key_val == no_key_msg:
            return False
        else:
            return True

    def is_tor_proxy_running(self):
        status = self.root_params.get_tor_proxy_running_observable()
        if status:
            msg = 'Tor proxies are currently running. You must shut down tor proxies before changing host key.'
            self.launch_alert_log(msg)
            return True
        else:
            return False

    def key_info_button_clicked(self, event):
        target_widget = self.view.key_info_option_var
        keyid = self.get_keyid_from_view_option_var_widget(target_widget)

        result = keyfinder.KeyFinder(self.gpg_data_context.key_ring).find(keyid)
        if result is None:
            self.print_notification("No key selected.")
            return None
        else:
            key = popuplauncher.launch_key_info_popup(self.root, result)
            return key

    def get_keyid_from_view_option_var_widget(self, widget):
        view_string = widget.get()
        key_id = view_string.split()[-1]
        return key_id

    def new_key_button_clicked(self, event):
        if self.creating_new_key:
            self.print_notification("Creating new key...")
            return None
        key_input_dict = popuplauncher.launch_new_key_popup(self.root)
        if key_input_dict is None:
            self.print_notification("No new key created")
            return None
        else:
            self.creating_new_key = True
            self.create_new_key(key_input_dict)

    def create_new_key(self, key_input_dict):
        key_creator = keycreator.KeyCreator(self.gpg_data_context.get_home_dir(), self.queue)
        key_creator.execute(key_input_dict)
        self.print_notification("Creating new key...")

    def handle_create_new_key_result(self, payload):
        self.creating_new_key = False
        desc = payload['desc']
        result = payload['result']
        stderr = result.stderr
        if result.fingerprint is None:
            self.print_notification("Error: {}".format(desc))
            self.append_notification(stderr)
        else:
            self.print_notification("{} success! {}".format(desc, result.fingerprint))
            final = self.cleanup_new_key_success_stderr_string(stderr)
            self.append_notification(final)
            self.gpg_data_context.set_key_list()
            self.gpg_data_context.set_host_key()

    def cleanup_new_key_success_stderr_string(self, stderr):
        target = '[GNUPG:] PROGRESS primegen'
        draft = [x for x in stderr.split('\n') if target not in x]
        final = '\n'.join(draft)
        return final

    def delete_key_button_clicked(self, event):
        raw_key_list = self.gpg_data_context.get_raw_key_list()
        targets = popuplauncher.launch_delete_key_popup(self.root, raw_key_list)
        if targets is None:
            msg = 'Delete Keys Cancelled'
            self.print_notification(msg)
            return None

        deleter = keydeleter.KeyDeleter(self.gpg_data_context.get_home_dir())
        result = deleter.execute(targets)

        if result.status == 'ok':
            self.print_notification('Successfully deleted key(s).')
            self.append_notification(result.stderr)
            self.gpg_data_context.set_key_list()
            self.gpg_data_context.set_host_key()
        else:
            self.print_notification(result.status)
            self.append_notification(result.stderr)

    def print_notification(self, msg):
        self.view.notifications_box.print_msg(msg)

    def append_notification(self, msg):
        self.view.notifications_box.append_msg(msg)

    def launch_alert_log(self, msg):
        log.warning(msg)
        popuplauncher.launch_alert_box_popup(self.root, msg)
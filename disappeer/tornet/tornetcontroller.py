"""
tornetcontroller.py

Module for TorNetController class object, view controller for TorNetFrame notebook tab view

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import queueconsumer
from disappeer.net import  networkservers
from disappeer.torproxy import torproxycontroller
from disappeer.constants import constants
from disappeer.utilities import logger
from disappeer.utilities.logger import log
from disappeer.popups import popuplauncher


class TorNetController(queueconsumer.QueueConsumer):

    def __init__(self, root_params, tor_datacontext):
        super().__init__(root_params.root)
        self.root_params = root_params
        self.view = root_params.get_tor_net_frame()
        self.root_queue = root_params.root_queue
        self.tor_datacontext = tor_datacontext
        self.tor_proxy_controller = torproxycontroller.TorProxyController(self.queue)
        # TODO: refactor this method patch
        networkservers.contactresponseserver.SSLThreadedContactResponseTCPServer.get_sync_db_path = self.root_params.database_facade.get_server_sync_db_path
        # TODO: should the network servers get the TorNetController queue instead of the root queue for error handling?
        self.net_servers = networkservers.NetworkServers(self.root_queue)
        self.config_data_context()
        self.config_event_bindings()

    def config_data_context(self):
        self.tor_datacontext.add_tor_request_proxy_addr_observer(self.view.request_onion_entry_var)
        self.tor_datacontext.add_tor_response_proxy_addr_observer(self.view.response_onion_entry_var)
        self.tor_datacontext.add_tor_message_proxy_addr_observer(self.view.message_onion_entry_var)
        self.root_params.add_session_passphrase_observable_callback(self.session_passphrase_observable_callback)

    def config_event_bindings(self):
        command_button_release_1 = "<ButtonRelease-1>"

        # Server radio button bindings
        self.view.net_server_on_button.bind(command_button_release_1, self.net_server_radio_button_clicked)
        self.view.net_server_off_button.bind(command_button_release_1, self.net_server_radio_button_clicked)

        # Tor Proxy radio button bindings
        self.view.tor_proxy_on_button.bind(command_button_release_1, self.tor_proxy_radio_button_clicked)
        self.view.tor_proxy_off_button.bind(command_button_release_1, self.tor_proxy_radio_button_clicked)

    def handle_queue_payload(self, payload):
        desc = payload['desc']
        if desc == constants.command_list.Tor_Proxy_Request_Server:
            self.handle_tor_proxy_request_server(payload)
        elif desc == constants.command_list.Tor_Proxy_Response_Server:
            self.handle_tor_proxy_response_server(payload)
        elif desc == constants.command_list.Tor_Proxy_Message_Server:
            self.handle_tor_proxy_message_server(payload)
        elif desc == constants.command_list.Tor_Proxy_Error:
            self.handle_tor_proxy_error(payload)
        else:
            log.error("TorNetController QUEUE UNHANDLED PAYLOAD: {}".format(payload))

    def net_server_radio_button_clicked(self, event):
        current_selection = self.view.get_net_server_radio_var()
        if current_selection == 1:
            button_state = self.view.net_server_on_button['state']
            if button_state == 'disabled':
                return None
            self.view.handle_net_server_on_clicked_actions()
            self.start_network_services()
            self.view.set_net_server_status_var('Running')
        elif current_selection == 0:
            self.proxy_threads_are_alive()
            self.view.handle_net_server_off_clicked_actions()
            self.stop_network_services()
            self.view.set_net_server_status_var('Stopped')

    def start_network_services(self):
        self.net_servers.start_network_services()

    def stop_network_services(self):
        self.net_servers.stop_network_services()

    def tor_proxy_radio_button_clicked(self, event):
        if self.is_session_passphrase_none():
            return None

        current_selection = self.view.get_tor_proxy_radio_var()
        if current_selection == 1:
            self.tor_proxy_radio_button_start_clicked()

        elif current_selection == 0:
            self.tor_proxy_radio_button_stop_clicked()

    def tor_proxy_radio_button_start_clicked(self):
        button_state = self.view.tor_proxy_on_button['state']
        if button_state == 'disabled':
            return None

        elif not self.check_network_servers():
            self._update_tor_proxy_off_methods()
            return None

        elif self.proxy_threads_are_alive():
            self._update_tor_proxy_off_methods()
            return None

        check_button_val = self.view.get_tor_proxy_persistent_checkbutton_var()
        if check_button_val:
            self.tor_proxy_controller.start_all_proxies(persistent=check_button_val, tor_key_dir=self.get_user_tor_keys_dir())
        else:
            self.tor_proxy_controller.start_all_proxies()

        self._update_tor_proxy_on_methods()

    def _update_tor_proxy_on_methods(self):
        self.root_params.set_tor_proxy_running_observable(True)
        self.view.handle_tor_proxy_on_clicked_actions()
        self.view.set_tor_proxy_status_var('Running')
        self.view.disable_tor_proxy_persistent_checkbutton()

    def tor_proxy_radio_button_stop_clicked(self):
        button_state = self.view.tor_proxy_off_button['state']
        if button_state == 'disabled':
            return None
        self.tor_proxy_controller.stop_all_proxies()
        self._update_tor_proxy_off_methods()

    def _update_tor_proxy_off_methods(self):
        self.root_params.set_tor_proxy_running_observable(False)
        self.view.handle_tor_proxy_off_clicked_actions()
        self.view.set_tor_proxy_status_var('Stopped')
        self.view.enable_tor_proxy_persistent_checkbutton()

    def proxy_threads_are_alive(self):
        status = self.tor_proxy_controller.is_any_alive()
        if status:
            msg = 'Current TOR proxy threads are still running.'
            self.launch_alert_log(msg)
        return status

    def check_network_servers(self):
        if self.net_servers.are_running():
            return True
        else:
            msg = 'Network servers are not running. You must start network services to receive messages over TOR proxy.'
            self.launch_alert_log(msg)
            return False

    def is_session_passphrase_none(self):
        status = self.root_params.get_session_passphrase_observable()
        if status is None:
            msg = 'GPG host key passphrase not set. You must set passphrase from GPG tab for network session.'
            self.launch_alert_log(msg)
            return True
        else:
            return False

    def session_passphrase_observable_callback(self, obs):
        status = obs.get()
        if status is None:
            self.disable_tor_proxy_buttons()
        else:
            self.enable_tor_proxy_buttons()

    def handle_tor_proxy_request_server(self, payload):
        address = payload['address']
        self.tor_datacontext.set_tor_request_proxy_addr(address)

    def handle_tor_proxy_response_server(self, payload):
        address = payload['address']
        self.tor_datacontext.set_tor_response_proxy_addr(address)

    def handle_tor_proxy_message_server(self, payload):
        address = payload['address']
        self.tor_datacontext.set_tor_message_proxy_addr(address)

    def handle_tor_proxy_error(self, payload):
        # We get this error, ex. if tor service is not running
        log.error("Tor Proxy Error: {}".format(payload))
        log.debug("Is your local TOR service running?")
        server_name = payload['name']
        error = payload['error']
        if server_name == constants.command_list.Tor_Proxy_Request_Server:
            self.view.set_tor_onion_request_addr(error)
        elif server_name == constants.command_list.Tor_Proxy_Response_Server:
            self.view.set_tor_onion_response_addr(error)
        elif server_name == constants.command_list.Tor_Proxy_Message_Server:
            self.view.set_tor_onion_message_addr(error)

    def get_user_tor_keys_dir(self):
        keyid = self.root_params.get_host_key_id()
        tor_dir_path = self.tor_datacontext.get_user_tor_keys_dir(keyid)
        return tor_dir_path

    def launch_alert_log(self, msg):
        log.warning(msg)
        popuplauncher.launch_alert_box_popup(self.root, msg)

    def disable_tor_proxy_buttons(self):
        self.view.disable_tor_proxy_on_button()
        self.view.disable_tor_proxy_off_button()

    def enable_tor_proxy_buttons(self):
        self.view.enable_tor_proxy_on_button()
        self.view.enable_tor_proxy_off_button()



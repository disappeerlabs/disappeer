"""
sendnewmessagereceiver.py

Module for SendNewMessageReceiver class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


from disappeer.constants import constants
from disappeer.executor.receivers import abstractreceiver
from disappeer.popups import popuplauncher
from disappeer.net.message import messagefactory
from disappeer.net.bases import clientcontroller
import types
from disappeer.utilities.logger import log
command_list = constants.command_list


class SendNewMessageReceiver(abstractreceiver.AbstractReceiver):

    kwarg_keys = {'console_controller',
                  'tor_datacontext',
                  'gpg_datacontext',
                  'root_params'}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        suffix = '_Receiver'
        return command_list.Send_New_Message + suffix

    @property
    def valid_kwarg_keys(self):
        return self.kwarg_keys

    def execute(self, payload):
        # Get data record from payload
        data_record = payload['data_record']
        # Get current console text from console
        console_text = self.console_controller_get_console_text()
        # Launch send popup
        result = self.launch_send_message_popup(data_record, console_text)
        if result is None:
            return False

        build_payload_result = self.build_new_message_payload_dict(data_record.gpg_pub_key, console_text)
        if build_payload_result is False:
            msg = "New msg payload build returned false. Make sure network and proxies are up and running. Check logs."
            self.launch_alert_log(msg)
            return False

        arg_namespace = self.construct_arg_namespace(data_record, build_payload_result, console_text)
        self.start_client_controller(arg_namespace)

    def console_controller_get_console_text(self):
        result = self.console_controller.get_console_text()
        return result

    def tor_datacontext_get_tor_message_proxy_addr(self):
        result = self.tor_datacontext.get_tor_message_proxy_addr()
        if not result.endswith('onion'):
            return False
        return result

    def launch_send_message_popup(self, data_record, console_text):
        result = popuplauncher.launch_sendmessage_popup(self.root_params.root, data_record, console_text)
        return result

    def build_new_message_payload_dict(self, gpg_pub_key, msg_text):
        tor_message_onion_addr = self.tor_datacontext_get_tor_message_proxy_addr()
        if tor_message_onion_addr is False:
            msg = 'Cannot build message dict, tor address not set to onion address'
            log.error(msg)
            return False

        message_factory = messagefactory.MessageFactory(tor_message_onion_addr,
                                                        self.gpg_datacontext.get_home_dir(),
                                                        gpg_pub_key,
                                                        self.gpg_datacontext.get_host_key_fingerprint(),
                                                        msg_text,
                                                        self.root_params.get_session_passphrase_observable())
        result = message_factory.build()

        if message_factory.valid:
            return result
        else:
            log.error("Message Factory Build returned error: {}".format(message_factory.error))
            return False

    def construct_arg_namespace(self, data_record, payload_dict, message_text):
        argnamespace = types.SimpleNamespace(host=data_record.address_host,
                                             port=int(data_record.address_port),
                                             queue=self.root_params.root_queue,
                                             payload_dict=payload_dict,
                                             nonce=payload_dict['nonce'],
                                             command='MSG',
                                             data_record=data_record,
                                             plaintext=message_text)
        return argnamespace

    def start_client_controller(self, argspace):
        client_controller = clientcontroller.ClientController('send_message', argspace)
        client_controller.start()

    def launch_alert_log(self, msg):
        popuplauncher.launch_alert_box_popup(self.root_params.root, msg)
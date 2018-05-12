"""
rootcontroller.py

Root Controller module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


from disappeer.constants import constants
from disappeer.gpg import gpgcontroller
from disappeer.console import consolecontroller
from disappeer.utilities import queueconsumer
from disappeer.popups import popuplauncher
from disappeer.messages import messagescontroller
from disappeer.tornet import tornetcontroller
from disappeer.requests import requestscontroller
from disappeer.root import rootparameters
from disappeer.utilities.logger import log
import functools
from disappeer.executor import controllermediator
from disappeer.executor import commandclient


class RootController(queueconsumer.QueueConsumer):

    def __init__(self, root, root_view, gpg_data_context, database_facade, tor_data_context):
        super().__init__(root)
        self.view = root_view
        self.gpg_datacontext = gpg_data_context
        self.database_facade = database_facade
        self.tor_datacontext = tor_data_context

        self.root_params = rootparameters.RootParameters(self.root, self.view, self.queue, self.database_facade, self.gpg_datacontext.get_host_key_observer())

        self.tornet_controller = tornetcontroller.TorNetController(self.root_params,
                                                                   self.tor_datacontext)

        self.requests_controller = requestscontroller.RequestsController(self.root_params,
                                                                         self.tor_datacontext,
                                                                         self.gpg_datacontext.get_home_dir_observer())

        self.gpg_controller = gpgcontroller.GPGController(self.root_params,
                                                          self.gpg_datacontext)

        self.console_controller = consolecontroller.ConsoleController(self.root_params,
                                                                      self.gpg_datacontext)

        self.message_controller = messagescontroller.MessagesController(self.root_params,
                                                                        self.gpg_datacontext.get_home_dir_observer())
        self.config_event_bindings()
        self.config_menubar()
        # TODO: host key observer is redundant, can just add callback to the host key observable itself
        self.gpg_datacontext.host_key_observer.add_callback(self.delay_update_all_treeviews)

        self.controller_mediator = controllermediator.ControllerMediator(self.database_facade,
                                                                         self.gpg_datacontext,
                                                                         self.tor_datacontext,
                                                                         self.requests_controller,
                                                                         self.message_controller,
                                                                         self.console_controller,
                                                                         self.root_params)
        self.command_client = commandclient.CommandClient(self.controller_mediator)

    def config_event_bindings(self):
        pass
        # Uncomment to enable Debug Panel Buttons
        # self.view.left_panel.debug_button.bind("<ButtonRelease-1>", self.debug_button_clicked)
        # self.view.left_panel.debug_button_2.bind("<ButtonRelease-1>", self.debug_button_2_clicked)

    def handle_queue_payload(self, payload):
        desc = payload['desc']
        command_list = constants.command_list

        if desc == command_list.New_Contact_Req:
            self.handle_new_contact_request(payload)
        elif desc == command_list.New_Contact_Req_Client_Err:
            self.handle_new_contact_request_client_error(payload)
        elif desc == command_list.New_Contact_Req_Client_Res:
            self.handle_new_contact_request_client_response(payload)
        elif desc == command_list.New_Contact_Res:
            self.handle_new_contact_response(payload)
        elif desc == command_list.New_Contact_Res_Client_Err:
            self.handle_new_contact_response_client_error(payload)
        elif desc == command_list.Send_New_Message:
            self.handle_send_new_message(payload)
        elif desc == command_list.Received_New_Message:
            self.handle_received_new_message(payload)
        elif desc == command_list.Send_New_Message_Client_Err:
            self.handle_send_new_message_client_error(payload)
        elif desc == command_list.Send_New_Message_Client_Res:
            self.handle_send_new_message_client_response(payload)
        elif desc == command_list.New_Contact_Res_Client_Res:
            self.handle_new_contact_response_client_response(payload)
        elif desc == command_list.Server_Error:
            self.handle_server_error(payload)
        elif desc == command_list.Inspect_Message:
            self.handle_inspect_message(payload)
        else:
            log.error("ROOT CONTROLLER QUEUE UNHANDLED PAYLOAD:", payload)

    ########################
    #  View Update Methods #
    ########################

    def delay_update_all_treeviews(self, obs_obj):
        self.root.after(2000, self.update_all_treeviews)

    def update_all_treeviews(self):
        """
        callback method to update treeviews, obs_obj is not necessary for the method.
        It is required by the signature of observable callbacks.
        :param obs_obj: observable obj if called by observable, otherwise just provide placeholder
        """
        self.requests_controller.update_all_treeviews()
        self.message_controller.update_all_treeviews()

    ###########################
    #  CONSOLE Update METHODS #
    ###########################

    def handle_inspect_message(self, payload):
        argspace = payload['payload']
        msg_text = argspace.message_text
        self.console_controller.print_to_console(msg_text)

    ################################
    #  HANDLE SERVER ERROR METHODS #
    ################################

    def handle_server_error(self, payload):
        # TODO: add tests and handling for Server Error
        log.error("RootController interface {} found server error: {}".format(payload['interface'], payload['error']))

    ##########################################
    # HANDLE NEW CONTACT RESPONSE and CLIENT #
    ##########################################

    def handle_new_contact_response_client_response(self, payload):
        # REFACTORED WITH COMMAND CLIENT
        payload_dict = dict(payload=payload)
        self.command_client.run(constants.command_list.New_Contact_Res_Client_Res, **payload_dict)

    def handle_new_contact_response_client_error(self, payload):
        msg = "RootController Contact Response Client Error: {}".format(payload['error'])
        self.launch_alert_log(msg)

    def handle_new_contact_response(self, payload):
        # REFACTORED WITH COMMAND CLIENT
        payload_dict = dict(payload=payload)
        self.command_client.run(constants.command_list.New_Contact_Res, **payload_dict)

    #########################################
    #   HANDLE NEW CONTACT REQUEST METHODS  #
    #########################################

    def handle_new_contact_request(self, payload):
        self.database_facade.insert_contact_request(payload)
        self.requests_controller.update_received_requests_treeview()

    def handle_new_contact_request_client_error(self, payload):
        """
        Called from QueueConsumer, New Contact Request Client send resulted in an error.
        :param payload:
        """
        msg = "Contact REQUEST CLIENT ERROR: {}".format(payload['error'])
        self.launch_alert_log(msg)

    def handle_new_contact_request_client_response(self, payload):
        # REFACTORED WITH COMMAND CLIENT
        payload_dict = dict(payload=payload)
        self.command_client.run(constants.command_list.New_Contact_Req_Client_Res, **payload_dict)

    ################################
    #   HANDLE NEW MESSAGE METHODS #
    ################################

    def handle_received_new_message(self, incoming_payload):
        # REFACTORED WITH COMMAND CLIENT
        payload_dict = dict(payload=incoming_payload)
        self.command_client.run(constants.command_list.Received_New_Message, **payload_dict)

    def handle_send_new_message(self, payload):
        # REFACTORED WITH COMMAND CLIENT
        payload_dict = dict(payload=payload)
        self.command_client.run(constants.command_list.Send_New_Message, **payload_dict)

    def handle_send_new_message_client_error(self, payload):
        msg = "Send new message client error payload: {}".format(payload['error'])
        self.launch_alert_log(msg)

    def handle_send_new_message_client_response(self, payload):
        # REFACTORED WITH COMMAND CLIENT
        payload_dict = dict(payload=payload)
        self.command_client.run(constants.command_list.Send_New_Message_Client_Res, **payload_dict)

    #######################
    #   LAUNCH ALERT LOG  #
    #######################

    def launch_alert_log(self, msg):
        log.warning(msg)
        popuplauncher.launch_alert_box_popup(self.root, msg)

    ##########
    # CONFIG #
    ##########

    def config_menubar(self):
        app_menu = self.root_params.get_app_menu_obj()
        app_menu.add_command(label='About', command=functools.partial(popuplauncher.launch_about_box_popup, self.root))
        app_menu.add_command(label='Exit', command=self.exit)

    def exit(self):
        try:
            self.tornet_controller.stop_network_services()
        except AttributeError as err:
            pass
        self.tornet_controller.tor_proxy_controller.stop_all_proxies()
        self.root.quit()

    ########################################
    #   DEBUG FRAME BUTTON HANDLERS        #
    ########################################

    def debug_button_clicked(self, event):
        log.debug("Debug Button ONE Clicked")

    def debug_button_2_clicked(self, event):
        log.debug("Debug Button TWO Clicked")




"""
requestscontroller.py

Module for RequestsController class object, controller for sent/received requests notebook frame.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups import popuplauncher
from disappeer.net.contact import contactrequestfactory
from disappeer.net.contact import contactrequestvalidator
from disappeer.net.bases import clientcontroller
import types
from disappeer.net.contactresponse import contactresponsefactory
from disappeer.utilities import logger
from disappeer import settings
from disappeer.utilities.logger import log


class RequestsController:

    def __init__(self, root_params, tor_datacontext, gpg_homedir_observer):
        self.root_params = root_params
        self.root = self.root_params.root
        self.view = self.root_params.get_requests_frame()
        self.root_queue = self.root_params.root_queue
        self.database_facade = self.root_params.database_facade
        self.tor_datacontext = tor_datacontext
        self.gpg_homedir_observer = gpg_homedir_observer
        self.config_event_bindings()
        self.update_all_treeviews()

    def config_event_bindings(self):
        command_button_release_1 = "<ButtonRelease-1>"
        self.view.send_request_button.bind(command_button_release_1, self.send_request_button_clicked)
        self.view.sent_requests_tree_view.bind(command_button_release_1, self.sent_request_treeview_clicked)
        self.view.received_requests_tree_view.bind(command_button_release_1, self.received_request_treeview_clicked)

    ##################################
    #   Treeview Update Methods      #
    ##################################

    def update_all_treeviews(self):
        self.update_sent_requests_treeview()
        self.update_received_requests_treeview()

    def update_sent_requests_treeview(self):
        # TODO: should this get nonce instead of fingerprint???
        data_rows = self.database_facade.fetch_all_pending_contact_response_hosts_and_fingerprints()
        self.view.append_all_to_sent_requests(data_rows)

    def update_received_requests_treeview(self):
        """
        View update method using db table data.
        """
        data_rows = self.database_facade.fetch_all_contact_request_address_and_nonce_with_status()
        self.view.append_all_to_received_requests(data_rows)

    #######################################
    #  SEND REQUEST BUTTON CLICKED        #
    #######################################

    def send_request_button_clicked(self, event):
        result = popuplauncher.launch_peerconnect_popup(self.root)
        if result is None:
            return None
        else:
            self.contact_request_client_send(result)

    def contact_request_client_send(self, host_port_tuple):
        payload_build_result = self.build_contact_request_dict()
        if payload_build_result is False:
            msg = 'Build contact request dict returned false. Check log for network or gpg error'
            self.launch_alert_log(msg)
            return False

        # validate and check for validation error
        validator = self.validate_contact_request_dict(payload_build_result)
        if not validator.valid:
            msg = "Client Req Payload Build Error: {}".format(validator.error)
            self.launch_alert_log(msg)
            return validator

        # build argnamespace
        host = host_port_tuple[0]
        port = int(host_port_tuple[1])
        args = types.SimpleNamespace(host=host,
                                     port=port,
                                     queue=self.root_queue,
                                     nonce=validator.nonce,
                                     payload_dict=payload_build_result)
        client_controller = clientcontroller.ClientController('contact_request', args)
        client_controller.start()

    def build_contact_request_dict(self):
        tor_response_onion_addr = self.tor_datacontext.get_tor_response_proxy_addr()
        if not tor_response_onion_addr.endswith('onion'):
            log.info("Tor address not yet set, cannot send request.")
            return False

        factory = contactrequestfactory.ContactRequestFactory(self.tor_datacontext.get_tor_response_proxy_addr(),
                                                              self.gpg_homedir_observer.get(),
                                                              self.root_params.get_session_passphrase_observable())
        build_result = factory.build()

        if hasattr(build_result, 'stderr'):
            msg = "Build contact request dict, GPG SIG ERROR: {}".format(build_result.stderr)
            log.error(msg)
            return False

        return build_result

    def validate_contact_request_dict(self, request_payload_dict):
        """
        Validate contact request payload dict
        :param request_payload_dict: created by build method of ContactRequestFactory
        :return: validator
        """
        validator = contactrequestvalidator.ContactRequestValidator(request_payload_dict)
        return validator

    ###############################################
    #   Received Request Treeview Clicked Methods #
    ###############################################

    def received_request_treeview_clicked(self, event):
        nonce = self.view.get_clicked_received_request_treeview_nonce()
        if nonce is None:
            return None

        data_record = self.database_facade.fetch_one_contact_request_by_nonce(nonce)
        result = popuplauncher.launch_contactrequest_popup(self.root, data_record)

        if result is None:
            self.database_facade.update_contact_request_col_to_val_where_x_is_y('status', 'read', 'nonce', data_record.nonce)
        elif result == 'invalid':
            self.database_facade.delete_contact_request_where_x_is_y('nonce', data_record.nonce)
        elif result == 'reject':
            self.database_facade.delete_contact_request_where_x_is_y('nonce', data_record.nonce)
        elif result == 'accept':
            self.database_facade.update_contact_request_col_to_val_where_x_is_y('status', result, 'nonce', data_record.nonce)
            self.contact_response_client_send(data_record)

        self.update_received_requests_treeview()

    def contact_response_client_send(self, data_record):
        build_result = self.build_contact_response_dict(data_record)
        if build_result is False:
            msg = "Build contact response client send returned error. May be network or GPG error. Check logs."
            self.launch_alert_log(msg)
            return None

        payload_dict, nonce = build_result

        argnamespace = types.SimpleNamespace(host=data_record.address_host,
                                             port=int(data_record.address_port),
                                             queue=self.root_queue,
                                             payload_dict=payload_dict,
                                             nonce=nonce,
                                             request_nonce=data_record.nonce,
                                             command='RES')
        client_controller = clientcontroller.ClientController('contact_response', argnamespace)
        client_controller.start()

    def build_contact_response_dict(self, data_record):
        """
        Build payload for ContactResponseClient
        :param data_record:
        :return: build result payload dict or false on error
        """
        tor_response_onion_addr = self.tor_datacontext.get_tor_message_proxy_addr()
        if not tor_response_onion_addr.endswith('onion'):
            log.info("Cannot build contact response dict, tor address not set.")
            return False

        factory = contactresponsefactory.ContactResponseFactory(tor_response_onion_addr,
                                                                self.gpg_homedir_observer.get(),
                                                                data_record,
                                                                self.root_params.get_session_passphrase_observable())
        build_result = factory.build()
        if factory.valid:
            return build_result
        else:
            log.error("Contact Response Factory Build Error: {}".format(factory.error))
            return False

    ###############################################
    #   Sent Request Treeview Clicked Methods #
    ###############################################

    def sent_request_treeview_clicked(self, event):
        sent_req_vals = self.view.get_clicked_sent_request_treeview_vals()
        if sent_req_vals is None:
            return None

        address = sent_req_vals[0]
        fingerprint = sent_req_vals[1]
        gpg_pub_key = self.database_facade.fetch_contact_response_pub_key_by_fingerprint(fingerprint)

        result = popuplauncher.launch_display_sent_request_popup(self.root, gpg_pub_key, address)


        return True

    ####################
    #   LAUNCH ALERTS  #
    ####################

    def launch_alert_log(self, msg):
        log.warning(msg)
        popuplauncher.launch_alert_box_popup(self.root, msg)

    def launch_user_alert(self, msg):
        popuplauncher.launch_alert_box_popup(self.root, msg)
















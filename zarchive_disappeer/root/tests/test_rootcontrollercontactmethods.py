"""
test_rootcontrollercontactmethods.py

Test suite for development of RootController Contact Request and Response handling methods
Necessary after refactor, removing the monolithic NetController.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from unittest.mock import MagicMock, patch
from disappeer.constants import constants
from disappeer.requests import requestscontroller
from disappeer.root.tests.rootsetupclass import RootSetupClass


class TestRootControllerNetContactReqResRelated(RootSetupClass):
    example_client_response_payload_NOT_valid = {'nonce': '6c4b060de315f72ab205deb19145132772fb5d44',
                                                      'result': {'desc': 'ACK', 'nonce': '6c4b060de315f72ab205deb19145132772fb5d44',
                                                                 'gpg_pub_key': '-----BEGIN PGP PUBLIC KEY BLOCK-----\nVersion: GnuPG v1\n\n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\n=IF8v\n-----END PGP PUBLIC KEY BLOCK-----\n'},
                                                      'nonce_valid': False,
                                                      'host': 'host_string',
                                                      'desc': 'New_Contact_Req_Client_Res'}
    example_client_response_payload_valid = {'nonce': '6c4b060de315f72ab205deb19145132772fb5d44',
                                                  'result': {'desc': 'ACK', 'nonce': '6c4b060de315f72ab205deb19145132772fb5d44',
                                                             'gpg_pub_key': '-----BEGIN PGP PUBLIC KEY BLOCK-----\nVersion: GnuPG v1\n\n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\n=IF8v\n-----END PGP PUBLIC KEY BLOCK-----\n'},
                                                  'nonce_valid': True,
                                                  'host': 'host_string',
                                                  'desc': 'New_Contact_Req_Client_Res'}


    def test_requests_controller_attr_set(self):
        self.assertIsInstance(self.x.requests_controller, requestscontroller.RequestsController)
        self.assertEqual(self.x.requests_controller.root, self.x.root)
        self.assertEqual(self.x.requests_controller.view, self.x.view.left_panel.requests_frame)
        self.assertEqual(self.x.requests_controller.root_queue, self.x.queue)
        self.assertEqual(self.x.requests_controller.tor_datacontext, self.x.tor_datacontext)
        self.assertEqual(self.x.requests_controller.gpg_homedir_observer, self.x.gpg_datacontext.home_dir_observer)

    #######################################
    #  HANDLE QUEUE PAYLOAD METHODS       #
    #######################################

    def test_handle_queue_payload_new_contact_req_calls_handle_new_contact_req_method(self):
        val_dict = dict(desc=constants.command_list.New_Contact_Req)
        target = self.x.handle_new_contact_request = MagicMock()
        self.x.handle_queue_payload(val_dict)
        target.assert_called_with(val_dict)

    def test_handle_queue_payload_new_contact_req_client_error_calls_handle_new_contact_req_client_error_method(self):
        val_dict = dict(desc=constants.command_list.New_Contact_Req_Client_Err)
        target = self.x.handle_new_contact_request_client_error = MagicMock()
        self.x.handle_queue_payload(val_dict)
        target.assert_called_with(val_dict)

    def test_handle_queue_payload_new_contact_req_client_res_calls_handle_new_contact_req_client_response_method(self):
        val_dict = dict(desc=constants.command_list.New_Contact_Req_Client_Res)
        target = self.x.handle_new_contact_request_client_response = MagicMock()
        self.x.handle_queue_payload(val_dict)
        target.assert_called_with(val_dict)

    def test_handle_queue_payload_new_contact_response_calls_handle_new_contact_response_method(self):
        val_dict = dict(desc=constants.command_list.New_Contact_Res)
        target = self.x.handle_new_contact_response = MagicMock()
        self.x.handle_queue_payload(val_dict)
        target.assert_called_with(val_dict)

    def test_handle_queue_payload_new_contact_res_client_error_calls_handle_new_contact_res_client_error_method(self):
        val_dict = dict(desc=constants.command_list.New_Contact_Res_Client_Err)
        target = self.x.handle_new_contact_response_client_error = MagicMock()
        self.x.handle_queue_payload(val_dict)
        target.assert_called_with(val_dict)

    def test_handle_queue_payload_new_contact_res_client_res_calls_handle_new_contact_res_client_res_method(self):
        val_dict = dict(desc=constants.command_list.New_Contact_Res_Client_Res)
        target = self.x.handle_new_contact_response_client_response = MagicMock()
        self.x.handle_queue_payload(val_dict)
        target.assert_called_with(val_dict)

    #############################################
    #  HANDLE NEW CONTACT REQUEST METHODS       #
    #############################################

    def test_handle_new_contact_req_method_calls_new_payload_on_db_table(self):
        payload = dict()
        target = self.x.database_facade.insert_contact_request = MagicMock()
        self.x.handle_new_contact_request(payload)
        target.assert_called_with(payload)

    def test_handle_new_contact_req_method_calls_update_received_contact_requests_treeview_method_in_requests_controller(self):
        payload = dict()
        sub = self.x.database_facade.insert_contact_request = MagicMock()
        target = self.x.requests_controller.update_received_requests_treeview = MagicMock()
        self.x.handle_new_contact_request(payload)
        target.assert_called_with()

    #########################################################
    #   HANDLE NEW CONTACT REQUEST CLIENT RESPONSE METHODS  #
    #########################################################

    def test_handle_new_contact_request_client_response_calls_command_client_with_args(self):
        payload = dict(desc=constants.command_list.New_Contact_Req_Client_Res, payload='payload')
        payload_dict = dict(payload=payload)
        target = self.x.command_client = MagicMock()
        result = self.x.handle_new_contact_request_client_response(payload)
        target.run.assert_called_with(constants.command_list.New_Contact_Req_Client_Res, **payload_dict)

    def test_handle_new_contact_request_client_error_calls_alert_log(self):
        mock_payload = dict(error='error_msg')
        target = self.x.launch_alert_log = MagicMock()
        self.x.handle_new_contact_request_client_error(mock_payload)
        self.assertTrue(target.called)

    #########################################
    #   HANDLE NEW CONTACT RESPONSE METHODS #
    #########################################

    def test_handle_new_contact_response_calls_command_client_with_args(self):
        payload = dict(desc=constants.command_list.New_Contact_Res, payload='payload')
        payload_dict = dict(payload=payload)
        target = self.x.command_client = MagicMock()
        result = self.x.handle_new_contact_response(payload)
        target.run.assert_called_with(constants.command_list.New_Contact_Res, **payload_dict)


    #########################################################
    #   HANDLE NEW CONTACT RESPONSE CLIENT RESPONSE METHODS #
    #########################################################

    def test_handle_new_contact_response_client_response_calls_command_client_with_args(self):
        payload = dict(desc=constants.command_list.New_Contact_Res_Client_Res,
                       result='',
                       nonce='',
                       nonce_valid=False,
                       request_nonce='')
        payload_dict = dict(payload=payload)
        target = self.x.command_client = MagicMock()
        result = self.x.handle_new_contact_response_client_response(payload)
        target.run.assert_called_with(constants.command_list.New_Contact_Res_Client_Res, **payload_dict)

    def test_handle_new_contact_response_client_error_calls_alert_method(self):
        target = self.x.launch_alert_log = MagicMock()
        mock_payload = dict(error='error_msg')
        self.x.handle_new_contact_response_client_error(mock_payload)
        self.assertTrue(target.called)

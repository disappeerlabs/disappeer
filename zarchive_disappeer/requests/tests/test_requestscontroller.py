"""
test_requestscontroller.py

Test suite for RequestsController module and class object, controls left panel notebook frame for sent/received msgs.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.requests import requestscontroller
import tkinter
import queue
from disappeer.popups import popuplauncher
from disappeer.net.contact import contactrequestfactory
from disappeer.net.contact import contactrequestvalidator
import types
from disappeer.net.bases import clientcontroller
from disappeer import settings
from disappeer.models.db import dbcontactrequesttable
from disappeer.models.db import dbpendingcontactresponsetable
from disappeer.net.contactresponse import contactresponsefactory
from disappeer.root import rootparameters
from disappeer.root import rootview
from disappeer.utilities import logger
from disappeer.utilities.logger import log
from disappeer.models.db import databasefacade


class TestImports(unittest.TestCase):

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, requestscontroller.popuplauncher)

    def test_contactrequestfactory(self):
        self.assertEqual(contactrequestfactory, requestscontroller.contactrequestfactory)

    def test_contactrequestvalidator(self):
        self.assertEqual(contactrequestvalidator, requestscontroller.contactrequestvalidator)

    def test_types(self):
        self.assertEqual(types, requestscontroller.types)

    def test_clientcontroller(self):
        self.assertEqual(clientcontroller, requestscontroller.clientcontroller)

    def test_settings(self):
        self.assertEqual(settings, requestscontroller.settings)

    def test_contactresponsefactory(self):
        self.assertEqual(contactresponsefactory, requestscontroller.contactresponsefactory)

    def test_logger(self):
        self.assertEqual(logger, requestscontroller.logger)

    def test_log(self):
        self.assertEqual(logger.log, requestscontroller.log)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.command = "<ButtonRelease-1>"
        self.root = tkinter.Tk()
        self.root_view = MagicMock()
        self.queue = queue.Queue()
        self.database_facade = MagicMock(spec=databasefacade.DatabaseFacade)
        self.mock_observer = MagicMock()
        self.root_params = rootparameters.RootParameters(self.root, self.root_view, self.queue, self.database_facade, self.mock_observer)
        mock_view_method = self.root_params.get_requests_frame = MagicMock(return_value=MagicMock())
        self.view = mock_view_method.return_value
        self.tor_datacontact = MagicMock()
        self.gpg_homedir_observer = MagicMock()
        self.x = requestscontroller.RequestsController(self.root_params,
                                                       self.tor_datacontact,
                                                       self.gpg_homedir_observer)

    def test_instance(self):
        self.assertIsInstance(self.x, requestscontroller.RequestsController)

    def test_root_params_attr_set(self):
        self.assertEqual(self.root_params, self.x.root_params)

    def test_root_attribute_set(self):
        self.assertEqual(self.root, self.x.root)

    def test_view_attribute_set(self):
        self.assertEqual(self.view, self.x.view)

    def test_root_queue_attribute_set(self):
        self.assertEqual(self.queue, self.x.root_queue)

    def test_database_facade_attr_set(self):
        self.assertEqual(self.x.database_facade, self.x.root_params.database_facade)

    def test_tor_datacontext_attr_set(self):
        self.assertEqual(self.tor_datacontact, self.x.tor_datacontext)

    def test_gpg_homedir_observer_attr_set(self):
        self.assertEqual(self.gpg_homedir_observer, self.x.gpg_homedir_observer)

    def test_config_event_bindings_calls_bind_on_send_request_button(self):
        self.x.config_event_bindings()
        self.view.send_request_button.bind.assert_called_with(self.command, self.x.send_request_button_clicked)

    def test_config_event_bindings_calls_bind_on_received_requests_treeview_item(self):
        self.x.config_event_bindings()
        self.view.received_requests_tree_view.bind.assert_called_with(self.command, self.x.received_request_treeview_clicked)

    def test_config_event_bindings_calls_bind_on_sent_requests_treeview_item(self):
        self.x.config_event_bindings()
        self.x.view.sent_requests_tree_view.bind.assert_called_with(self.command, self.x.sent_request_treeview_clicked)

    @patch('disappeer.requests.requestscontroller.RequestsController.update_all_treeviews')
    @patch('disappeer.requests.requestscontroller.RequestsController.config_event_bindings')
    def test_constructor_calls_config_event_bindings_update_all_treeviews(self, config_events, update_treeviews):
        self.x = requestscontroller.RequestsController(self.root_params, self.tor_datacontact, self.gpg_homedir_observer)
        self.assertTrue(config_events.called)
        self.assertTrue(update_treeviews.called)

    @patch.object(requestscontroller.popuplauncher, 'launch_alert_box_popup')
    def test_launch_alert_log_launches_alert_and_log_with_msg(self, alertbox):
        msg = 'hello'
        self.x.launch_alert_log(msg)
        alertbox.assert_called_with(self.x.root, msg)

    @patch.object(requestscontroller.popuplauncher, 'launch_alert_box_popup')
    def test_launch_user_alert_launches_alert_with_msg(self, alertbox):
        msg = 'hello'
        self.x.launch_user_alert(msg)
        alertbox.assert_called_with(self.x.root, msg)

    #######################################
    #  SEND REQUEST BUTTON CLICKED        #
    #######################################

    @patch('disappeer.popups.popuplauncher.launch_peerconnect_popup')
    def test_send_request_button_clicked_launches_peer_connect_popup(self, mocked_popup):
        sub = self.x.build_contact_request_dict = MagicMock()
        sub1 = self.x.contact_request_client_send = MagicMock()
        self.x.send_request_button_clicked(None)
        mocked_popup.assert_called_with(self.x.root)

    @patch('disappeer.popups.popuplauncher.launch_peerconnect_popup')
    def test_send_request_button_clicked_returns_none_if_popup_cancelled(self, mocked_popup):
        mocked_popup.return_value = None
        result = self.x.send_request_button_clicked(None)
        self.assertIsNone(result)

    @patch('disappeer.popups.popuplauncher.launch_peerconnect_popup')
    def test_send_request_button_clicked_calls_contact_request_client_send(self, mocked_popup):
        mocked_popup.return_value = ('localhost', '1234')
        sub = self.x.build_contact_request_dict = MagicMock()
        target = self.x.contact_request_client_send = MagicMock()
        self.x.send_request_button_clicked(None)
        target.assert_called_with(mocked_popup.return_value)

    #######################################
    #  CONTACT REQUEST CLIENT SEND        #
    #######################################

    def test_build_contact_request_dict_returns_false_if_tor_response_proxy_addr_is_not_onion(self):
        tmp_arg = 'xxx'
        sub = self.x.tor_datacontext.get_tor_response_proxy_addr = MagicMock(return_value=tmp_arg)
        result = self.x.build_contact_request_dict()
        self.assertIs(result, False)

    @patch.object(requestscontroller.contactrequestfactory, 'ContactRequestFactory')
    def test_build_contact_request_dict_method_inits_contact_request_factory(self, mod):
        tmp_arg = 'xxx.onion'
        sub = self.x.tor_datacontext.get_tor_response_proxy_addr = MagicMock(return_value=tmp_arg)
        result = self.x.build_contact_request_dict()
        self.assertTrue(mod.called)
        mod.assert_called_with(sub.return_value, self.x.gpg_homedir_observer.get(), self.root_params.get_session_passphrase_observable())

    @patch.object(requestscontroller.contactrequestfactory, 'ContactRequestFactory')
    def test_build_contact_request_dict_method_calls_build_on_contact_request_factory(self, mod):
        mod.return_value = MagicMock()
        tmp_arg = 'xxx.onion'
        sub = self.x.tor_datacontext.get_tor_response_proxy_addr = MagicMock(return_value=tmp_arg)
        result = self.x.build_contact_request_dict()
        self.assertTrue(mod.called)
        self.assertTrue(mod.return_value.build.called)

    @patch.object(requestscontroller.contactrequestfactory, 'ContactRequestFactory')
    def test_build_contact_request_dict_returns_false_if_build_returns_error(self, mod):
        class MockBadResult(MagicMock):
                data = b''
                stderr = 'Mock Error'
        mod.return_value = MockBadResult()
        tmp_arg = 'xxx.onion'
        sub = self.x.tor_datacontext.get_tor_response_proxy_addr = MagicMock(return_value=tmp_arg)
        result = self.x.build_contact_request_dict()
        self.assertIs(result, False)

    @patch.object(requestscontroller.contactrequestfactory, 'ContactRequestFactory')
    def test_build_contact_request_dict_returns_result_of_valid_build(self, mod):
        val = dict()
        class MockGoodResult(MagicMock):
            def build(self):
                return val

        mod.return_value = MockGoodResult()
        tmp_arg = 'xxx.onion'
        sub = self.x.tor_datacontext.get_tor_response_proxy_addr = MagicMock(return_value=tmp_arg)
        result = self.x.build_contact_request_dict()
        self.assertEqual(result, mod.return_value.build())

    def test_contact_request_client_send_calls_alert_returns_false_if_build_contact_request_dict_returns_false(self):
        sub = self.x.build_contact_request_dict = MagicMock(return_value=False)
        arg_vals = ('localhost', '1234')
        alert_target = self.x.launch_alert_log = MagicMock()
        result = self.x.contact_request_client_send(arg_vals)
        self.assertIs(result, False)
        self.assertTrue(alert_target.called)

    def test_validate_contact_request_dict_method_returns_validator(self):
        payload = dict()
        result = self.x.validate_contact_request_dict(payload)
        self.assertIsInstance(result, contactrequestvalidator.ContactRequestValidator)

    def test_contact_request_client_send_calls_alert_returns_validator_with_error_on_invalid_payload(self):
        request_payload_dict = dict(desc='hello')
        sub = self.x.build_contact_request_dict = MagicMock(return_value=request_payload_dict)
        arg_vals = ('localhost', '1234')
        alert_target = self.x.launch_alert_log = MagicMock()
        result = self.x.contact_request_client_send(arg_vals)
        self.assertIsNotNone(result.error)
        self.assertIsInstance(result, contactrequestvalidator.ContactRequestValidator)
        self.assertTrue(alert_target.called)

    def test_contact_request_client_send_calls_client_controller(self):
        request_payload_dict = dict(desc='hello')
        nonce_val = 'nonce'
        sub = self.x.build_contact_request_dict = MagicMock(return_value=request_payload_dict)
        sub1 = self.x.validate_contact_request_dict = MagicMock(return_value=MagicMock(valid=True, nonce=nonce_val))
        arg_vals = ('localhost', '1234')
        argnamespace = types.SimpleNamespace(host='localhost', nonce=nonce_val, port=1234, queue=self.x.root_queue, payload_dict=sub.return_value)
        target = requestscontroller.clientcontroller.ClientController = MagicMock()
        self.x.contact_request_client_send(arg_vals)
        target.assert_called_with('contact_request', argnamespace)

    def test_update_sent_requests_treeview_gets_db_data_rows(self):
        target = self.x.database_facade.fetch_all_pending_contact_response_hosts_and_fingerprints = MagicMock()
        self.x.update_sent_requests_treeview()
        target.assert_called_with()

    def test_update_sent_requests_treeview_calls_view_update_methpd(self):
        val = 'xxx'
        sub = self.x.database_facade.fetch_all_pending_contact_response_hosts_and_fingerprints = MagicMock(return_value=val)
        target = self.x.view.append_all_to_sent_requests = MagicMock()
        self.x.update_sent_requests_treeview()
        target.assert_called_with(sub.return_value)

    def test_update_received_requests_treeview_calls_fetch_address_and_nonce_with_status(self):
        target = self.x.database_facade.fetch_all_contact_request_address_and_nonce_with_status = MagicMock()
        self.x.update_received_requests_treeview()
        target.assert_called_with()

    def test_update_received_requests_treeview_calls_append_all_method_on_view(self):
        val = [(1), (2)]
        sub = self.x.database_facade.fetch_all_contact_request_address_and_nonce_with_status = MagicMock(return_value=val)
        self.x.update_received_requests_treeview()
        self.x.view.append_all_to_received_requests.assert_called_with(sub.return_value)

    def test_update_all_treeviews_calls_all_treeview_update_methods(self):
        sent_treeview_method = self.x.update_sent_requests_treeview = MagicMock()
        recvd_treeview_method = self.x.update_received_requests_treeview = MagicMock()
        self.x.update_all_treeviews()
        sent_treeview_method.assert_called_with()
        recvd_treeview_method.assert_called_with()

    ###############################################
    #   Recevied Request Treeview Clicked TESTS   #
    ###############################################

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_calls_get_nonce_on_view(self, pop, ctrlr):
        target = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock()
        self.x.received_request_treeview_clicked(None)
        target.assert_called_with()

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_returns_none_if_nonce_is_none(self, pop, ctrlr):
        target = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock(return_value=None)
        result = self.x.received_request_treeview_clicked(None)
        self.assertIsNone(result)

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_fetches_db_record_with_nonce(self, pop, contr):
        val = 'xxx'
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock(return_value=val)
        target = self.x.database_facade.fetch_one_contact_request_by_nonce = MagicMock()
        result = self.x.received_request_treeview_clicked(None)
        target.assert_called_with(sub.return_value)

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_launches_contact_request_popup_with_db_record(self,  pop, controller):
        val = 'xxx'
        db_val = 'yyy'
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock(return_value=val)
        sub2 = self.x.database_facade.fetch_one_contact_request_by_nonce = MagicMock(return_value=db_val)
        result = self.x.received_request_treeview_clicked(None)
        pop.assert_called_with(self.x.root, sub2.return_value)

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_sets_db_record_status_to_read_calls_update_received_requests_if_popup_returns_none(self,  pop, controller):
        val = 'xxx'
        db_val = 'yyy'
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock(return_value=val)
        sub2 = self.x.database_facade.fetch_one_contact_request_by_nonce = MagicMock()
        pop.return_value = None
        target = self.x.database_facade.update_contact_request_col_to_val_where_x_is_y = MagicMock()
        target_2 = self.x.update_received_requests_treeview = MagicMock()
        result = self.x.received_request_treeview_clicked(None)
        self.assertIsNone(result)
        target.assert_called_with('status', 'read', 'nonce', sub2().nonce)
        target_2.assert_called_with()

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_deletes_record_if_popup_returns_invalid(self,  pop, controller):
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock()
        sub2 = self.x.database_facade.fetch_one_contact_request_by_nonce = MagicMock()
        target = self.x.database_facade.delete_contact_request_where_x_is_y = MagicMock()
        pop.return_value = 'invalid'
        result = self.x.received_request_treeview_clicked(None)
        target.assert_called_with('nonce', sub2().nonce)

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_deletes_record_if_popup_returns_reject(self,  pop, controller):
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock()
        sub2 = self.x.database_facade.fetch_one_contact_request_by_nonce = MagicMock()
        target = self.x.database_facade.delete_contact_request_where_x_is_y = MagicMock()
        pop.return_value = 'reject'
        result = self.x.received_request_treeview_clicked(None)
        target.assert_called_with('nonce', sub2().nonce)

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_updates_record_if_popup_returns_accept(self,  pop, controller):
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock()
        sub2 = self.x.database_facade.fetch_one_contact_request_by_nonce = MagicMock()
        sub3 = self.x.contact_response_client_send = MagicMock()
        target = self.x.database_facade.update_contact_request_col_to_val_where_x_is_y = MagicMock()
        pop.return_value = 'accept'
        result = self.x.received_request_treeview_clicked(None)
        target.assert_called_with('status', 'accept', 'nonce', sub2().nonce)

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_received_request_treeview_clicked_updates_treeview_if_popup_not_none(self,  pop, controller):
        val = 'xxx'
        db_val = 'yyy'
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock(return_value=val)
        target = self.x.update_received_requests_treeview = MagicMock()
        pop.return_value = 'xxxx'
        result = self.x.received_request_treeview_clicked(None)
        target.assert_called_with()

    @patch.object(requestscontroller.popuplauncher, 'ContactRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_contactrequest_popup')
    def test_peers_treeview_clicked_calls_contact_response_client_send_if_popup_returns_accept(self,  pop, controller):
        db_val = MagicMock()
        sub = self.x.view.get_clicked_received_request_treeview_nonce = MagicMock()
        sub2 = self.x.database_facade.fetch_one_contact_request_by_nonce = MagicMock(return_value=db_val)
        pop.return_value = 'accept'
        target = self.x.contact_response_client_send = MagicMock()
        result = self.x.received_request_treeview_clicked(None)
        target.assert_called_with(sub2.return_value)

    ###############################################
    #  build_contact_response_dict TESTS          #
    ###############################################

    def test_build_contact_response_dict_returns_false_if_tor_message_proxy_addr_is_not_onion(self):
        tmp_arg = 'xxx'
        sub = self.x.tor_datacontext.get_tor_message_proxy_addr = MagicMock(return_value=tmp_arg)
        tmp_rec = MagicMock()
        result = self.x.build_contact_response_dict(tmp_rec)
        self.assertIs(result, False)

    @patch.object(requestscontroller.contactresponsefactory, 'ContactResponseFactory')
    def test_build_contact_response_dict_calls_contact_response_factory(self, target):
        tor_return = 'xxx.onion'
        tor_sub = self.x.tor_datacontext.get_tor_message_proxy_addr = MagicMock(return_value=tor_return)
        data_record = MagicMock()
        result = self.x.build_contact_response_dict(data_record)
        target.assert_called_with(tor_sub.return_value, self.x.gpg_homedir_observer.get(), data_record, self.root_params.get_session_passphrase_observable())

    @patch.object(requestscontroller.contactresponsefactory, 'ContactResponseFactory')
    def test_build_contact_response_dict_calls_build_on_contact_response_factory(self, target):
        target.return_value = MagicMock()
        tor_return = 'xxx.onion'
        tor_sub = self.x.tor_datacontext.get_tor_message_proxy_addr = MagicMock(return_value=tor_return)
        data_record = MagicMock()
        result = self.x.build_contact_response_dict(data_record)
        self.assertTrue(target.return_value.build.called)

    @patch.object(requestscontroller.contactresponsefactory, 'ContactResponseFactory')
    def test_build_contact_response_dict_returns_build_result_on_valid_factory(self, target):
        build_result = 'xxxxxx'
        class MockValid(MagicMock):
            valid = True
            def build(self):
                return build_result

        target.return_value = MockValid()
        tor_return = 'xxx.onion'
        tor_sub = self.x.tor_datacontext.get_tor_message_proxy_addr = MagicMock(return_value=tor_return)
        data_record = MagicMock()
        result = self.x.build_contact_response_dict(data_record)
        self.assertEqual(result, build_result)

    @patch.object(requestscontroller.contactresponsefactory, 'ContactResponseFactory')
    def test_build_contact_response_dict_returns_false_on_NOT_valid_factory(self, target):
        build_result = 'xxxxxx'

        class MockValid(MagicMock):
            valid = False

            def build(self):
                return build_result

        target.return_value = MockValid()
        tor_return = 'xxx.onion'
        tor_sub = self.x.tor_datacontext.get_tor_message_proxy_addr = MagicMock(return_value=tor_return)
        data_record = MagicMock()
        result = self.x.build_contact_response_dict(data_record)
        self.assertIs(result, False)

    ###############################################
    #  contact_response_client_send TESTS         #
    ###############################################

    def test_contact_response_client_send_calls_alert_returns_none_if_build_contact_response_dict_returns_false(self):
        data_rec = MagicMock()
        alert_targ = self.x.launch_alert_log = MagicMock()
        self.x.build_contact_response_dict = MagicMock(return_value=False)
        result = self.x.contact_response_client_send(data_rec)
        self.assertIsNone(result)
        self.assertTrue(alert_targ.called)

    def test_contact_response_client_send_calls_client_controller_with_correct_args(self):
        class MockData:
            address_host = 'host'
            address_port = '123'
            ssl_key = 'ssl_key'
            nonce = 'nonce_string'
            _fields = 'mocked attribute'
        data_record = MockData()
        tmp_return = (dict(), 'nonce_string')
        sub = self.x.build_contact_response_dict = MagicMock(return_value=tmp_return)

        argnamespace = types.SimpleNamespace(host=data_record.address_host,
                                       port=int(data_record.address_port),
                                       queue=self.x.root_queue,
                                       payload_dict=sub.return_value[0],
                                       nonce=sub.return_value[1],
                                       request_nonce=data_record.nonce,
                                       command='RES')

        target = requestscontroller.clientcontroller.ClientController = MagicMock()
        result = self.x.contact_response_client_send(data_record)
        target.assert_called_with('contact_response', argnamespace)

    ###############################################
    #  SENT REQUEST TREEVIEW CLICKED METHOD TESTS #
    ###############################################

    @patch.object(requestscontroller.popuplauncher, 'DisplaySentRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_display_sent_request_popup')
    def test_sent_request_treeview_clicked_calls_get_nonce_on_view(self, pop, controller):
        target = self.x.view.get_clicked_sent_request_treeview_vals = MagicMock()
        self.x.sent_request_treeview_clicked(None)
        target.assert_called_with()

    @patch.object(requestscontroller.popuplauncher, 'DisplaySentRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_display_sent_request_popup')
    def test_sent_request_treeview_clicked_returns_none_if_vals_are_none(self, pop, controller):
        target = self.x.view.get_clicked_sent_request_treeview_vals = MagicMock(return_value=None)
        result = self.x.sent_request_treeview_clicked(None)
        self.assertIsNone(result)

    @patch.object(requestscontroller.popuplauncher, 'DisplaySentRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_display_sent_request_popup')
    def test_sent_request_treeview_clicked_fetches_db_record_by_fingerprint(self, pop, controller):
        vals = ('xxx', 'yyy')
        sub = self.x.view.get_clicked_sent_request_treeview_vals = MagicMock(return_value=vals)
        target = self.x.database_facade.fetch_contact_response_pub_key_by_fingerprint = MagicMock()
        result = self.x.sent_request_treeview_clicked(None)
        target.assert_called_with(sub.return_value[1])


    @patch.object(requestscontroller.popuplauncher, 'DisplaySentRequestController')
    @patch.object(requestscontroller.popuplauncher, 'launch_display_sent_request_popup')
    def test_sent_request_treeview_clicked_launches_display_sent_request_request_popup_with_addr_and_fingerprint(self,  pop, controller):
        vals = ('xxx', 'yyy')
        db_val = 'yyy'
        sub = self.x.view.get_clicked_sent_request_treeview_vals = MagicMock(return_value=vals)
        sub2 = self.x.database_facade.fetch_contact_response_pub_key_by_fingerprint = MagicMock(return_value=db_val)
        result = self.x.sent_request_treeview_clicked(None)
        pop.assert_called_with(self.x.root, sub2.return_value, sub.return_value[0])





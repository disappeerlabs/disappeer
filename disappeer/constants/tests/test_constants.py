"""
test_constants.py

Test suite for the constants module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
import constants.constants as constants
import collections
import sys
import os


class TestImports(unittest.TestCase):

    def test_collections(self):
        self.assertEqual(collections, constants.collections)

    def test_sys(self):
        self.assertEqual(sys, constants.sys)

    def test_os(self):
        self.assertEqual(os, constants.os)


class TestBasicConstants(unittest.TestCase):

    def setUp(self):
        self.title = "Disappeer"

    def test_displayimages(self):
        target = bool()
        self.assertIsInstance(constants.display_images, type(target))

    def test_displayimages_by_platform(self):
        if sys.platform == 'darwin':
            self.assertFalse(constants.display_images)
        elif os.environ.get('TESTING'):
            self.assertFalse(constants.display_images)
        else:
            self.assertTrue(constants.display_images)

    def test_display_images_false_if_test_flag_set(self):
        os.environ['TESTING'] = '1'
        self.assertIs(constants.display_images, False)

    def test_title(self):
        self.assertEqual(self.title, constants.title)

    def test_key_info_ordered_field_labels(self):
        target = ('uids', 'fingerprint', 'keyid', 'date', 'expires', 'length', 'trust', 'ownertrust', 'type', 'algo', 'subkeys', 'dummy')
        self.assertEqual(target, constants.key_info_ordered_field_labels)

    def test_new_key_ordered_field_labels(self):
        target = ("Name", "Email", "Comment", "Key Length", "Key Type", "Key Usage", "Subkey Type", "Subkey Length", "Expire Date", "Passphrase")
        self.assertEqual(target, constants.new_key_ordered_field_labels)

    def test_new_key_default_vals_dict(self):
        # Default values for the New Key Form labels and entries
        new_key_default_vals_dict = {
                    "Name": "Mallory",
                    "Email": "mallory@email.com",
                    "Comment": "Default comment message",
                    "Key Length": "2048",
                    "Key Type": "RSA",
                    "Key Usage": "",
                    "Subkey Type": "ELG-E",
                    "Subkey Length": "2048",
                    "Expire Date": "2028-04-01",
                    "Passphrase": "passphrase"
                }
        self.assertEqual(new_key_default_vals_dict, constants.new_key_default_vals_dict)

    def test_new_key_input_dict(self):

        # Dictionary mapping new key field labels to the proper input names for key generation
        new_key_input_dict = {
                    "Name": "name_real",
                    "Email": "name_email",
                    "Comment": "name_comment",
                    "Key Length": "key_length",
                    "Key Type": "key_type",
                    "Key Usage": "key_usage",
                    "Subkey Type": "subkey_type",
                    "Subkey Length": "subkey_length",
                    "Expire Date": "expire_date",
                    "Passphrase": "passphrase"
                    }
        self.assertEqual(new_key_input_dict, constants.new_key_input_dict)

    def test_command_list_named_tuple_objs(self):
        self.assertEqual(type(constants.command_list_inputs), type(list()))
        for item in constants.command_list_inputs:
            self.assertIn(item, dir(constants.command_list_tuple_obj))
            self.assertIn(item, dir(constants.command_list))

    def test_command_list_create_new_key(self):
        txt = "Create_New_Key"
        self.assertEqual(constants.command_list.Create_New_Key, txt)

    def test_command_list_check_sanity(self):
        txt = "Check_Sanity"
        self.assertEqual(constants.command_list.Check_Sanity, txt)

    def test_command_list_new_contact_request(self):
        txt = 'New_Contact_Req'
        self.assertEqual(constants.command_list.New_Contact_Req, txt)

    def test_command_list_new_contact_request_client_err(self):
        txt = 'New_Contact_Req_Client_Err'
        self.assertEqual(constants.command_list.New_Contact_Req_Client_Err, txt)

    def test_command_list_new_contact_request_client_res(self):
        txt = 'New_Contact_Req_Client_Res'
        self.assertEqual(constants.command_list.New_Contact_Req_Client_Res, txt)

    def test_command_list_new_contact_response(self):
        txt = 'New_Contact_Res'
        self.assertEqual(constants.command_list.New_Contact_Res, txt)

    def test_command_list_new_contact_response_client_err(self):
        txt = 'New_Contact_Res_Client_Err'
        self.assertEqual(constants.command_list.New_Contact_Res_Client_Err, txt)

    def test_command_list_new_contact_response_client_res(self):
        txt = 'New_Contact_Res_Client_Res'
        self.assertEqual(constants.command_list.New_Contact_Res_Client_Res, txt)

    def test_command_list_send_new_message(self):
        txt = 'Send_New_Message'
        self.assertEqual(constants.command_list.Send_New_Message, txt)

    def test_command_list_send_new_message_client_error(self):
        txt = 'Send_New_Message_Client_Err'
        self.assertEqual(constants.command_list.Send_New_Message_Client_Err, txt)

    def test_command_list_send_new_message_client_response(self):
        txt = 'Send_New_Message_Client_Res'
        self.assertEqual(constants.command_list.Send_New_Message_Client_Res, txt)

    def test_command_list_received_new_message(self):
        txt = 'Received_New_Message'
        self.assertEqual(constants.command_list.Received_New_Message, txt)

    def test_command_list_tor_proxy_request_server(self):
        txt = 'Tor_Proxy_Request_Server'
        self.assertEqual(constants.command_list.Tor_Proxy_Request_Server, txt)

    def test_command_list_tor_proxy_response_server(self):
        txt = 'Tor_Proxy_Response_Server'
        self.assertEqual(constants.command_list.Tor_Proxy_Response_Server, txt)

    def test_command_list_tor_proxy_message_server(self):
        txt = 'Tor_Proxy_Message_Server'
        self.assertEqual(constants.command_list.Tor_Proxy_Message_Server, txt)

    def test_command_list_server_error(self):
        txt = 'Server_Error'
        self.assertEqual(constants.command_list.Server_Error, txt)

    def test_command_list_tor_proxy_error(self):
        txt = 'Tor_Proxy_Error'
        self.assertEqual(constants.command_list.Tor_Proxy_Error, txt)

    def test_command_list_inspect_message(self):
        txt = 'Inspect_Message'
        self.assertEqual(constants.command_list.Inspect_Message, txt)





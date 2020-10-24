"""
constants.py

Root level programmatic constants

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import collections
import sys
import os


title = "Disappeer"

if sys.platform == 'darwin':
    display_images = False
elif os.environ.get('TESTING'):
    display_images = False
else:
    display_images = True

# To add a new constant to the command list, add string to inputs
command_list_inputs = ['Check_Sanity',
                       'Create_New_Key',
                       'New_Contact_Req',
                       'New_Contact_Req_Client_Err',
                       'New_Contact_Req_Client_Res',
                       'New_Contact_Res',
                       'New_Contact_Res_Client_Err',
                       'New_Contact_Res_Client_Res',
                       'Send_New_Message',
                       'Send_New_Message_Client_Err',
                       'Send_New_Message_Client_Res',
                       'Received_New_Message',
                       'Tor_Proxy_Request_Server',
                       'Tor_Proxy_Response_Server',
                       'Tor_Proxy_Message_Server',
                       'Server_Error',
                       'Tor_Proxy_Error',
                       'Inspect_Message']
command_list_tuple_obj = collections.namedtuple("Command_List", command_list_inputs)
command_list = command_list_tuple_obj(*command_list_inputs)


# Key Info ordered field labels
key_info_ordered_field_labels = ('uids', 'fingerprint', 'keyid', 'date', 'expires', 'length', 'trust', 'ownertrust', 'type', 'algo', 'subkeys', 'dummy')

# New Key ordered field labels
new_key_ordered_field_labels = ("Name", "Email", "Comment", "Key Length", "Key Type", "Key Usage", "Subkey Type", "Subkey Length", "Expire Date", "Passphrase")

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
"""
settings.py

App Level settings

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import os
import pathlib


if os.environ.get('TESTING'):
    root_data_dir = os.path.abspath('tests/data/root_data_dir_test') + '/'
else:
    root_data_dir_name = '/.disappeer/'
    root_data_dir = str(pathlib.Path.home()) + root_data_dir_name

default_key_dir = root_data_dir + 'keys'
default_log_dir = root_data_dir + 'log/'

port_contact_request_server = 16661
port_contact_response_server = 16662
port_message_server = 16663
port_tor_controller = 9051

gpg_host_pubkey = root_data_dir + 'host_gpg_pubkey.gpg'





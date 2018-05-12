"""
test_settings.py

Test Suite for the app level settings file

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer import settings
import os


class TestImports(unittest.TestCase):

    def test_os(self):
        self.assertEqual(os, settings.os)


class TestBasicVars(unittest.TestCase):

    def test_port_contact_request_server(self):
        target = 16661
        self.assertEqual(target, settings.port_contact_request_server)

    def test_port_contact_response_server(self):
        target = 16662
        self.assertEqual(target, settings.port_contact_response_server)

    def test_port_message_server(self):
        target = 16663
        self.assertEqual(target, settings.port_message_server)

    def test_port_tor_controller(self):
        target = 9051
        self.assertEqual(target, settings.port_tor_controller)

    def test_gpg_host_pubkey_file(self):
        name = 'host_gpg_pubkey.gpg'
        target = settings.root_data_dir + name
        self.assertEqual(target, settings.gpg_host_pubkey)

    def test_root_data_dir(self):
        name = 'root_data_dir'
        check = hasattr(settings, name)
        self.assertEqual(type('t'), type(settings.root_data_dir))
        self.assertEqual(settings.root_data_dir[-1], '/')
        import pathlib
        self.assertIn(str(pathlib.Path.home()), settings.root_data_dir)

    def test_default_key_dir_exists_is_dir(self):
        name = 'default_key_dir'
        check = hasattr(settings, name)
        self.assertEqual(settings.default_key_dir, settings.root_data_dir + 'keys')

    def test_default_log_dir_exists_is_dir(self):
        name = 'default_log_dir'
        check = hasattr(settings, name)
        self.assertEqual(settings.default_log_dir, settings.root_data_dir + 'log/')
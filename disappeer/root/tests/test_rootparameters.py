"""
test_rootparameters.py

Test suite for RootParameters class object and module, containing primary root params of root controller.
To be passed in to the other controllers.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.root import rootparameters
import tkinter
from disappeer.utilities import observable

class TestImports(unittest.TestCase):

    def test_observable(self):
        self.assertEqual(observable, rootparameters.observable)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.root_view = MagicMock()
        self.root_queue = MagicMock()
        self.database_facade = MagicMock()
        self.key_text = 'xxx,yyy,zzz'
        self.host_key_observer = observable.Observable(self.key_text)
        self.x = rootparameters.RootParameters(self.root, self.root_view, self.root_queue, self.database_facade, self.host_key_observer)

    def test_instance(self):
        self.assertIsInstance(self.x, rootparameters.RootParameters)

    def test_root_attr(self):
        self.assertEqual(self.x.root, self.root)

    def test_root_view_attr(self):
        self.assertEqual(self.x.root_view, self.root_view)

    def test_root_queue_attr(self):
        self.assertEqual(self.x.root_queue, self.root_queue)

    def test_root_database_facade_attr(self):
        self.assertEqual(self.x.database_facade, self.database_facade)

    def test_host_key_observer_attr(self):
        self.assertEqual(self.x.host_key_observer, self.host_key_observer)

    def test_tor_proxy_running_observable_attr_set_false(self):
        self.assertIsInstance(self.x.tor_proxy_running_observable, observable.Observable)
        self.assertIs(self.x.tor_proxy_running_observable.get(), False)

    def test_host_key_session_passphrase_observable_attr_set(self):
        self.assertIsInstance(self.x.host_key_session_passphrase_observable, observable.Observable)

    def test_get_tor_net_frame_returns_tor_net_frame(self):
        target = self.x.root_view.left_panel.tor_net_frame
        result = self.x.get_tor_net_frame()
        self.assertEqual(result, target)

    def test_get_requests_frame_returns_requests_frame(self):
        target = self.x.root_view.left_panel.requests_frame
        result = self.x.get_requests_frame()
        self.assertEqual(result, target)

    def test_get_gpg_frame_returns_gpg_frame(self):
        target = self.x.root_view.left_panel.gpg_frame
        result = self.x.get_gpg_frame()
        self.assertEqual(result, target)

    def test_get_messages_frame_returns_messages_frame(self):
        target = self.x.root_view.left_panel.messages_frame
        result = self.x.get_messages_frame()
        self.assertEqual(result, target)

    def test_get_console_frame_returns_console_frame(self):
        target = self.x.root_view.right_panel.console_frame
        result = self.x.get_console_frame()
        self.assertEqual(result, target)

    def test_get_root_menubar(self):
        result = self.x.get_root_menubar()
        self.assertEqual(result, self.root_view.root_menubar)

    def test_get_app_menu_obj_returns_correct_menu_obj(self):
        result = self.x.get_app_menu_obj()
        self.assertEqual(result, self.x.root_view.app_menu)

    def test_get_file_menu_obj_returns_correct_menu_obj(self):
        result = self.x.get_file_menu_obj()
        self.assertEqual(result, self.x.root_view.file_menu)

    def test_get_gpg_menu_obj_returns_correct_menu_obj(self):
        result = self.x.get_gpg_menu_obj()
        self.assertEqual(result, self.x.root_view.gpg_menu)

    def test_get_host_key_id_gets_host_key_id(self):
        key_vals = self.x.host_key_observer.get()
        split = key_vals.split(',')
        key_id = split.pop().strip()
        result = self.x.get_host_key_id()
        self.assertEqual(result, key_id)

    def test_set_tor_proxy_observable_sets_observable(self):
        val = True
        result = self.x.set_tor_proxy_running_observable(True)
        self.assertIs(self.x.tor_proxy_running_observable.get(), val)

    def test_get_tor_proxy_observable_is_current_val(self):
        val = 'xxx'
        self.x.tor_proxy_running_observable.set(val)
        result = self.x.get_tor_proxy_running_observable()
        self.assertEqual(result, val)

    def test_set_session_passphrase_observable_sets_observable(self):
        val = True
        result = self.x.set_session_passphrase_observable(True)
        self.assertIs(self.x.host_key_session_passphrase_observable.get(), val)

    def test_get_session_passphrase_observable_gets_observable(self):
        val = 'xxx'
        self.x.host_key_session_passphrase_observable.set(val)
        result = self.x.get_session_passphrase_observable()
        self.assertEqual(result, val)

    def test_add_session_passphrase_observable_callback_adds_callback(self):
        def hello():
            pass

        self.x.add_session_passphrase_observable_callback(hello)
        self.assertIn(hello, self.x.host_key_session_passphrase_observable.callbacks)

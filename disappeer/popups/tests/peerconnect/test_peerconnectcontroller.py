"""
test_peerconnectcontroller.py

Test suite for PeerConnectController popup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.peerconnect import peerconnectcontroller
from disappeer.popups.peerconnect import peerconnectview
from disappeer.popups.bases import basepopupcontroller
import tkinter


class TestImports(unittest.TestCase):

    def test_peerconnectview(self):
        self.assertEqual(peerconnectview, peerconnectcontroller.peerconnectview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, peerconnectcontroller.basepopupcontroller)

    def test_tkinter(self):
        self.assertEqual(tkinter, peerconnectcontroller.tkinter)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.x = peerconnectcontroller.PeerConnectController(self.root)

    def test_instance(self):
        self.assertIsInstance(self.x, peerconnectcontroller.PeerConnectController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_root_attribute(self):
        self.assertEqual(self.root, self.x.root)

    def test_title_attribute_set(self):
        target = 'Peer Connect'
        self.assertEqual(target, self.x.title)

    def test_view_attribute(self):
        self.assertIsInstance(self.x.view, peerconnectview.PeerConnectView)

    def test_view_window_attribute(self):
        self.assertEqual(self.x.window, self.x.view.window)

    def test_config_event_bindings_calls_bind_on_cancel_button(self):
        self.x.view = MagicMock()
        self.x.view.cancel_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.cancel_button.bind.called)

    @patch.object(peerconnectcontroller.PeerConnectController, 'config_event_bindings')
    def test_config_event_bindings_method_called_by_constructor(self, mocked):
        x = peerconnectcontroller.PeerConnectController(self.root)
        self.assertTrue(mocked.called)

    def test_config_event_bindings_calls_bind_on_connect_button(self):
        self.x.view = MagicMock()
        self.x.view.connect_button = MagicMock()
        self.x.config_event_bindings()
        self.assertTrue(self.x.view.connect_button.bind.called)

    def test_connect_button_calls_set_output_and_close_with_host_port_tuple(self):
        host = 'host'
        port = 'port'
        self.x.view.host_entry_var.get = MagicMock(return_value=host)
        self.x.view.port_entry_var.get = MagicMock(return_value=port)
        target = self.x.set_output_and_close = MagicMock()
        self.x.connect_button_clicked(None)
        target.assert_called_with((host, port))


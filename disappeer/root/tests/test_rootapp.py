"""
test_rootapp.py

Tests for RootApp class module


Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import sys 
import tkinter
import logging
import unittest
from argparse import Namespace
from unittest.mock import patch, MagicMock
from disappeer.root.rootapp import RootApp
from disappeer.root import rootcontroller
from disappeer import metainfo



class TestAppClass(unittest.TestCase):

    @patch.object(rootcontroller, 'RootController')
    def setUp(self, patch_controller):
        self.patch_controller = patch_controller
        arg_obj = Namespace()
        arg_obj.home_dir = 'HELLO_HOME_DIR_ARG'
        self.args = arg_obj
        self.x = RootApp(self.args)
        self.x.root.mainloop = MagicMock()

    def test_title_attribute(self):
        name = 'title'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_title_attribute_set(self):
        self.assertEqual(self.x.title, metainfo.title)

    def test_args_attribute(self):
        name = 'args'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_args_attribute_set(self):
        self.assertEqual(self.x.args, self.args)

    def test_config_logger_method_configs_logger(self):
        check = logging.getLogger(metainfo.title)
        self.x.config_logger()
        self.assertEqual(check, self.x.log)
        self.assertEqual(sys.excepthook, self.x.log.handle_uncaught_system_exception)
        self.assertEqual(self.x.root.report_callback_exception, self.x.log.handle_uncaught_tkinter_exception)

    def test_config_exit_protocol_configs(self):
        target = self.x.root.protocol = MagicMock()
        self.x.config_exit_protocol()
        target.assert_called_with("WM_DELETE_WINDOW", self.x.root_controller.exit)

    def test_root_attribute(self):
        name = 'root'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_root_is_tk_obj(self):
        self.assertIsInstance(self.x.root, tkinter.Tk)

    def test_run_attribute(self):
        name = 'run'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_run_calls_tk_mainloop(self):
        self.x.root.mainloop = MagicMock()
        self.x.run()
        self.assertTrue(self.x.root.mainloop.called)

    def test_controller_attribute(self):
        name = 'root_controller'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_controller_is_controller(self):
        self.assertEqual(self.x.root_controller, self.patch_controller())

    def test_root_controller_has_correct_args(self):
        self.patch_controller.assert_called_with(self.x.args, self.x.root)

    # TODO: enable this test to add logo configuration
    # def test_config_logo_method_sets_icon(self):
    #     self.x.config_logo()

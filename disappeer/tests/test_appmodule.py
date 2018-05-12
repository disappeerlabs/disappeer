"""
test_appmodule.py

Test suite for the disappeer root app module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
import disappeer
from disappeer.constants import constants
import logging
from disappeer.utilities import logger
import tkinter
from disappeer.root import rootcontroller
import sys
from disappeer.utilities import dirmaker
from disappeer.root import rootview
from disappeer import settings
from disappeer.models import gpgdatacontext
from disappeer.models.db import databasefacade
from disappeer.models import tordatacontext
log = logging.getLogger(constants.title)
from disappeer import __main__


class TestImports(unittest.TestCase):

    def test_constants(self):
        self.assertEqual(constants, __main__.constants)

    def test_logger(self):
        self.assertEqual(logger, __main__.logger)

    def test_tkinter(self):
        self.assertEqual(tkinter, __main__.tkinter)

    def test_controller(self):
        self.assertEqual(rootcontroller, __main__.rootcontroller)

    def test_sys(self):
        self.assertEqual(sys, __main__.sys)

    def test_dirmaker(self):
        self.assertEqual(dirmaker, __main__.dirmaker)

    def test_rootview(self):
        self.assertEqual(rootview, __main__.rootview)

    def test_settings(self):
        self.assertEqual(settings, __main__.settings)

    def test_gpgdatacontext(self):
        self.assertEqual(gpgdatacontext, __main__.gpgdatacontext)

    def test_databasefacade(self):
        self.assertEqual(databasefacade, __main__.databasefacade)

    def test_tordatacontext(self):
        self.assertEqual(tordatacontext, __main__.tordatacontext)


class TestAppClass(unittest.TestCase):
    content = ''

    @classmethod
    def save_gpg_key(cls):
        with open(settings.gpg_host_pubkey, 'r') as f:
            content = f.read()
        return content

    @classmethod
    def write_gpg_key(cls, content):
        with open(settings.gpg_host_pubkey, 'w') as f:
            f.write(content)

    @classmethod
    def setUpClass(cls):
        """
        App module setup deletes contents of gpg host key.
        Save it, then write it back on del
        """
        cls.content = cls.save_gpg_key()

    @classmethod
    def tearDownClass(cls):
        cls.write_gpg_key(cls.content)

    @patch.object(rootcontroller, 'RootController')
    @patch.object(rootview, 'RootView')
    def setUp(self, patch_view, patch_controller):
        self.patch_view = patch_view
        self.patch_controller = patch_controller
        self.x = __main__.App()

    def altsetup(self):
        self.x = __main__.App()

    def test_setup_with_no_patches_runs_without_error(self):
        self.altsetup()

    def test_instance(self):
        self.assertIsInstance(self.x, __main__.App)

    def test_title_attribute(self):
        name = 'title'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_title_attribute_set(self):
        self.assertEqual(self.x.title, constants.title)

    def test_config_logger_method_configs_logger(self):
        check = logging.getLogger(constants.title)
        self.x.config_logger()
        self.assertEqual(check, self.x.log)
        self.assertEqual(sys.excepthook, self.x.log.handle_uncaught_system_exception)
        self.assertEqual(self.x.root.report_callback_exception, self.x.log.handle_uncaught_tkinter_exception)

    def test_config_logo_method_sets_icon(self):
        self.x.config_logo()

    def test_config_exit_protocol_configs(self):
        target = self.x.root.protocol = MagicMock()
        self.x.config_exit_protocol()
        target.assert_called_with("WM_DELETE_WINDOW", self.x.controller.exit)

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
        name = 'controller'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_controller_is_controller(self):
        self.assertEqual(self.x.controller, self.patch_controller())

    def test_root_view_is_root_view(self):
        self.assertEqual(self.x.root_view, self.patch_view())

    def test_root_controller_has_correct_args(self):
        self.patch_controller.assert_called_with(self.x.root,
                                                 self.x.root_view,
                                                 self.x.gpg_datacontext,
                                                 self.x.database_facade,
                                                 self.x.tor_datacontext)

    def test_dir_maker_attr_set(self):
        self.assertEqual(self.x.dir_maker.root_dir, settings.root_data_dir)
        self.assertIsInstance(self.x.dir_maker, dirmaker.DirMaker)

    def test_gpg_datacontext_attr_instance(self):
        self.assertIsInstance(self.x.gpg_datacontext, gpgdatacontext.GPGDataContext)

    def test_gpg_datacontext_called_with_settings_key_default(self):
        self.assertEqual(settings.default_key_dir, self.x.gpg_datacontext.key_home_path)

    def test_database_facade_is_database_facade_with_args(self):
        self.assertIsInstance(self.x.database_facade, databasefacade.DatabaseFacade)
        self.assertEqual(self.x.database_facade.host_key_observer, self.x.gpg_datacontext.host_key_observer)
        self.assertEqual(self.x.database_facade.get_user_database_dir_method, self.x.dir_maker.get_user_database_dir)

    def test_tor_datacontext_attr_is_tor_datacontect_with_arg(self):
        self.assertIsInstance(self.x.tor_datacontext, tordatacontext.TorDataContext)
        self.assertEqual(self.x.tor_datacontext.get_user_tor_keys_dir_method, self.x.dir_maker.get_user_tor_keys_dir)


class TestMainFunction(unittest.TestCase):

    @patch.object(__main__, 'App')
    def test_main_function_inits_app(self, target):
        __main__.main()
        target.assert_called_with()

    @patch.object(__main__.App, 'run')
    def test_main_function_runs_app(self, target):
        __main__.main()
        target.assert_called_with()



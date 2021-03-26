"""
test_main.py

Test main run file, parse_args and main functions

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import sys 
import unittest
import tempfile
from argparse import Namespace
from unittest.mock import patch, MagicMock
from disappeer import __main__
from disappeer.root import rootapp 


class TestParseArgs(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = tempfile.TemporaryDirectory()
    
    @classmethod
    def tearDownClass(cls):
        cls.tmp_dir.cleanup()

    def setUp(self):
        self.target_func = __main__.parse_args

    def test_parse_args_returns_namespace(self):
        self.assertIsInstance(self.target_func([]), Namespace)

    def test_directory_argument(self):
        args = ['--home_dir', self.tmp_dir.name]
        result = self.target_func(args)
        self.assertEqual(result.home_dir, self.tmp_dir.name)


class TestMainFunction(unittest.TestCase):
    
    def setUp(self):
        self.target_func = __main__.main
    
    @patch('disappeer.__main__.parse_args')
    def test_main_calls_parse_args_with_sysv_args(self, parse_args_patch):
        testargs = [1, 2, 3]
        with patch.object(sys, 'argv', testargs):
            o = self.target_func()
            parse_args_patch.assert_called_with(testargs[1:])

    @patch('disappeer.__main__.RootApp')
    def test_main_calls_root_app_with_parsed_args(self, patch_root_app):
        val = [1, 2, 3, 4]
        with patch.object(__main__, 'parse_args') as m1:
            m1.return_value = val
            self.target_func()
            patch_root_app.assert_called_with(val)

    @patch('disappeer.__main__.RootApp.run')
    def test_main_calls_run_on_root_app(self, patch_root_app_run):
        val = [1, 2, 3, 4]
        with patch.object(__main__, 'parse_args') as m1:
            m1.return_value = val
            self.target_func()
            patch_root_app_run.assert_called_with()


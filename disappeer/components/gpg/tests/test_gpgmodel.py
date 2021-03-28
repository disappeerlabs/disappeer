"""
test_gpgmodel.py

Tests for GPG data model
"""

import unittest
from unittest.mock import MagicMock
import tempfile
from disappeer.__main__ import parse_args
from dptools.tkcomponents.baseapp import basemodel
from disappeer.components.gpg import gpgmodel
from dptools.utilities import observable 




class TestGPGModelBasic(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        arg_list = ['--home_dir', self.temp_dir.name]
        self.args = parse_args(arg_list)
        self.mock_root = MagicMock()
        self.mock_queue = MagicMock()
        self.x = gpgmodel.GPGModel(args=self.args, root=self.mock_root, queue=self.mock_queue)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_kwargs_set(self):
        self.assertEqual(self.x.root, self.mock_root)
        self.assertEqual(self.x.args, self.args)
        self.assertEqual(self.x.queue, self.mock_queue)

    def test_subclass(self):
        self.assertIsInstance(self.x, basemodel.BaseModel)

    def test_instance(self):
        self.assertIsInstance(self.x,  gpgmodel.GPGModel)

    def test_home_dir_attribute(self):
        self.assertEqual(self.args.home_dir, self.x.home_dir)

    def test_home_dir_observable_attribute(self):
        name = 'home_dir_observable'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_config_home_dir_observable_method(self):
        result = self.x.config_home_dir_observable()
        self.assertIsInstance(result, observable.Observable)

    def test_config_home_dir_observable_calls_set_permissions_on_home_dir_path(self):
        target = self.x.set_permissions = MagicMock()
        result = self.x.config_home_dir_observable()
        target.assert_called_with(self.x.home_dir)

    def test_config_home_dir_observable_method_sets_home_dir(self):
        result = self.x.config_home_dir_observable()
        target = self.x.home_dir
        check = result.get()
        self.assertEqual(target, check)

    def test_home_dir_attribute_equals_result_config_home_dir_observable(self):
        result = self.x.config_home_dir_observable()
        target = result.get()
        check = self.x.home_dir_observable.get()
        self.assertEqual(target, check)

    def test_add_home_dir_observer_adds_observer_to_home_dir_observable(self):
        sub = MagicMock()
        self.x.add_home_dir_observer(sub)
        self.assertIn(sub, self.x.home_dir_observable.observer_list)
    
    def test_set_home_dir_observable_sets_var(self):
        val = '1234yrth5'
        self.x.set_home_dir_observable(val)
        o = self.x.home_dir_observable.get()
        self.assertEqual(o, val)

    def test_get_home_dir_observable_gets_var(self):
        val = '1234yrth5'
        self.x.set_home_dir_observable(val)
        o = self.x.get_home_dir_observable()
        self.assertEqual(o, val)


"""
test_rootcontroller.py

Test cases for rootcontroller module and class
"""

import unittest
from unittest.mock import MagicMock
import tempfile
from disappeer.__main__ import parse_args
from disappeer.root import rootcontroller
from dptools.tkcomponents.baseapp import basepanelview, basecontroller
from disappeer.components.gpg import gpgcontroller


class TestRootController(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        arg_list = ['--home_dir', self.temp_dir.name]
        self.args = parse_args(arg_list)
        self.mock_root = MagicMock()
        self.x = rootcontroller.RootController(args=self.args, root=self.mock_root)
    
    def tearDown(self):
        self.temp_dir.cleanup()

    def test_args_attr_set(self):
        self.assertEqual(self.x.args, self.args)

    def test_root_attr_set(self):
        self.assertEqual(self.x.root, self.mock_root)

    def test_is_instance_base_controller(self):
        self.assertIsInstance(self.x, basecontroller.BaseController)

    def test_root_view_initialized(self):
        self.assertIsInstance(self.x.root_view, basepanelview.BasePanelView)

    def test_gpg_controller_initialized(self):
        self.assertIsInstance(self.x.gpg_controller, gpgcontroller.GPGController)

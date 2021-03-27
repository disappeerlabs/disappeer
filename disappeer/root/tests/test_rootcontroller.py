"""
test_rootcontroller.py

Test cases for rootcontroller module and class
"""

import unittest
from unittest.mock import MagicMock
from disappeer.__main__ import parse_args
from disappeer.root import rootcontroller
from dptools.tkcomponents.baseapp import basepanelview, basecontroller


class TestRootController(unittest.TestCase):

    def setUp(self):
        arg_list = ['--home_dir', 'hello-world']
        self.args = parse_args(arg_list)
        self.mock_root = MagicMock()
        self.x = rootcontroller.RootController(args=self.args, root=self.mock_root)
    
    def test_args_attr_set(self):
        self.assertEqual(self.x.args, self.args)

    def test_root_attr_set(self):
        self.assertEqual(self.x.root, self.mock_root)

    def test_is_instance_base_controller(self):
        self.assertIsInstance(self.x, basecontroller.BaseController)

    def test_root_view_initialized(self):
        self.assertIsInstance(self.x.root_view, basepanelview.BasePanelView)

"""
test_gpginit.py

Test initialization function for gpg component widget
"""


import unittest
from unittest.mock import MagicMock
from disappeer.components import gpg 
from disappeer.components.gpg import gpgcontroller


class TestGPGRegisterWidgetFunction(unittest.TestCase):

    def setUp(self):
        self.mock_root = MagicMock()
        self.mock_view_method = MagicMock()
        self.mock_model_method = MagicMock()
        self.x = gpg.register_widget(self.mock_root, self.mock_view_method, self.mock_model_method)
    
    def test_instance(self):
        self.assertIsInstance(self.x, gpgcontroller.GPGController)

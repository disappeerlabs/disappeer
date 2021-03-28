"""
test_gpgcontroller.py

Tests for GPG component widget controller
"""

import unittest
from unittest.mock import MagicMock
from disappeer.components.gpg import gpgcontroller


class TestBasics(unittest.TestCase):

    def setUp(self):
        self.mock_root = MagicMock()
        self.mock_view = MagicMock()
        self.mock_model = MagicMock()
        self.x = gpgcontroller.GPGController(self.mock_root, self.mock_view, self.mock_model)
    
    def test_instance(self):
        self.assertIsInstance(self.x, gpgcontroller.GPGController)
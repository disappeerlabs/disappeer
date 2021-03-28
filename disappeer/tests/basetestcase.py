"""
basetestcase.py

Base class for common test case setup

"""

import unittest
import tempfile


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()


    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

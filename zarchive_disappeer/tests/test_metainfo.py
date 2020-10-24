"""
test_metainfo.py

Test suite for app metainfo

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer import metainfo


class TestBasics(unittest.TestCase):

    def test_title(self):
        name = 'Disappeer'
        self.assertEqual(name, metainfo.title)

    def test_version(self):
        name = 'version'
        check = hasattr(metainfo, name)
        self.assertTrue(check)
        self.assertIsNotNone(metainfo.version)

    def test_license(self):
        name = 'license'
        check = hasattr(metainfo, name)
        self.assertTrue(check)
        self.assertIsNotNone(metainfo.license)

    def test_github(self):
        name = 'github'
        check = hasattr(metainfo, name)
        self.assertTrue(check)
        self.assertIsNotNone(metainfo.github)

    def test_email(self):
        name = 'email'
        check = hasattr(metainfo, name)
        self.assertTrue(check)
        self.assertIsNotNone(metainfo.email)


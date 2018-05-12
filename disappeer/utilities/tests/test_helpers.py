"""
test_helpers.py

Test suite for app utilities.helpers module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.utilities import helpers
import datetime
import os
import pathlib


class TestImports(unittest.TestCase):

    def test_datetime(self):
        self.assertEqual(datetime, helpers.datetime)

    def test_os(self):
        self.assertEqual(os, helpers.os)

    def test_pathlib(self):
        self.assertEqual(pathlib, helpers.pathlib)


class TestBasics(unittest.TestCase):

    def test_get_date_time_stamp(self):
        secs = '1495828561'
        target = '05/26/2017'
        result = helpers.get_date_time_stamp(secs)
        self.assertEqual(result, target)

    def test_get_local_ipaddress(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 53))
        check = s.getsockname()[0]
        s.close()
        result = helpers.get_local_ipaddress()
        self.assertEqual(check, result)

    def test_get_images_dir_path(self):
        from disappeer import images
        expected = os.path.dirname(images.__file__) + '/'
        actual = helpers.get_images_dir_path()
        self.assertEqual(expected, actual)

    def test_get_user_home_dir(self):
        self.assertEqual(pathlib.Path.home(), helpers.get_user_home_dir())


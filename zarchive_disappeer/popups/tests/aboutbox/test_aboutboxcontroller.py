"""
test_aboutboxcontroller.py

Test suite for the popup AboutBoxController module for the about info window

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups.aboutbox import aboutboxview
from disappeer.popups.bases import basepopupcontroller
from disappeer.popups.aboutbox import aboutboxcontroller
import tkinter


class TestImports(unittest.TestCase):

    def test_alertbox_view(self):
        self.assertEqual(aboutboxview, aboutboxcontroller.aboutboxview)

    def test_basecontroller(self):
        self.assertEqual(basepopupcontroller, aboutboxcontroller.basepopupcontroller)


class TestAboutBoxControllerClassBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.x = aboutboxcontroller.AboutBoxController(self.root)

    def test_instance(self):
        self.assertIsInstance(self.x, aboutboxcontroller.AboutBoxController)

    def test_instance_basecontroller(self):
        self.assertIsInstance(self.x, basepopupcontroller.BasePopupController)

    def test_title(self):
        name = "About"
        self.assertEqual(name, self.x.title)

    def test_config_event_bindings_attribute(self):
        name = 'config_event_bindings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_root_attribute_set(self):
        self.assertEqual(self.root, self.x.root)

    def test_view_attribute(self):
        self.assertIsInstance(self.x.view, aboutboxview.AboutBoxView)


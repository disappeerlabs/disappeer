"""
test_invoker.py

Test suite for command pattern invoker object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import executor.invoker as invoker


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.x = invoker.Invoker()

    def test_instance(self):
        self.assertIsInstance(self.x, invoker.Invoker)

    def test_invoker_has_class_execute_method_calls_execute_on_arg(self):
        cmd = MagicMock()
        invoker.Invoker.execute(cmd)
        cmd.execute.assert_called_with()

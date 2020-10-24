"""
test_threadmanagers.py

Test suite for ThreadManagers module, should contain class objects for:
    - AbstractThreadManager
    - ServerThreadManager
    - ClientThreadManager

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
import net.bases.threadmanagers as threadmanagers
import abc
import threading


class TestImports(unittest.TestCase):

    def test_abc(self):
        self.assertEqual(abc, threadmanagers.abc)

    def test_threading(self):
        self.assertEqual(threading, threadmanagers.threading)


class MockConcreteThreadManager(threadmanagers.AbstractThreadManager):

    def run_widget_command(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class TestAbstractThreadManagerClassBasics(unittest.TestCase):

    def setUp(self):
        self.mock_factory = MagicMock()
        self.x = MockConcreteThreadManager(self.mock_factory)

    def test_instance(self):
        self.assertIsInstance(self.x, threadmanagers.AbstractThreadManager)

    def test_metaclass_attribute(self):
        check = hasattr(self.x, '_abc_registry')
        self.assertTrue(check)

    def test_factory_attribute_set(self):
        self.assertEqual(self.x.factory, self.mock_factory)

    def test_widget_thread_attribute_none(self):
        self.assertIsNone(self.x.widget_thread)

    def test_widget_attribute_none(self):
        self.assertIsNone(self.x.widget)

    def test_start_method_calls_build_on_factory(self):
        val = MagicMock()
        sub = self.x.factory.build = MagicMock(return_value=val)
        sub1 = self.x.run_widget_command = MagicMock()
        self.x.start()
        sub.assert_called_with()

    @patch('threading.Thread')
    def test_start_method_sets_widget_attribute(self, mock_thread):
        val = MagicMock()
        sub = self.x.factory.build = MagicMock(return_value=val)
        self.x.start()
        self.assertEqual(self.x.widget, val)

    @patch('threading.Thread')
    def test_start_method_calls_thread(self, mock_thread):
        val = MagicMock()
        sub = self.x.factory.build = MagicMock(return_value=val)
        self.x.start()
        self.assertTrue(mock_thread.called)

    @patch('threading.Thread')
    def test_start_method_calls_thread_with_args(self, mock_thread):
        val = MagicMock()
        sub = self.x.factory.build = MagicMock(return_value=val)
        self.x.start()
        mock_thread.assert_called_with(target=self.x.run_widget_command, name=self.x.factory.name)

    @patch('threading.Thread')
    def test_start_method_sets_widget_thread_attribute(self, mock_thread):
        val = MagicMock()
        sub = self.x.factory.build = MagicMock(return_value=val)
        mock_thread.return_value = val
        self.x.start()
        self.assertEqual(self.x.widget_thread, mock_thread.return_value)

    @patch('threading.Thread')
    def test_start_method_sets_thread_damon_true(self, mock_thread):
        val = MagicMock()
        sub = self.x.factory.build = MagicMock(return_value=val)
        mock_thread.return_value = val
        self.x.start()
        self.assertEqual(self.x.widget_thread.daemon, True)

    @patch('threading.Thread')
    def test_start_method_calls_start_on_widget_thread(self, mock_thread):
        val = MagicMock()
        sub = self.x.factory.build = MagicMock(return_value=val)
        mock_thread.return_value = val
        target = mock_thread.start = MagicMock()
        self.x.start()
        self.assertTrue(self.x.widget_thread.start.called)

    def test_run_widget_command_method_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.x.run_widget_command()

    def test_stop_method_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.x.stop()


class TestServerThreadManager(unittest.TestCase):

    def setUp(self):
        self.mock_factory = MagicMock()
        self.x = threadmanagers.ServerThreadManager(self.mock_factory)

    def test_instance(self):
        self.assertIsInstance(self.x, threadmanagers.ServerThreadManager)

    def test_threadmanager_instance(self):
        self.assertIsInstance(self.x, threadmanagers.AbstractThreadManager)

    def test_run_widget_command_calls_serve_forever_on_widget(self):
        self.x.widget = MagicMock()
        target = self.x.widget.serve_forever = MagicMock()
        self.x.run_widget_command()
        self.assertTrue(target.called)

    def test_stop_method_calls_shutdown_and_server_close(self):
        self.x.widget = MagicMock()
        target = self.x.widget.shutdown = MagicMock()
        target1 = self.x.widget.server_close = MagicMock()
        self.x.stop()
        self.assertTrue(target.called)
        self.assertTrue(target1.called)


class TestClientThreadManager(unittest.TestCase):

    def setUp(self):
        self.mock_factory = MagicMock()
        self.x = threadmanagers.ClientThreadManager(self.mock_factory)

    def test_instance(self):
        self.assertIsInstance(self.x, threadmanagers.ClientThreadManager)

    def test_threadmanager_instance(self):
        self.assertIsInstance(self.x, threadmanagers.AbstractThreadManager)

    def test_run_widget_command_calls_send_on_widget(self):
        self.x.widget = MagicMock()
        target = self.x.widget.send = MagicMock()
        self.x.run_widget_command()
        self.assertTrue(target.called)

    def test_run_widget_command_calls_stop_on_widget(self):
        self.x.widget = MagicMock()
        target = self.x.widget.stop = MagicMock()
        self.x.stop()
        self.assertTrue(target.called)
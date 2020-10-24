"""
test_observable.py

TDD tests for observable class object.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.utilities import observable


class ObservableTest(unittest.TestCase):

    def setUp(self):
        self.o = observable.Observable()

    def test_exists(self):
        """Observable class object exists"""
        o = observable.Observable()
        self.assertIsInstance(o, observable.Observable)

    def test_data_param(self):
        """Set data param on obj"""
        o = observable.Observable(True)
        self.assertEqual(o.data, True)

    def test_callbacks_param(self):
        """Set callbacks param on obj"""
        o = observable.Observable()
        self.assertEqual(len(o.callbacks), 1)

    def test_get(self):
        """Get should return current data"""
        val = []
        o = observable.Observable(val)
        result = o.get()
        self.assertEqual(result, val)

    def test_set(self):
        """Should update current data"""
        val = []
        o = observable.Observable(val)
        target = True
        o.set(target)
        self.assertEqual(o.data, target)

    def test_unset(self):
        """Should update data to none"""
        val = []
        o = observable.Observable(val)
        o.unset()
        self.assertEqual(o.data, None)

    def test_set_calls_run_callbacks(self):
        """Should update current data"""
        val = []
        o = observable.Observable(val)
        mock = MagicMock()
        o.add_callback(mock)
        target = True
        o.set(target)
        self.assertIs(mock.called, True)

    def test_add_callback(self):
        """Add callback should update the callback attribute"""
        o = observable.Observable()
        mock = MagicMock()
        o.add_callback(mock)
        self.assertEqual(len(o.callbacks), 2)

    def test_run_callbacks(self):
        o = observable.Observable()
        mock = MagicMock(return_value=True)
        o.add_callback(mock)
        o.run_callbacks()
        self.assertIs(mock.called, True)

    def test_delete_callback(self):
        o = observable.Observable()
        mock = MagicMock(return_value=True)
        o.add_callback(mock)
        o.delete_callback(mock)
        self.assertEqual(len(o.callbacks), 1)

    def test_update_widget_attribute(self):
        name = 'update_widget'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_update_widget_calls_set_on_arg(self):
        from unittest.mock import MagicMock

        mock = MagicMock()
        mock.set = MagicMock()

        msg = 'XXX^666'
        self.o.set(msg)
        self.o.update_widget(mock)
        mock.set.assert_called_with(msg)

    def test_observer_list_attribute(self):
        name = 'observer_list'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_observer_list_attribute_is_list(self):
        self.assertEqual([], self.o.observer_list)

    def test_add_observer_attribute(self):
        name = 'add_observer'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_add_observer_method_adds(self):
        obs = MagicMock()
        self.o.add_observer(obs)
        self.assertIn(obs, self.o.observer_list)

    def test_add_observer_calls_set(self):
        sub = self.o.set = MagicMock()
        obs = MagicMock()
        self.o.add_observer(obs)
        current = self.o.get()
        sub.assert_called_with(current)

    def test_update_observers_attribute(self):
        name = 'update_observers'
        check = hasattr(self.o, name)
        self.assertTrue(check)

    def test_update_observers_calls_observers(self):
        from unittest.mock import MagicMock
        obs = MagicMock()
        obs.set = MagicMock()

        self.o.add_observer(obs)
        self.o.set("HELLO THERE")
        self.assertTrue(obs.set.called)

    def test_update_observers_is_callback(self):
        self.assertIn(self.o.update_observers, self.o.callbacks)

if __name__ == '__main__':
    unittest.main()

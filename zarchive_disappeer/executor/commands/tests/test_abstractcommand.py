"""
test_abstractcommand.py

Test suite for the AbstractCommand abstract base class for command objects

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import abc
import unittest
from unittest.mock import MagicMock

import executor.commands.abstractcommand as abstractcommand


class TestImports(unittest.TestCase):

    def test_abc(self):
        self.assertEqual(abc, abstractcommand.abc)


class ValidConcreteCommand(abstractcommand.AbstractCommand):

    def __init__(self, receiver, **kwargs):
        super().__init__(receiver, **kwargs)

    @property
    def name(self):
        return 'valid concrete test command'

    @property
    def valid_kwarg_keys(self):
        return set(['one', 'two', 'three'])

    def execute(self):
        pass


class InvalidConcreteCommandOne(abstractcommand.AbstractCommand):
    pass


class InvalidConcreteCommandThree(InvalidConcreteCommandOne):

    @property
    def name(self):
        return 'invalid concrete test command'


class InvalidConcreteCommandFour(InvalidConcreteCommandOne):

    @property
    def name(self):
        return 'valid concrete test command'

    @property
    def valid_kwarg_keys(self):
        return []

    def execute(self):
        pass


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.receiver = MagicMock()
        self.invalid_kwargs = dict(one=1, two=2, three=3, four=4)
        self.valid_kwargs = dict(one=1, two=2, three=3)
        self.valid_obj = ValidConcreteCommand(self.receiver, **self.valid_kwargs)

    def test_instance(self):
        self.assertIsInstance(self.valid_obj, abstractcommand.AbstractCommand)

    def test_metaclass_attribute(self):
        check = hasattr(self.valid_obj, '_abc_registry')
        self.assertTrue(check)

    def test_receiver_attr_set(self):
        self.assertEqual(self.valid_obj.receiver, self.receiver)

    def test_invalid_command_raises_error_with_no_methods(self):
        with self.assertRaises(TypeError):
            x = InvalidConcreteCommandOne(self.receiver)

    def test_invalid_command_raises_error_with_no_execute_method(self):
        with self.assertRaises(TypeError):
            x = InvalidConcreteCommandThree(self.receiver)

    def test_command_name_property(self):
        name = 'name'
        check = hasattr(self.valid_obj, name)
        self.assertTrue(check)
        with self.assertRaises(AttributeError):
            self.valid_obj.name = 'hello'

    def test_valid_kwarg_keys_property(self):
        name = 'valid_kwarg_keys'
        check = hasattr(self.valid_obj, name)
        self.assertTrue(check)
        with self.assertRaises(AttributeError):
            self.valid_obj.valid_kwarg_keys = 'hello'

    def test_validate_method_raises_error_if_valid_kwarg_keys_is_not_set(self):
        with self.assertRaises(ValueError):
            x = InvalidConcreteCommandFour(self.receiver)
            x.validate()

    def test_validate_method_raises_error_if_kwarg_keys_not_in_valid_keys(self):
        with self.assertRaises(KeyError):
            x = ValidConcreteCommand(self.receiver, **self.invalid_kwargs)
            x.validate()

    def test_validate_method_calls_update_attrs_method(self):
        self.valid_obj.validate()
        self.assertEqual(self.valid_obj.one, self.valid_kwargs['one'])

    def test_validate_called_by_constructor_on_valid_input(self):
        self.assertEqual(self.valid_obj.one, self.valid_kwargs['one'])

    def test_kwargs_attr_set(self):
        self.assertEqual(self.valid_obj.kwargs, self.valid_kwargs)

    def test_update_attrs_with_kwargs_updates_attrs(self):
        self.valid_obj.update_attrs_with_kwargs()
        self.assertEqual(self.valid_obj.one, self.valid_kwargs['one'])
        self.assertEqual(self.valid_obj.two, self.valid_kwargs['two'])

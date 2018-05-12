"""
test_abstractreceiver.py

Test suite for AbstractReceiver module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import abc
import unittest

from disappeer.executor.receivers import abstractreceiver


class TestImports(unittest.TestCase):

    def test_abc(self):
        self.assertEqual(abc, abstractreceiver.abc)


class ValidConcreteReceiver(abstractreceiver.AbstractReceiver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self):
        return 'valid concrete test receiver'

    @property
    def valid_kwarg_keys(self):
        return set(['one', 'two', 'three'])

    def execute(self):
        pass


class InvalidConcreteReceiverOne(abstractreceiver.AbstractReceiver):
    pass


class InvalidConcreteReceiverTwo(InvalidConcreteReceiverOne):

    def execute(self):
        pass


class InvalidConcreteReceiverThree(InvalidConcreteReceiverOne):

    @property
    def name(self):
        return 'invalid concrete test command'


class InvalidConcreteReceiverFour(InvalidConcreteReceiverOne):

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
        self.invalid_kwargs = dict(one=1, two=2, three=3, four=4)
        self.valid_kwargs = dict(one=1, two=2, three=3)
        self.valid_obj = ValidConcreteReceiver(**self.valid_kwargs)

    def test_instance(self):
        self.assertIsInstance(self.valid_obj, abstractreceiver.AbstractReceiver)

    def test_metaclass_attribute(self):
        check = hasattr(self.valid_obj, '_abc_registry')
        self.assertTrue(check)

    def test_invalid_receiver_raises_error_with_no_methods(self):
        with self.assertRaises(TypeError):
            x = InvalidConcreteReceiverOne()

    def test_invalid_receiver_raises_error_with_no_name(self):
        with self.assertRaises(TypeError):
            x = InvalidConcreteReceiverTwo()

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
            x = InvalidConcreteReceiverFour()
            x.validate()

    def test_validate_method_raises_error_if_kwarg_keys_not_in_valid_keys(self):
        with self.assertRaises(KeyError):
            x = ValidConcreteReceiver(**self.invalid_kwargs)
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

    def test_valid_concrete_receiver_with_func_refs_as_kwargs(self):
        target = 'wtf666'

        def external_func():
            return target

        class ValidConcreteReceiverWithFuncRefs(ValidConcreteReceiver):

            @property
            def valid_kwarg_keys(self):
                return {'func'}

            def execute(self):
                return self.func()

        kwargs = dict(func=external_func)
        x = ValidConcreteReceiverWithFuncRefs(**kwargs)
        result = x.execute()
        self.assertEqual(result, target)


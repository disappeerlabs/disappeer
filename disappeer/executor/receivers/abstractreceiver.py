"""
abstractreceiver.py

Module for command pattern AbstractReceiver class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import abc
from disappeer.utilities.logger import log


class AbstractReceiver(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.validate()

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def valid_kwarg_keys(self):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def validate(self):
        if not isinstance(self.valid_kwarg_keys, set):
            log.error("Valid kwarg keys must be a set.")
            raise ValueError
        if self.valid_kwarg_keys != self.kwargs.keys():
            log.error("Key Error: Invalid keys in receiver object.\nValid kwarg keys: {}.\nGiven kwarg keys: {}".format(self.valid_kwarg_keys, self.kwargs.keys()))
            raise KeyError
        self.update_attrs_with_kwargs()

    def update_attrs_with_kwargs(self):
        self.__dict__.update((k, v) for k, v in self.kwargs.items())
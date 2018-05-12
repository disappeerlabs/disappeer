"""
abstractcommand.py

Module for the AbstractCommand abstract base class for command objects

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import abc
from disappeer.utilities.logger import log


class AbstractCommand(metaclass=abc.ABCMeta):

    def __init__(self, receiver, **kwargs):
        self.receiver = receiver
        self.kwargs = kwargs
        self.validate()

    @property
    @abc.abstractproperty
    def name(self):
        raise NotImplementedError

    @property
    @abc.abstractproperty
    def valid_kwarg_keys(self):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError

    def validate(self):
        if not isinstance(self.valid_kwarg_keys, set):
            raise ValueError
        elif self.valid_kwarg_keys != self.kwargs.keys():
            log.error("Key Error:\nValid kwarg keys: {}.\nGiven kwarg keys: {}".format(self.valid_kwarg_keys, self.kwargs.keys()))
            raise KeyError
        self.update_attrs_with_kwargs()

    def update_attrs_with_kwargs(self):
        self.__dict__.update((k, v) for k, v in self.kwargs.items())



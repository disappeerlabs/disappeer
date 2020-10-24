"""
observable.py

A simple observable class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


class Observable:

    def __init__(self, data=None):
        self.data = data
        self.callbacks = {}
        self.observer_list = []
        self.add_callback(self.update_observers)

    def get(self):
        return self.data

    def set(self, data):
        self.data = data
        self.run_callbacks()

    def unset(self):
        self.data = None

    ##############################
    #  CALLBACK METHODS          #
    ##############################

    def add_callback(self, func):
        self.callbacks[func] = 1

    def run_callbacks(self):
        for func in self.callbacks:
            func(self)

    def delete_callback(self, func):
        del self.callbacks[func]

    ##############################
    #  OBSERVER METHODS          #
    ##############################

    def update_widget(self, widget_var):
        widget_var.set(self.get())

    def add_observer(self, observer):
        self.observer_list.append(observer)
        self.set(self.data)

    def update_observers(self, param):
        for item in self.observer_list:
            self.update_widget(item)
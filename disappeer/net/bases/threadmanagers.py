"""
threadmanagers.py

Threadmanager module for:
    - AbstractThreadManager
    - ServerThreadManager concrete class
    - ClientThreadManager concrete class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import abc
import threading


class AbstractThreadManager(metaclass=abc.ABCMeta):

    def __init__(self, factory):
        self.factory = factory
        self.widget_thread = None
        self.widget = None

    def start(self):
        self.widget = self.factory.build()
        self.widget_thread = threading.Thread(target=self.run_widget_command, name=self.factory.name)
        self.widget_thread.daemon = True
        self.widget_thread.start()

    @abc.abstractmethod
    def run_widget_command(self):
        raise NotImplementedError

    @abc.abstractmethod
    def stop(self):
        """
        Stop data thread, set running flag.
        """
        raise NotImplementedError


class ServerThreadManager(AbstractThreadManager):

    def run_widget_command(self):
        # TODO: add try/except to catch Attribute Error if object does not exist
        self.widget.serve_forever()

    def stop(self):
        # TODO: add try/except to catch Attribute Error if object does not exist
        self.widget.shutdown()
        self.widget.server_close()


class ClientThreadManager(AbstractThreadManager):

    def run_widget_command(self):
        self.widget.send()

    def stop(self):
        self.widget.stop()


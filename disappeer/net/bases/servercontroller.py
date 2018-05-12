"""
servercontroller.py

Module for ServerController class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.utilities import observable


class ServerController:

    def __init__(self, que, factory, manager):
        self.status = observable.Observable(False)
        self.queue = que
        self.factory = factory(self.queue)
        self.server = manager(self.factory)

    def start(self):
        self.server.start()
        self.status.set(True)

    def stop(self):
        self.server.stop()
        self.status.set(False)

    def get_status(self):
        return self.status.get()

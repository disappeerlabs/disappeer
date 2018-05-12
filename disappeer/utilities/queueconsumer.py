"""
queueconsumer.py

Module for QueueConsumer controller base class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import queue
from disappeer.constants import constants
import logging

log = logging.getLogger(constants.title)


class QueueConsumer:

    def __init__(self, root):
        self.root = root
        self.queue = queue.Queue()
        self.poll_queue()

    def poll_queue(self):
        self.consume_queue()
        self.root.after(200, self.poll_queue)

    def consume_queue(self):
        if not self.queue.empty():
            got = self.queue.get()
            self.process_queue_result(got)
            self.queue.task_done()

    def process_queue_result(self, payload):
        check = self.check_payload(payload)
        if check:
            self.handle_queue_payload(payload)

    def check_payload(self, payload):
        if not isinstance(payload, dict):
            log.error("{}-QueueConsumer payload of type {} is not dict: {}".format(type(self).__name__, type(payload), payload))
            return False
        try:
            desc = payload['desc']
        except KeyError as err:
            log.error("{}-QueueConsumer, malformed payload: {}, {}".format(type(self).__name__, err, payload))
            return False
        return payload

    def handle_queue_payload(self, payload):
        raise NotImplementedError
"""
keycreator.py

KeyCreator GPG Agent module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.constants import constants
from disappeer.gpg.agents import gpgagent
import threading

command_list = constants.command_list


class KeyCreator(gpgagent.GPGAgent):

    def __init__(self, keydir, queue):
        super().__init__(keydir)
        self.queue = queue

    def execute(self, key_input_dict):
        t = threading.Thread(name=command_list.Create_New_Key,
                             target=self._create_new_key_worker,
                             args=(key_input_dict,))
        t.start()

    def _create_new_key_worker(self, key_input_dict):
        input_data = self.gpg.gen_key_input(**key_input_dict)
        result = self.gpg.gen_key(input_data)
        desc = command_list.Create_New_Key
        payload = {"desc": desc, "result": result}
        self.queue.put(payload)

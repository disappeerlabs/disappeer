"""
contactrequestfactory.py

Module for ContactRequestFactory class object, for generating contact request payload dicts

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import hashlib
import random
import sys
import json
from disappeer import settings
from disappeer.gpg.agents import signer


class ContactRequestFactory:

    def __init__(self, contact_response_host_address, key_home_dir, passphrase):
        self.key_home_dir = key_home_dir
        self.gpgsigner = signer.Signer(self.key_home_dir)
        self.contact_response_host = contact_response_host_address
        self.contact_response_port = settings.port_contact_response_server
        self.passphrase = passphrase

    def build(self):
        encoded_data_dict = self.encode_data_dict()
        detached_sig = self.sign_encoded_data(encoded_data_dict)
        if len(detached_sig.data) == 0:
            return detached_sig
        else:
            request_dict = dict(data=encoded_data_dict, sig=str(detached_sig))
            return request_dict

    def sign_encoded_data(self, encoded_data):
        result = self.gpgsigner.execute(encoded_data, None, self.passphrase, detach=True)
        return result

    def encode_data_dict(self):
        return json.dumps(self.construct_data_dict())

    def construct_data_dict(self):
        data_dict = dict(gpg_pub_key=self.read_file(settings.gpg_host_pubkey),
                         address_host=self.contact_response_host,
                         address_port=self.contact_response_port,
                         nonce=self.random_hash())
        return data_dict

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            result = f.read()
        return result

    def random_hash(self):
        num_str = str(random.randint(0, sys.maxsize))
        result = self.hash_message(num_str)
        return result

    def hash_message(self, message):
        hasher = hashlib.sha1()
        hasher.update(bytes(message, 'UTF-8'))
        digest = hasher.hexdigest()
        return digest


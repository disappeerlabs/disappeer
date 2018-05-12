"""
contactresponsefactory.py

Module for ContactResponseFactory class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import hashlib
import random
from disappeer import settings
import sys
import json
import tempfile
from disappeer.gpg.agents import keyring
from disappeer.gpg.agents import signer
from disappeer.gpg.agents import encrypter


class ContactResponseFactory:

    def __init__(self, message_server_host_address, key_home_dir, request_data_record, passphrase):
        self.request_data_record = request_data_record
        self.message_server_address = message_server_host_address
        self.message_server_port = settings.port_message_server
        self.key_home_dir = key_home_dir
        self.passphrase = passphrase
        self.gpgsigner = signer.Signer(self.key_home_dir)
        self.temp_dir = self.create_temp_dir()
        self.temp_dir_name = self.temp_dir.name
        self.key_ring = keyring.KeyRing(self.temp_dir_name)
        self.encrypt_agent = encrypter.Encrypter(self.temp_dir_name)
        self.target_fingerprint = None
        self.request_nonce = None
        self.response_nonce = None
        self.data_dict = None
        self.encoded_data_dict = None
        self.sig = None
        self.error = None
        self.valid = None
        self.sig_dict = None
        self.encoded_sig_dict = None

    def import_pubkey_to_keyring(self):
        result = self.key_ring.import_key(self.request_data_record.gpg_pub_key)
        if len(result.fingerprints) == 1:
            self.target_fingerprint = result.fingerprints[0]
        else:
            msg = "Key import error"
            self.set_error(msg)
        return result

    def construct_data_dict(self):
        self.response_nonce = self.random_hash()
        data_dict = dict(address_host=self.message_server_address,
                         address_port=self.message_server_port,
                         response_nonce=self.response_nonce,
                         request_nonce=self.request_data_record.nonce)
        self.data_dict = data_dict
        return data_dict

    def encode_data_dict(self):
        self.encoded_data_dict = self.encode_obj(self.construct_data_dict())
        return self.encoded_data_dict

    def sign_encoded_data_dict(self):
        encoded_data = self.encode_data_dict()
        sig = self.gpgsigner.execute(encoded_data, None, self.passphrase, detach=True)
        if len(sig.data) == 0:
            msg = 'GPG sig error'
            self.set_error(msg)
        else:
            self.sig_dict = dict(sig=str(sig), data=encoded_data)
            return self.sig_dict

    def encode_sig_dict(self):
        sig_dict = self.sign_encoded_data_dict()
        if self.error is not None:
            return None
        else:
            self.encoded_sig_dict = self.encode_obj(sig_dict)
            return self.encoded_sig_dict

    def encrypt_encoded_sig_dict(self):
        result_encrypt = self.encrypt_agent.execute(self.encoded_sig_dict, self.target_fingerprint)
        if not result_encrypt.ok:
            self.set_error("GPG encypt error" + result_encrypt.stderr)
        else:
            final = dict(ciphertext=str(result_encrypt))
            return final

    def build(self):
        self.import_pubkey_to_keyring()
        self.encode_sig_dict()
        final = self.encrypt_encoded_sig_dict()
        if self.error is None:
            self.valid = True
            final['request_nonce'] = self.request_data_record.nonce
            final['response_nonce'] = self.response_nonce
            return final, self.response_nonce

    def set_error(self, err_msg):
        self.error = err_msg
        self.valid = False

    def encode_obj(self, target_object):
        return json.dumps(target_object)

    def create_temp_dir(self):
        temp_dir = tempfile.TemporaryDirectory()
        return temp_dir

    def close_temp_dir(self):
        self.temp_dir.cleanup()

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            result = f.read()
        return result

    def hash_message(self, message):
        hasher = hashlib.sha1()
        hasher.update(bytes(message, 'UTF-8'))
        digest = hasher.hexdigest()
        return digest

    def random_hash(self):
        num_str = str(random.randint(0, sys.maxsize))
        result = self.hash_message(num_str)
        return result

    def __del__(self):
        try:
            self.close_temp_dir()
        except AttributeError:
            pass

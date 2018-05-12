"""
messagefactory.py

Module for the MessageFactory class object, for building message payload dicts.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from  disappeer import  settings
import hashlib
import random
import sys
import json
from disappeer.gpg.agents import signer
from disappeer.gpg.helpers import tempkeyring
from disappeer.gpg.agents import encrypter


class MessageFactory:

    def __init__(self, message_server_host_address, key_home_dir, peer_pub_key, host_fingerprint, message_text, passphrase):
        self.message_server_host_address = message_server_host_address
        self.message_server_host_port = settings.port_message_server
        self.key_home_dir = key_home_dir
        self.peer_gpg_pub_key = peer_pub_key  # this is the SEND-TO val, i.e. addressee
        self.host_fingerprint = host_fingerprint  # this is the SENT-FROM val, i.e. addresser
        self.message_text = message_text
        self.passphrase = passphrase
        self.gpgsigner = signer.Signer(self.key_home_dir)
        self.temp_keyring = tempkeyring.TempKeyRing()
        self.encrypt_agent = encrypter.Encrypter(self.key_home_dir)
        self.nonce = None
        self.data_dict = None
        self.sig_dict = None
        self.target_fingerprint = None
        self.ciphertext_dict = None
        self.valid = None
        self.error = None

    def build(self):
        """
        If false, return false. Otherwise . . .
        :return: {nonce: 'nonce_string', ciphertext: 'ciphertextstring'}
        """
        encoded_data_dict = self.construct_data_dict()
        encoded_sig_dict = self.construct_sig_dict(encoded_data_dict)
        if encoded_sig_dict is False:
            return False

        # TODO: THIS IS UNNECESSARY IF WE USE THE CURRENT HOST KEY RING
        #     - this gives us the fingerprint
        #     - could instead just pass in fingerprint as init arg, and skip this step
        #     - But this import also checks to make sure the key is valid so, there's that
        target_fingerprint = self.import_pubkey_to_temp_keyring()
        if target_fingerprint is False:
            return False

        fingerprint_list = [self.host_fingerprint, target_fingerprint]
        ciphertext_dict = self.construct_ciphertext_dict(encoded_sig_dict, fingerprint_list)
        if ciphertext_dict is False:
            return False

        ciphertext_dict['nonce'] = self.nonce
        self.valid = True
        return ciphertext_dict

    def construct_ciphertext_dict(self, plaintext, fingerprint):
        result = self.encrypt_agent.execute(plaintext, fingerprint)
        if not result.ok:
            self.set_error("GPG encypt error" + result.stderr)
            return False
        else:
            self.ciphertext_dict = dict(ciphertext=str(result))
            return self.ciphertext_dict

    def import_pubkey_to_temp_keyring(self):
        result = self.temp_keyring.key_ring.import_key(self.peer_gpg_pub_key)
        if len(result.fingerprints) == 1:
            self.target_fingerprint = result.fingerprints[0]
            return self.target_fingerprint
        else:
            msg = "Key import error"
            self.set_error(msg)
            return False

    def construct_sig_dict(self, encoded_data_obj):
        sig = self.gpgsigner.execute(encoded_data_obj, None, self.passphrase, detach=True)
        if len(sig.data) == 0:
            msg = 'GPG sig error'
            self.set_error(msg)
            return False
        else:
            self.sig_dict = dict(sig=str(sig), data=encoded_data_obj)
            return self.encode_obj(self.sig_dict)

    def construct_data_dict(self):
        self.nonce = self.random_hash()
        self.data_dict = dict(address_host=self.message_server_host_address,
                              address_port=self.message_server_host_port,
                              nonce=self.nonce,
                              sent_to=self.import_pubkey_to_temp_keyring(),
                              sent_from=self.host_fingerprint,
                              message=self.message_text)
        return self.encode_obj(self.data_dict)

    def set_error(self, err_msg):
        self.error = err_msg
        self.valid = False

    def encode_obj(self, target_object):
        return json.dumps(target_object)

    def hash_message(self, message):
        hasher = hashlib.sha1()
        hasher.update(bytes(message, 'UTF-8'))
        digest = hasher.hexdigest()
        return digest

    def random_hash(self):
        num_str = str(random.randint(0, sys.maxsize))
        result = self.hash_message(num_str)
        return result

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            result = f.read()
        return result

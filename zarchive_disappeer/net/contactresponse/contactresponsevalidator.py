"""
contactresponsevalidator.py

Module for ContactResponseValidator class object:
    - check payload keys
    - check request nonce against valid outstanding request nonces
    - decrypt ciphertext
    - check decryption for sig and data dict keys
    - check sig of data dict
    - decode data dict
    - check info in data dict


Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


from disappeer.gpg.agents import decrypter
from disappeer.gpg.helpers import tempdetachedverifier
from disappeer.models.db import dbpendingcontactresponsetable
from disappeer import settings
import json


class ContactResponseValidator:

    def __init__(self, contact_response_server_request_payload, key_dir, pending_contact_resp_db_table, passphrase):
        self.payload = contact_response_server_request_payload
        self.key_dir = key_dir
        self.db_pending_contacts = pending_contact_resp_db_table
        self.passphrase = passphrase
        self.error = None
        self.valid = None
        self.data_dict = None

    def validate(self):
        payload_key_check = self.check_payload_keys(self.payload)
        if payload_key_check is False:
            msg = 'Error: bad payload'
            self.set_error(msg)
            return False

        request_nonce = self.payload['request_nonce']
        request_nonce_check = self.is_request_nonce_valid(request_nonce)
        if request_nonce_check is False:
            msg = 'Error: bad request nonce.'
            self.set_error(msg)
            return False

        ciphertext = self.payload['ciphertext']
        decrypted_ciphertext = self.decrypt_ciphertext(ciphertext)
        if decrypted_ciphertext is False:
            return False

        sig_dict = self.decode_json_string(decrypted_ciphertext)
        if sig_dict is False:
            msg = 'Error: sig dict decode of decrypted ciphertext returned false'
            self.set_error(msg)
            return False

        sig_dict_check = self.check_sig_dict_keys(sig_dict)
        if sig_dict_check is False:
            msg = 'Error: sig dict keys are false'
            self.set_error(msg)
            return False

        gpg_pub_key = self.fetch_gpg_pub_key_by_nonce(request_nonce)
        if gpg_pub_key is None:
            msg = 'Error: gpg pub key from db is None'
            self.set_error(msg)
            return False

        sig_is_valid = self.verify_sig_dict_with_key(gpg_pub_key, sig_dict)
        if sig_is_valid is False:
            msg = 'Error: signature validation failed'
            self.set_error(msg)
            return False

        sig_data_dict = self.decode_json_string(sig_dict['data'])
        if sig_data_dict is False:
            msg = 'Error: signature data dict decode error'
            self.set_error(msg)
            return False

        check_sig_data_dict_keys = self.check_sig_dict_data_dict_keys(sig_data_dict)
        if check_sig_data_dict_keys is False:
            msg = 'Error: sig data dict keys are false'
            self.set_error(msg)
            return False

        self.valid = True
        self.data_dict = sig_data_dict
        return True

    def check_sig_dict_data_dict_keys(self, sig_dict_data_dict):
        target_keys = ['address_host',
                       'address_port',
                       'response_nonce',
                       'request_nonce']
        try:
            check = all(key in sig_dict_data_dict for key in target_keys)
        except TypeError as err:
            return False
        else:
            return check

    def verify_sig_dict_with_key(self, pub_key, sig_dict):
        verifier = tempdetachedverifier.TempDetachedVerifier(pub_key, sig_dict)
        if not verifier.valid:
            return False
        else:
            return True

    def fetch_gpg_pub_key_by_nonce(self, nonce):
        result = self.db_pending_contacts.fetch_gpg_pub_key_by_nonce(nonce)
        return result

    def check_sig_dict_keys(self, sig_dict):
        target_keys = ['sig', 'data']
        try:
            check = all(key in sig_dict for key in target_keys)
        except TypeError as err:
            return False
        else:
            return check

    def decrypt_ciphertext(self, ciphertext):
        decrypt_agent = decrypter.Decrypter(self.key_dir)
        result = decrypt_agent.execute(ciphertext, self.passphrase)
        if result.ok is False:
            self.set_error(result.status)
            return False
        else:
            return str(result)

    def is_request_nonce_valid(self, request_nonce):
        nonce_list = self.db_pending_contacts.fetch_all_nonces()
        if request_nonce in nonce_list:
            return True
        else:
            return False

    def check_payload_keys(self, payload):
        target_keys = ['ciphertext',
                       'request_nonce',
                       'response_nonce']
        try:
            check = all(key in payload for key in target_keys)
        except (TypeError, KeyError) as err:
            return False
        else:
            return check

    def decode_json_string(self, json_string):
        try:
            result = json.loads(json_string)
        except (TypeError, ValueError) as err:
            return False
        else:
            return result

    def set_error(self, err_msg):
        self.error = err_msg
        self.valid = False

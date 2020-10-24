"""
messagevalidator.py

Module for MessageValidator class object to validate received messages

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import decrypter
from disappeer.gpg.agents import detachedverifier
import json
import tempfile


class MessageValidator:

    def __init__(self, message_server_payload, key_dir, passphrase):
        self.message_payload = message_server_payload
        self.key_dir = key_dir
        self.passphrase = passphrase
        self.gpg_verifier = detachedverifier.DetachedVerifier(self.key_dir)
        self.error = None
        self.valid = None
        self.data_dict = None
        self.verify_result = None

    def validate(self):
        payload_key_check = self.check_payload_keys(self.message_payload)
        if payload_key_check is False:
            msg = 'Message payload key check is false'
            self.set_error(msg)
            return False

        decrypt_result = self.decrypt_ciphertext(self.message_payload['ciphertext'])
        if decrypt_result is False:
            return False

        decoded_decrypt_result = self.decode_json_string(decrypt_result)
        if decoded_decrypt_result is False:
            msg = 'JSON decode of decryption result returned false'
            self.set_error(msg)
            return False

        sig_dict_keys_check = self.check_sig_dict_keys(decoded_decrypt_result)
        if sig_dict_keys_check is False:
            msg = 'Sig dict key check is false'
            self.set_error(msg)
            return False

        verify_sig_result = self.verify_sig_dict(decoded_decrypt_result)
        if verify_sig_result is False:
            return False

        data_dict_encoded = decoded_decrypt_result['data']
        data_dict = self.decode_json_string(data_dict_encoded)

        data_dict_check = self.check_data_dict_keys(data_dict)
        if data_dict_check is False:
            msg = 'Data dict check returned false'
            self.set_error(msg)
            return False

        # Success
        self.valid = True
        self.data_dict = data_dict
        return True

    def check_data_dict_keys(self, data_dict):
        target_keys = ['address_host',
                       'address_port',
                       'nonce',
                       'message']
        try:
            check = all(key in data_dict for key in target_keys)
        except TypeError as err:
            return False
        else:
            return check

    def verify_sig_dict(self, sig_dict):
        sig_bytes = bytes(sig_dict['sig'], 'utf-8')
        data_bytes = bytes(sig_dict['data'], 'utf-8')
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(sig_bytes)
            tmp_file.seek(0)
            self.verify_result = self.gpg_verifier.execute(tmp_file.name, data_bytes)
            if self.verify_result.valid:
                return self.verify_result.valid
            else:
                self.set_error(self.verify_result.stderr)
                return self.verify_result.valid

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

    def check_payload_keys(self, payload):
        target_keys = ['ciphertext', 'nonce']
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

"""
contactrequestvalidator.py

Module for the ContactRequestValidator class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.gpg.agents import detachedverifier
from disappeer.gpg.agents import keyring
import tempfile
import json


class ContactRequestValidator:

    def __init__(self, contact_request_dict):
        self.contact_req_dict = contact_request_dict
        self.sig = None
        self.data = None
        self.data_dict = None
        self.pub_key = None
        self.nonce = None
        self.error = None
        self.valid = None
        self.result_dict = None
        self.key_dict = None
        self.run_checks()
        self.validate()
        self.construct_result_dict()

    def check_sig(self):
        try:
            self.sig = self.contact_req_dict['sig']
        except (KeyError, TypeError) as err:
            self.sig = False

    def check_data(self):
        try:
            self.data = self.contact_req_dict['data']
        except (KeyError, TypeError) as err:
            self.data = False

    def check_data_dict(self):
        try:
            self.data_dict = json.loads(self.data)
        except (ValueError, TypeError) as err:
            self.data_dict = False

    def check_pub_key(self):
        try:
            self.pub_key = self.data_dict['gpg_pub_key']
        except (KeyError, TypeError) as err:
            self.pub_key = False

    def check_nonce(self):
        try:
            self.nonce = self.data_dict['nonce']
        except (KeyError, TypeError) as err:
            self.nonce = False

    def run_checks(self):
        self.check_sig()
        self.check_data()
        self.check_data_dict()
        self.check_pub_key()
        self.check_nonce()

    def is_data_valid(self):
        if not all([self.sig, self.data, self.pub_key, self.data_dict, self.nonce]):
            self.error = 'Invalid data structure in request object.'
            self.valid = False
            return False

    def is_key_valid(self, key_dir):
        key_ring_agent = keyring.KeyRing(key_dir)
        result = key_ring_agent.import_key(self.pub_key)
        if result.count == 0:
            self.error = result.stderr
            self.valid = False
            return False
        else:
            self.key_dict = key_ring_agent.get_raw_key_list()[0]

    def verify_sig(self, key_dir):
        verifier = detachedverifier.DetachedVerifier(key_dir)
        sig_bytes = bytes(self.sig, 'utf-8')
        data_bytes = bytes(self.data, 'utf-8')

        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(sig_bytes)
            tmp_file.seek(0)
            verify_detached = verifier.execute(tmp_file.name, data_bytes)
            if not verify_detached.valid:
                self.error = verify_detached.stderr
            self.valid = verify_detached.valid
            return verify_detached

    def validate(self):
        if self.is_data_valid() is False:
            return False
        with tempfile.TemporaryDirectory() as tmp_dir:
            if self.is_key_valid(tmp_dir) is False:
                return False
            result = self.verify_sig(tmp_dir)
            return result

    def construct_result_dict(self):
        if self.valid:
            target = dict(contact_req_dict=self.contact_req_dict,
                          nonce=self.nonce,
                          data_dict=self.data_dict)
            self.result_dict = target
            return self.result_dict
        else:
            self.result_dict = False
            return False

"""
test_contactresponsefactory.py

Test suite for ContactResponseFactory class object and module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import patch, MagicMock
from disappeer.net.contactresponse import contactresponsefactory
import hashlib
import random
from disappeer import settings
import sys
import json
import tempfile
from disappeer.gpg.agents import keyring
from disappeer.gpg.agents import signer
from disappeer.gpg.agents import encrypter
import copy


gpg_pub_key_string = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQENBFkV2wYBCADhSKS5957Y/3NPYUO6RVYpTPScMxULQ5fR2bwIZYMvSjZ7rdPM
zlcCg7MbXvFBrzbRKebzt1tmhntBjzi0HnpPcsTslQZyOfiZ3plfiQXGZMdL83t4
g/nxP6i3+TfXafalUnr2Zp3vk9ClWyBFS1Bmzqz97w4S8uhrvMal/TklDJ+3MY8F
vsPpaOgZvCgG27vyoQnay+mVkWgC+bOFnl9tjXCSr2a1seHJpUCmJgT/qba3wVI2
NUdq9fHChY9ug1BHTFm7HvFWntRKPT+682lm3iS8kssdacxFxpheRwj6Qdk+yRQO
Ht+I8T/GtCEF0HlscYhg+7JbLnxMdYhKctTjABEBAAG0N21hY3Rvd2VyIChEZWZh
dWx0IGNvbW1lbnQgbWVzc2FnZSkgPG1hY3Rvd2VyQGVtYWlsLmNvbT6JAT4EEwEC
ACgFAlkV2wYCGy8FCQGqfjoGCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEFWk
Wpn+ReVA4i8IAIW0JB7VEI+q0n2+exWu7uITB6OmSvJ+xadEP6sUwf02Eghppiyg
u181ZE9TpspMNscTxyv03bK9yMqbNgpNQ6LUKzD90Qlut9gl9whxCVDI78VGrCXf
YjTfG5kowCU2mIhJIpUAdb8ufvqZFYo2BnRrsj/heu9+JSYRevs+yTADo2gJGOZQ
LOm+ra8BXyw5SYAwfO+YzyuXw5ITkXppxvL2jvLf62OGNSPF3nEbS/EebJZENtw7
F0fh+9xKao+mJIX6bjAgUlIWvaqsu6W7DKeNf/flYoCnddnP06FvgjCMC9G2II9p
qVw+Ytr7XLZuvjqx84VimuK6y4+DY6shhOC5Ag0EWRXbBhAIALCVLle15qOSsQwr
0sbJ2+sN57ZzNfYOZMUqZbC9YCOPDDu54UtY2nB6oJ54PJZBGp4Fmd5oQgBYuntL
9BMj22MFgWH9Ia8RUuAImGScaGT0/BVyueeWygag0T7AuCN2Mkoed7GaA3Vv3rJf
YdBwlY6rGiIy68iWMFd4E4LCf8XTC6twufvaw0gKS4LuFLCmxEsKYIrRfYDT/MtU
b+tz+g+mxAmolGN7j7WyAdhYNNGKSh3N+AZQbBDUK0Mbrr0sdKOEJBCrN72jygGm
BfIgAkJFQ4XaG/AJ/sOgvXN3vXvzEFQrPgOVVmmVPoBOdU97kzETcEg+ZyQtOSAg
fFi20bMAAwUH/2KnoIigeKqhs8MbGGxEFJHsVxTAMxCj8A+p73+KLEtwm4DSziff
ggxnsPxEAPqwopIErB6DB2DPNVr6b4txQVIh/oe4zMhEpONi9GyTgINChNcjf7VW
Gu7So4s7y1FE2e14Xx/CsI7pICQa/FYZPmTEFOxF6vgPqnp3H2gfR7rG3FsrXZdr
mn9Aov4jCBbOBJ8Ucgfv3F0AIDs32qvuCusjYHRFggzdgtK4D92H5VidE+F0sdJK
314VtZVGcCnrvyNV/OKJ+LsKnskgGOWyYItEm5XJ8BIz1b9MBvXcGrSPPUeAonbE
6Ayl6ogjCn6l1Gn/h/JcsvawNSZLz2rYBjSJASUEGAECAA8FAlkV2wYCGwwFCQGq
fjoACgkQVaRamf5F5UCSkAgAx7gC2263ZPSTQZCJE8uJHeD9Ybik7o1/txaIICMV
vzBxIOBOSSOMVjwxJhQwkj3//WQjBmqNghlsIq5Rfwnj4bNSTrZj8pqDtoqYv1fg
WVhZv4mFF7Uw+O42Y/TC9rAU/pzvDIyUW6pLEOUMv0uUT7vqWFN8+ELGZrWQwSVL
8q6eBOhLuwq67ee4wFWc3EUh3BL1nTWfoUeJgWLJqgUIWsXK0UMhkTjuIJTRArxA
Htuy1Idq3WBJq0xL2apEfuaZTYlcbaKabieg62kseAwMsALEetBDljtUK7tkCWIS
9bB+QnZSJ1naxflAI/TtxVoLlyWRz3Mw5MxzDayjI7nYxA==
=IF8v
-----END PGP PUBLIC KEY BLOCK-----'''


class TestImports(unittest.TestCase):

    def test_hashlib(self):
        self.assertEqual(hashlib, contactresponsefactory.hashlib)

    def test_random(self):
        self.assertEqual(random, contactresponsefactory.random)

    def test_sys(self):
        self.assertEqual(sys, contactresponsefactory.sys)

    def test_json(self):
        self.assertEqual(json, contactresponsefactory.json)

    def test_tempfile(self):
        self.assertEqual(tempfile, contactresponsefactory.tempfile)

    def test_keyring(self):
        self.assertEqual(keyring, contactresponsefactory.keyring)

    def test_signer(self):
        self.assertEqual(signer, contactresponsefactory.signer)

    def test_encrypter(self):
        self.assertEqual(encrypter, contactresponsefactory.encrypter)


class MockDataRecord:
    nonce = 'nonce_string'
    gpg_pub_key = gpg_pub_key_string


class TestClassBasics(unittest.TestCase):

    hello = 'hello'
    target_file = settings.gpg_host_pubkey
    message_host_address = '.onion'
    key_home_dir = 'tests/data/keys/'
    request_nonce = 'request_nonce_string'
    request_data_record = MockDataRecord()
    passphrase = 'passphrase'
    valid_obj = contactresponsefactory.ContactResponseFactory(message_host_address,
                                                              key_home_dir,
                                                              request_data_record,
                                                              passphrase)

    def setUp(self):
        self.x = copy.deepcopy(self.valid_obj)

    def tearDown(self):
        self.x.temp_dir.cleanup()

    def test_instance(self):
        self.assertIsInstance(self.x, contactresponsefactory.ContactResponseFactory)

    def test_settings(self):
        self.assertEqual(settings, contactresponsefactory.settings)

    def test_message_server_port_attribute(self):
        self.assertEqual(settings.port_message_server, self.x.message_server_port)

    def test_message_server_host_address_attribute_set(self):
        self.assertEqual(self.message_host_address, self.x.message_server_address)

    def test_key_home_dir_attribute_set(self):
        self.assertEqual(self.x.key_home_dir, self.key_home_dir)

    def test_request_data_record_attribute_set(self):
        self.assertEqual(type(self.x.request_data_record), type(self.request_data_record))

    def test_passphrase_attr_set(self):
        self.assertEqual(self.x.passphrase, self.passphrase)

    def test_key_ring_attribute_is_keyring_with_temp_dir(self):
        self.assertIsInstance(self.x.key_ring, keyring.KeyRing)
        self.assertEqual(self.x.key_ring.home, self.x.temp_dir_name)

    def test_encypt_agent_is_encrypter_with_temp_dir(self):
        self.assertIsInstance(self.x.encrypt_agent, encrypter.Encrypter)
        self.assertEqual(self.x.encrypt_agent.home, self.x.temp_dir_name)

    def test_gpg_signer_attribute_set(self):
        self.assertIsInstance(self.x.gpgsigner, signer.Signer)
        self.assertEqual(self.x.gpgsigner.home, self.x.key_home_dir)

    def test_encoded_data_dict_attribute_set_none(self):
        self.assertIsNone(self.x.encoded_data_dict)

    def test_sig_attribute_set_none(self):
        self.assertIsNone(self.x.sig)

    def test_error_attribute_set_none(self):
        self.assertIsNone(self.x.error)

    def test_valid_attribute_set_none(self):
        self.assertIsNone(self.x.valid)

    def test_encoded_sig_dict_attribute_set_none(self):
        self.assertIsNone(self.x.encoded_sig_dict)

    def test_target_fingerprint_set_none(self):
        self.assertIsNone(self.x.target_fingerprint)

    def test_request_nonce_attribute_set_none(self):
        self.assertIsNone(self.x.request_nonce)

    def test_response_nonce_attribute_set_none(self):
        self.assertIsNone(self.x.response_nonce)

    def test_data_dict_set_none(self):
        self.assertIsNone(self.x.data_dict)

    def test_sig_dict_set_none(self):
        self.assertIsNone(self.x.sig_dict)

    def test_set_error_method_sets_error_and_valid(self):
        msg = 'Error Message'
        self.x.set_error(msg)
        self.assertEqual(self.x.error, msg)
        self.assertIs(self.x.valid, False)

    def test_hash_message_method_returns_hash(self):
        check = 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
        result = self.x.hash_message(self.hello)
        self.assertEqual(result, check)

    @patch('disappeer.net.contactresponse.contactresponsefactory.random')
    def test_random_hash_method_calls_randint(self, patched):
        check = 'b1d5781111d84f7b3fe45a0852e59758cd7a87e5'
        val = str(10)
        patched.randint.return_value = val
        result = self.x.random_hash()
        patched.randint.assert_called_with(0, sys.maxsize)
        self.assertEqual(result, check)

    def test_read_file_method_returns_file_contents(self):
        with open(self.target_file, 'r') as f:
            check = f.read()
        result = self.x.read_file(self.target_file)
        self.assertEqual(result, check)

    def test_encode_obj(self):
        val_dict = dict(desc='hello')
        result = self.x.encode_obj(val_dict)
        check = json.dumps(val_dict)
        self.assertEqual(result, check)

    def test_create_temp_dir_returns_temp_dir(self):
        result = self.x.create_temp_dir()
        self.assertIsInstance(result, tempfile.TemporaryDirectory)
        result.cleanup()

    def test_temp_dir_attribute_is_temp_dir(self):
        self.assertIsInstance(self.x.temp_dir, tempfile.TemporaryDirectory)

    def test_close_temp_dir_calls_close_on_temp_dir(self):
        try:
            self.x.close_temp_dir()
        except:
            self.assertTrue(False)

    def test_close_temp_dir_called_by_del(self):
        target = self.x.close_temp_dir = MagicMock()
        self.x.__del__()
        target.assert_called_with()
        self.x.temp_dir.cleanup()

    def test_temp_dir_name_attribute_is_temp_dir_name(self):
        self.assertEqual(self.x.temp_dir_name, self.x.temp_dir.name)

    def test_import_pubkey_to_keyring_imports_key_from_data_record(self):
        target = self.x.key_ring = MagicMock()
        result = self.x.import_pubkey_to_keyring()
        target.import_key.assert_called_once_with(self.x.request_data_record.gpg_pub_key)

    def test_import_pubkey_to_keyring_sets_target_fingerprint_on_valid(self):
        result = self.x.import_pubkey_to_keyring()
        self.assertEqual(result.fingerprints[0], self.x.target_fingerprint)

    def test_import_pubkey_to_keyring_calls_set_error_on_NOT_valid(self):
        target = self.x.set_error = MagicMock()
        self.x.request_data_record.gpg_pub_key = 'xxx'
        result = self.x.import_pubkey_to_keyring()
        self.assertTrue(target.called)

    def test_construct_data_dict_method_sets_data_dict_and_nonce(self):
        sub = self.x.random_hash = MagicMock(return_value='12345')
        data_dict = dict(address_host=self.x.message_server_address,
                         address_port=self.x.message_server_port,
                         response_nonce=self.x.random_hash(),
                         request_nonce=self.x.request_data_record.nonce)
        result = self.x.construct_data_dict()
        self.assertEqual(self.x.data_dict, data_dict)
        self.assertEqual(result, data_dict)
        self.assertEqual(self.x.response_nonce, data_dict['response_nonce'])

    def test_encode_data_dict_encodes_data_dict_sets_attribute(self):
        sub = self.x.random_hash = MagicMock(return_value='xxx')
        result = self.x.encode_data_dict()
        check = self.x.encode_obj(self.x.construct_data_dict())
        self.assertEqual(result, check)
        self.assertEqual(self.x.encoded_data_dict, check)

    @patch.object(contactresponsefactory.signer.Signer, 'execute')
    def test_sign_encoded_data_dict_calls_encode_data_dict(self, sub):
        target = self.x.encode_data_dict = MagicMock()
        self.x.sign_encoded_data_dict()
        target.assert_called_with()

    @patch.object(contactresponsefactory.signer.Signer, 'execute')
    def test_sign_encoded_data_dict_calls_signer_with_args(self, target):
        enc_return = 'hello'
        sub = self.x.encode_data_dict = MagicMock(return_value=enc_return)
        self.x.sign_encoded_data_dict()
        target.assert_called_with(sub.return_value, None, self.x.passphrase, detach=True)

    @patch.object(contactresponsefactory.signer.Signer, 'execute')
    def test_sign_encoded_data_dict_calls_set_error_on_error(self, sub):
        class MockBadResult:
            data = b''
            stderr = 'Mock Error'
        sub.return_value = MockBadResult()
        target = self.x.set_error = MagicMock()
        result = self.x.sign_encoded_data_dict()
        self.assertTrue(target.called)

    @patch.object(contactresponsefactory.signer.Signer, 'execute')
    def test_sign_encoded_data_dict_sets_returns_sig_dict_on_valid(self, sub):
        class MockGoodResult:
            data = b'xxx'
            stderr = 'Mock Error'

        sub.return_value = MockGoodResult()
        sub_encoded = self.x.encode_data_dict = MagicMock(return_value=dict())
        result = self.x.sign_encoded_data_dict()
        target = dict(sig=str(sub.return_value), data=sub_encoded.return_value)
        self.assertEqual(target, result)
        self.assertEqual(self.x.sig_dict, result)

    def test_encode_sig_dict_calls_sign_encoded_data_dict(self):
        sub = self.x.encode_obj = MagicMock()
        target = self.x.sign_encoded_data_dict = MagicMock()
        self.x.encode_sig_dict()
        target.assert_called_with()

    def test_encode_sig_dict_returns_none_if_error(self):
        self.x.error = 'Hello'
        result = self.x.encode_sig_dict()
        self.assertIsNone(result)

    def test_encoded_sig_dict_encodes_sig_dict_on_valid_sets_encoded_sig_dict(self):
        val = dict()
        sub = self.x.sign_encoded_data_dict = MagicMock(return_value=val)
        target = self.x.encode_obj = MagicMock(return_value='xxx')
        result = self.x.encode_sig_dict()
        target.assert_called_with(sub.return_value)
        self.assertEqual(self.x.encoded_sig_dict, target.return_value)
        self.assertEqual(result, self.x.encoded_sig_dict)

    @patch.object(contactresponsefactory.encrypter.Encrypter, 'execute')
    def test_encrypt_encoded_sig_dict_calls_encrypt_with_args(self, target):
        self.x.encrypt_encoded_sig_dict()
        target.assert_called_with(self.x.encoded_sig_dict, self.x.target_fingerprint)

    @patch.object(contactresponsefactory.encrypter.Encrypter, 'execute')
    def test_encrypt_encoded_sig_dict_sets_error_on_error(self, sub):
        class MockBadResult:
                ok = False
                stderr = 'Mock Error'
        sub.return_value = MockBadResult()
        target = self.x.set_error = MagicMock()
        self.x.encrypt_encoded_sig_dict()
        self.assertTrue(target.called)

    @patch.object(contactresponsefactory.encrypter.Encrypter, 'execute')
    def test_encrypt_encoded_sig_dict_builds_result_dict_on_valid(self, sub):
        class MockBadResult:
                ok = True
                stderr = 'Mock Error'
        sub.return_value = MockBadResult()
        result = self.x.encrypt_encoded_sig_dict()
        self.assertIsInstance(result, type({}))

    def test_build_calls_import_key(self):
        sub = self.x.encrypt_encoded_sig_dict = MagicMock()
        target = self.x.import_pubkey_to_keyring = MagicMock()
        self.x.build()
        self.assertTrue(target.called)

    def test_build_calls_encode_sig_dict(self):
        target = self.x.encode_sig_dict = MagicMock()
        self.x.build()
        self.assertTrue(target.called)

    @patch.object(contactresponsefactory.encrypter.Encrypter, 'execute')
    def test_build_calls_and_returns_encrypt_method_with_nonce(self, sub):
        target = self.x.encrypt_encoded_sig_dict = MagicMock(return_value=dict(ciphertext=''))
        result = self.x.build()
        final_dict = target.return_value
        final_dict['request_nonce'] = self.x.request_data_record.nonce
        final_dict['response_nonce'] = self.x.response_nonce
        check_return = (final_dict, self.x.response_nonce)
        self.assertTrue(target.called)
        self.assertEqual(result, check_return)

    @patch.object(contactresponsefactory.encrypter.Encrypter, 'execute')
    def test_build_sets_valid_true_if_error_none(self, sub):
        target = self.x.encrypt_encoded_sig_dict = MagicMock(return_value=dict())
        self.x.error = None
        result = self.x.build()
        self.assertTrue(self.x.valid)


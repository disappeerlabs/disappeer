"""
test_newmessagefactory.py

Test suite for NewMessageFactory class object, for generating new message payload dicts

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net.message import messagefactory
from disappeer.gpg.agents import signer
from disappeer.gpg.helpers import tempkeyring
from disappeer.gpg.agents import encrypter
from disappeer import settings
import hashlib
import random
import sys
import json
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

    def test_settings(self):
        self.assertEqual(settings, messagefactory.settings)

    def test_hashlib(self):
        self.assertEqual(hashlib, messagefactory.hashlib)

    def test_random(self):
        self.assertEqual(random, messagefactory.random)

    def test_sys(self):
        self.assertEqual(sys, messagefactory.sys)

    def test_json(self):
        self.assertEqual(json, messagefactory.json)

    def test_signer(self):
        self.assertEqual(signer, messagefactory.signer)

    def test_tempkeyring(self):
        self.assertEqual(tempkeyring, messagefactory.tempkeyring)

    def test_encrypter(self):
        self.assertEqual(encrypter, messagefactory.encrypter)


class TestClassBasics(unittest.TestCase):
    hello = 'hello'
    target_file = settings.gpg_host_pubkey
    message_server_host_address = 'address.onion'
    key_home_dir = 'tests/data/keys/'
    recipient_gpg_pub_key = gpg_pub_key_string
    host_fingerprint = 'host_fingerprint_string'
    message_text = 'hello world'
    passphrase = 'passphrase'
    valid_obj = messagefactory.MessageFactory(message_server_host_address,
                                           key_home_dir,
                                           recipient_gpg_pub_key,
                                           host_fingerprint,
                                           message_text,
                                           passphrase)

    def setUp(self):
        self.x = copy.deepcopy(self.valid_obj)

    def test_instance(self):
        self.assertIsInstance(self.x, messagefactory.MessageFactory)

    def test_message_server_host_address_attribute_set(self):
        self.assertEqual(self.message_server_host_address, self.x.message_server_host_address)

    def test_message_server_port_attribute_set(self):
        self.assertEqual(settings.port_message_server, self.x.message_server_host_port)

    def test_key_home_dir_attribute_set(self):
        self.assertEqual(self.x.key_home_dir, self.key_home_dir)

    def test_peer_pub_key_attribute_set(self):
        self.assertEqual(self.x.peer_gpg_pub_key, self.recipient_gpg_pub_key)

    def test_host_fingerprint_attribute_set(self):
        self.assertEqual(self.x.host_fingerprint, self.host_fingerprint)

    def test_message_text_attribute_set(self):
        self.assertEqual(self.x.message_text, self.message_text)

    def test_passphrase_attr_set(self):
        self.assertEqual(self.x.passphrase, self.passphrase)

    def test_nonce_attribute_set_none(self):
        self.assertIsNone(self.x.nonce)

    def test_data_dict_set_none(self):
        self.assertIsNone(self.x.data_dict)

    def test_sig_dict_attribute_set_none(self):
        self.assertIsNone(self.x.sig_dict)

    def test_ciphertext_dict_attribute_set_none(self):
        self.assertIsNone(self.x.ciphertext_dict)

    def test_target_fingerprint_attribute_set_none(self):
        self.assertIsNone(self.x.target_fingerprint)

    def test_error_attribute_set_none(self):
        self.assertIsNone(self.x.error)

    def test_valid_attribute_set_none(self):
        self.assertIsNone(self.x.valid)

    def test_gpg_signer_attribute_set(self):
        self.assertIsInstance(self.x.gpgsigner, signer.Signer)
        self.assertEqual(self.x.gpgsigner.home, self.x.key_home_dir)

    def test_temp_keyring_attribute_is_temp_keyring(self):
        self.assertIsInstance(self.x.temp_keyring, tempkeyring.TempKeyRing)

    def test_encypt_agent_is_encrypter_with_key_home_dir(self):
        self.assertIsInstance(self.x.encrypt_agent, encrypter.Encrypter)
        self.assertEqual(self.x.encrypt_agent.home, self.x.key_home_dir)


    def test_set_error_method_sets_error_and_valid(self):
        msg = 'Error Message'
        self.x.set_error(msg)
        self.assertEqual(self.x.error, msg)
        self.assertIs(self.x.valid, False)

    def test_hash_message_method_returns_hash(self):
        check = 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
        result = self.x.hash_message(self.hello)
        self.assertEqual(result, check)

    @patch('disappeer.net.message.messagefactory.random')
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

    def test_construct_data_dict_method_constructs_dict_sets_dict_and_nonce_returns_encoded(self):
        sub = self.x.random_hash = MagicMock(return_value='12345')
        data_dict = dict(address_host=self.x.message_server_host_address,
                         address_port=self.x.message_server_host_port,
                         nonce=self.x.random_hash(),
                         sent_to=self.x.import_pubkey_to_temp_keyring(),
                         sent_from=self.x.host_fingerprint,
                         message=self.message_text)
        result = self.x.construct_data_dict()
        self.assertEqual(self.x.data_dict, data_dict)
        self.assertEqual(self.x.nonce, sub.return_value)
        self.assertEqual(result, self.x.encode_obj(data_dict))

    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_construct_sig_dict_calls_signer_with_args(self, target):
        arg = 'hello'
        self.x.construct_sig_dict(arg)
        target.assert_called_with(arg, None, self.x.passphrase, detach=True)

    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_construct_sig_dict_calls_set_error_returns_false_on_error(self, sub):
        class MockBadResult:
            data = b''
            stderr = 'Mock Error'
        sub.return_value = MockBadResult()
        target = self.x.set_error = MagicMock()
        result = self.x.construct_sig_dict('xxxxxxxx')
        self.assertTrue(target.called)
        self.assertIs(result, False)

    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_construct_sig_dict_sets_returns_encoded_sig_dict_on_valid(self, sub):
        class MockGoodResult:
            data = b'xxx'
            stderr = 'Mock Error'

        data_obj = 'xxxx'
        sub.return_value = MockGoodResult()
        result = self.x.construct_sig_dict(data_obj)
        target = dict(sig=str(sub.return_value), data=data_obj)
        self.assertEqual(result, self.x.encode_obj(target))
        self.assertEqual(self.x.sig_dict, target)

    def test_import_pubkey_to_temp_keyring_imports_peer_pub_key(self):
        target = self.x.temp_keyring = MagicMock()
        result = self.x.import_pubkey_to_temp_keyring()
        target.key_ring.import_key.assert_called_once_with(self.x.peer_gpg_pub_key)

    def test_import_pubkey_to_temp_keyring_sets_and_returns_target_fingerprint_on_valid(self):
        result = self.x.import_pubkey_to_temp_keyring()
        self.assertEqual(result, self.x.target_fingerprint)

    def test_import_pubkey_to_keyring_calls_set_error_on_NOT_valid_returns_false(self):
        target = self.x.set_error = MagicMock()
        self.x.peer_gpg_pub_key = 'xxx'
        result = self.x.import_pubkey_to_temp_keyring()
        self.assertTrue(target.called)
        self.assertIs(result, False)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    def test_construct_ciphertext_dict_calls_encrypter_with_args(self, target):
        plaintext = 'hello'
        fingerprint = 'dwevwe'
        self.x.construct_ciphertext_dict(plaintext, fingerprint)
        target.assert_called_with(plaintext, fingerprint)


    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    def test_construct_ciphertext_dict_sets_error_on_error_returns_false(self, sub):
        class MockBadResult:
                ok = False
                stderr = 'Mock Error'
        sub.return_value = MockBadResult()
        target = self.x.set_error = MagicMock()
        result = self.x.construct_ciphertext_dict('xxx', 'yyyy')
        self.assertTrue(target.called)
        self.assertIs(result, False)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    def test_construct_ciphertext_dict_returns_dict_sets_ciphertext_dict_on_valid(self, sub):
        class MockBadResult:
                ok = True
                stderr = 'Mock Error'
        sub.return_value = MockBadResult()
        target_result = dict(ciphertext=str(sub.return_value))
        result = self.x.construct_ciphertext_dict('xxx', 'yyy')
        self.assertIsInstance(result, type({}))
        self.assertEqual(result, target_result)
        self.assertEqual(self.x.ciphertext_dict, result)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_calls_construct_data_dict(self, mock_signer, mock_encrypter):
        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        self.x.build()
        sub.assert_called_with()

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_calls_construct_sig_dict_with_data_dict_result(self, mock_signer, mock_encrypter):
        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        target = self.x.construct_sig_dict = MagicMock()
        self.x.build()
        target.assert_called_with(sub.return_value)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_returns_false_if_sig_dict_false(self, mock_signer, mock_encrypter):
        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        target = self.x.construct_sig_dict = MagicMock(return_value=False)
        result = self.x.build()
        self.assertIs(result, False)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_calls_import_pubkey_method(self, mock_signer, mock_encrypter):
        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        sub_1 = self.x.construct_sig_dict = MagicMock()
        target = self.x.import_pubkey_to_temp_keyring = MagicMock()
        self.x.build()
        target.assert_called_with()

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_returns_false_if_import_pubkey_method_false(self, mock_signer, mock_encrypter):
        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        sub_1 = self.x.construct_sig_dict = MagicMock()
        target = self.x.import_pubkey_to_temp_keyring = MagicMock(return_value=False)
        result = self.x.build()
        self.assertIs(result, False)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_calls_encrypt_method(self, mock_signer, mock_encrypter):
        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        sub_1 = self.x.construct_sig_dict = MagicMock(return_value='zzzz')
        fingerprint = 'xxxx'
        sub_2 = self.x.import_pubkey_to_temp_keyring = MagicMock(return_value=fingerprint)
        target_encrypt_fingerprints = [self.x.host_fingerprint, sub_2.return_value]
        self.x.build()
        mock_encrypter.assert_called_with(sub_1.return_value, target_encrypt_fingerprints)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_returns_false_if_encrypt_method_returns_false(self, mock_signer, mock_encrypter):
        class MockBadResult:
                ok = False
                stderr = 'Mock Error'

        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        sub_1 = self.x.construct_sig_dict = MagicMock()
        fingerprint = 'xxxx'
        sub_2 = self.x.import_pubkey_to_temp_keyring = MagicMock(return_value=fingerprint)
        mock_encrypter.return_value = MockBadResult()
        result = self.x.build()
        self.assertIs(result, False)

    @patch.object(messagefactory.encrypter.Encrypter, 'execute')
    @patch.object(messagefactory.signer.Signer, 'execute')
    def test_build_method_returns_final_dict_with_nonce_sets_valid(self, mock_signer, mock_encrypter):
        data_dict_return = MagicMock()
        sub = self.x.construct_data_dict = MagicMock(return_value=data_dict_return)
        sub_1 = self.x.construct_sig_dict = MagicMock()
        fingerprint = 'xxxx'
        sub_2 = self.x.import_pubkey_to_temp_keyring = MagicMock(return_value=fingerprint)
        sub_3 = self.x.construct_ciphertext_dict = MagicMock(return_value=dict(ciphertext=''))
        result = self.x.build()
        target_keys = ['ciphertext', 'nonce']
        for item in target_keys:
            self.assertTrue(item in result)
        self.assertTrue(self.x.valid)


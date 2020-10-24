"""
test_messagevalidator.py

Test suite for the MessageValidator module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.net.message import messagevalidator
from disappeer.net.message import messagefactory
from disappeer.gpg.agents import encrypter
from disappeer.gpg.agents import decrypter
from disappeer.gpg.agents import detachedverifier
from disappeer.gpg.agents import keyring
from disappeer.gpg.agents import signer
import json
import tempfile
import copy


class TestImports(unittest.TestCase):

    def test_decrypter(self):
        self.assertEqual(decrypter, messagevalidator.decrypter)

    def test_json(self):
        self.assertEqual(json, messagevalidator.json)

    def test_detachedverifier(self):
        self.assertEqual(detachedverifier, messagevalidator.detachedverifier)

    def test_tempfile(self):
        self.assertEqual(tempfile, messagevalidator.tempfile)


gpg_pub_key_string = '''-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBFrSHN0BCAC6dvkCAP8T/ytfe8s6CBe1rJOSLDjoha++Kl3G93SA2WHbcUmc
7Zg0xFkKo0XEZYdJlmNse0qS4zIlBdsNfJB3FJvYKK5gFGGA7u6xA1QBRiKTuhJM
P+MdoGSbmfsRi4Mxf9suHWvRYVkHjApNRcfqO5ahomwpYd6le26MrYPp7MutWdHX
AA05+ohMwBBWIn5ZCvchvU/1I4S53J2YxGmmQOFZl9FsbYl3jdrQz3QxYaZgHi03
8ugBEXqgrKnEHU2GJ9KQOXpd1AvKkDRVyo/A38OBfUTWYnEkf1HJ+PL21OeHijCL
5lvp+MlNV2phTRvV7XfCVp9z4sFH0r5dgVgFABEBAAG0J2FsaWNlIChpbiB3b25k
ZXJsYW5kKSA8YWxpY2VAZW1haWwuY29tPokBPgQTAQgAKAUCWtIc3QIbLwUJEr4z
4wYLCQgHAwIGFQgCCQoLBBYCAwECHgECF4AACgkQGQ21KVmsNWC5Twf/ZhgpVGFA
0CyYHZp2rqf7EVvSCPOQbukyl3kPbrAyzk+XJNT0TPcVBcCGx0JFAbWoay3vMULV
fdHJJZDm6RqQ0bEGmEJJeq70q1aMeDu6yEY+uyvRemzRVfjqDLL+mvTOo1foXufY
LPK07E0Ws7sflWkLwfQde6j0nXFQaID6ScHTZ45YqgD8CWuJxMxb/BpBEFZYdQ34
CLCrFiaCCehu9WyQoZSVxHYcsZJMJcRjZKLDO2yoM5SHLHPZQXJq9ZPHqGh0BYWU
FZtM8DCLepLXrRU7buiZ73eBhA5k2AGlwuVpxx14fuLsGHA/M+7LM1oaiGUGioFV
Iesp2aGV54m5c7kCDQRa0hzdEAgArVGcrj+shJc9K+lo0mXf6J33AbM4GUJ2eDq4
VSpO3DO5KGs9mal9QAznNbONRvgYZqn/sCDwlxkyNd+skqnma6A0c8gxNEacuw8B
J6y5IVBA3dm7c2tW0YcG3mQaET1/6SuCUm9UGZS6zy/9YJbTMNKkaqTCwv0lwLWn
Sg6ZNRi8qgNTTwrZ53IwME0ns5hWaidera9OVqEdFPGOVioUJKgDh3InQdzNakCS
hblzzMqxp/brA+bWQt8jWOkaPkiYTyyP0InByqKJoz4Rj+5ltdgac9cSfpNfLvH0
dqWrSXKJtew2L/LLvbToqJahz7viyu2TiN00+CFU9tqt5evXxwADBQf+J+I0P7ic
TJaYnrcve8sl+cHvi2m0e+e/wj9LmRaG1GlO0LVw8tgzE3AnOJq585CqUzf8qASv
Ns082TKI+iNlxmqTD+oi4UbwoKpF28ekH7e+dQUTkWWfJkfkSI7rJsngIeR0qkP4
T0qY/rabKXwSYNB8YziZ18uc1wDyhQ/RV4MnvNlLzQzJW+ckAa/ZNP6Vyts+w7/T
29nuP9azvqDvhsPPQXFZ/Z7udqbXYhsOeYwHwV5Ko1frgyFbSHxxluYgVZBh3lus
6ZMvvA3SOjcMwOLcFKW9PY3qBGKmPW0G0XQ68QZ7jhsYBrNVqZKIiNZft3ogmjTl
+yDn2EarBFeybYkBJQQYAQgADwUCWtIc3QIbDAUJEr4z4wAKCRAZDbUpWaw1YBgO
B/9i2HPg93ZNjsNlE1OMSmWT7YtejbFA1bEi+MQJyVBW49cwtpiae3dfrlgWb1d7
pJuzeC+UDa2Bv7EYEln1VfEv/SXzLWPH7XV2qndqqKz/Z2pbRPDf5ebR7dAFAIu9
toAbpHriptBi/ffNGWCDpA5AAO+Pa26Tl7rFueNpBAwcyJiDS7naPjnCUOlgGs43
EbIrALfUqcCaIwKaiJqn6b1fOq2lyZZrJ98OEE18fGoEELY+bzh/sSLEHaRAbC4w
R3pJgCsfXVV9JuwcZX4tIna6qs+TUwUydeXJ7FF67hOx8qjLm0ycH/YSCwNbRzFB
WB1lW8Sh/WYHghZrk4xqiE9t
=6s/b
-----END PGP PUBLIC KEY BLOCK-----'''



def build_valid_message_payload_with_factory():
    host_addr = 'host_addr_string'
    key_dir = 'tests/data/keys'
    message = "Hello world"
    host_key_fingerprint = 'AA74BBFE8A31ADBC0E9ED26B190DB52959AC3560'
    passphrase = 'passphrase'
    factory = messagefactory.MessageFactory(host_addr, key_dir, gpg_pub_key_string, host_key_fingerprint, message, passphrase)
    result = factory.build()
    return result


class TestClassBasics(unittest.TestCase):
    """
    Set everything up as class attributes, then copy the class instance in setup, this is much faster to run.
    """

    message = "Hello world"
    key_dir = 'tests/data/keys'
    key_ring = keyring.KeyRing(key_dir)
    encrypt_agent = encrypter.Encrypter(key_dir)
    encrypted_msg = str(encrypt_agent.execute(message, '190DB52959AC3560'))
    mock_valid_payload = dict(ciphertext=encrypted_msg, nonce='nonce_string')
    gpg_signer = signer.Signer(key_dir)
    valid_sig = gpg_signer.execute(message, None, 'passphrase', detach=True)
    valid_sig_dict = dict(sig=str(valid_sig), data=message)
    passphrase = 'passphrase'
    valid_obj = messagevalidator.MessageValidator(mock_valid_payload, key_dir, passphrase)

    def setUp(self):
        self.x = copy.deepcopy(self.valid_obj)

    def test_instance(self):
        self.assertIsInstance(self.x, messagevalidator.MessageValidator)

    def test_target_payload_attribute_set(self):
        self.assertEqual(self.x.message_payload, self.mock_valid_payload)

    def test_key_dir_attribute_set(self):
        self.assertEqual(self.x.key_dir, self.key_dir)

    def test_passphrase_attr_set(self):
        self.assertEqual(self.x.passphrase, self.passphrase)

    def test_error_attribute_set_none(self):
        self.assertIsNone(self.x.error)

    def test_valid_attribute_set_none(self):
        self.assertIsNone(self.x.valid)

    def test_data_dict_attribute_set_none(self):
        self.assertIsNone(self.x.data_dict)

    def test_verify_result_attribute_set_none(self):
        self.assertIsNone(self.x.verify_result)

    def test_gpg_verifier_attribute_is_verifier_home_set(self):
        self.assertIsInstance(self.x.gpg_verifier, detachedverifier.DetachedVerifier)
        self.assertEqual(self.x.key_dir, self.x.gpg_verifier.home)

    def test_set_error_method_sets_error_and_valid(self):
        msg = 'Error Message'
        self.x.set_error(msg)
        self.assertEqual(self.x.error, msg)
        self.assertIs(self.x.valid, False)

    def test_check_payload_keys_method_checks_payload_keys_sets_attributes(self):
        result = self.x.check_payload_keys(self.x.message_payload)
        self.assertIs(result, True)

    def test_check_payload_keys_method_returns_false_on_invalid_dict(self):
        bad_dict = dict()
        result = self.x.check_payload_keys(bad_dict)
        self.assertIs(result, False)

    def test_check_payload_keys_method_returns_false_on_bad_data(self):
        bad_data = 'xxx'
        result = self.x.check_payload_keys(bad_data)
        self.assertIs(result, False)

    @patch('net.message.messagevalidator.decrypter.Decrypter')
    def test_decrypt_ciphertext_method_calls_decrypter_with_key_dir(self, target):
        mock_ciphertext = 'xxx'
        self.x.decrypt_ciphertext(mock_ciphertext)
        target.assert_called_with(self.x.key_dir)

    @patch.object(messagevalidator.decrypter.Decrypter, 'execute')
    def test_decrypt_ciphertext_calls_execute_with_args(self, target):
        passphrase = 'passphrase'
        self.x.decrypt_ciphertext(self.encrypted_msg)
        target.assert_called_with(self.encrypted_msg, self.passphrase)

    @patch.object(messagevalidator.decrypter.Decrypter, 'execute')
    def test_decrypt_ciphertext_sets_error_returns_false_if_bad_response(self, sub):
        class MockBadResult:
            ok = False
            status = 'status_message'
        sub.return_value = MockBadResult()
        passphrase = 'passphrase'
        target = self.x.set_error = MagicMock()
        result = self.x.decrypt_ciphertext(self.encrypted_msg)
        target.assert_called_with(MockBadResult.status)
        self.assertIs(result, False)

    @patch.object(messagevalidator.decrypter.Decrypter, 'execute')
    def test_decrypt_ciphertext_returns_plaintext_on_valid_result(self, sub):
        class MockBadResult:
            ok = True
            status = 'status_message'
        sub.return_value = MockBadResult()
        passphrase = 'passphrase'
        result = self.x.decrypt_ciphertext(self.encrypted_msg)
        self.assertEqual(result, str(sub.return_value))

    def test_decode_json_decodes_returns_valid_json(self):
        msg_dict = dict(msg='hello world')
        encoded = json.dumps(msg_dict)
        result = self.x.decode_json_string(encoded)
        self.assertEqual(result, msg_dict)

    def test_decode_json_returns_false_on_invalid(self):
        msg_dict = dict(msg='hello world')
        result = self.x.decode_json_string(msg_dict)
        self.assertIs(result, False)

    def test_check_sig_dict_keys_returns_true_on_valid(self):
        sig_dict = dict(sig='sig', data='data')
        result = self.x.check_sig_dict_keys(sig_dict)
        self.assertIs(result, True)

    def test_check_sig_dict_keys_returns_false_on_invalid(self):
        sig_dict = dict(xxx='sig', data='data')
        result = self.x.check_sig_dict_keys(sig_dict)
        self.assertIs(result, False)

    def test_check_sig_dict_keys_returns_false_on_bad_input(self):
        bad = 123
        result = self.x.check_sig_dict_keys(bad)
        self.assertIs(result, False)

    def test_verify_sig_dict_verifies_valid_sig_dict_returns_true(self):
        result = self.x.verify_sig_dict(self.valid_sig_dict)
        self.assertIs(result, True)

    def test_verify_sig_dict_sets_error_returns_false_on_invalid(self):
        sig_dict = dict(sig='sig', data='data')
        target = self.x.set_error = MagicMock()
        result = self.x.verify_sig_dict(sig_dict)
        self.assertIs(result, False)
        self.assertTrue(target.called)

    def test_verify_sig_dict_sets_verify_result_attribute(self):
        result = self.x.verify_sig_dict(self.valid_sig_dict)
        self.assertIsNotNone(self.x.verify_result)

    def test_check_data_dict_keys_returns_true_on_valid(self):
        data_dict = dict(address_host='host-string',
                         address_port='port_string',
                         nonce='nonce_string',
                         message='message_string')
        result = self.x.check_data_dict_keys(data_dict)
        self.assertTrue(result)

    def test_check_data_dict_keys_returns_false_on_not_valid(self):
        data_dict = dict(xxxx='host-string',
                         address_port='port_string',
                         nonce='nonce_string',
                         message='message_string')
        result = self.x.check_data_dict_keys(data_dict)
        self.assertIs(result, False)

    def test_validate_calls_check_payload_keys_returns_false_if_false_and_sets_error(self):
        target_1 = self.x.check_payload_keys = MagicMock(return_value=False)
        target_2 = self.x.set_error = MagicMock()
        result = self.x.validate()
        target_1.assert_called_with(self.x.message_payload)
        self.assertTrue(target_2.called)
        self.assertIs(result, False)

    def test_validate_calls_decrypt_ciphertext_returns_false_if_false(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value=False)
        result = self.x.validate()
        decrypt_method_mock.assert_called_with(self.x.message_payload['ciphertext'])
        self.assertIs(result, False)

    def test_validate_calls_json_decode_if_decrypt_not_false(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock()
        result = self.x.validate()
        json_decode_mock.assert_any_call(decrypt_method_mock.return_value)

    def test_validate_sets_error_returns_false_if_json_decode_of_decrypt_is_false(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value=False)
        result = self.x.validate()
        self.assertTrue(set_error_mock.called)
        self.assertIs(result, False)

    def test_validate_calls_check_sig_dict_keys_if_json_decode_of_decrypt_not_false(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value=self.valid_sig_dict)
        verify_sig_mock = self.x.verify_sig_dict = MagicMock()
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock()
        result = self.x.validate()
        self.assertTrue(check_sig_dict_keys_mock.called)

    def test_validate_sets_error_returns_false_if_sig_dict_key_check_returns_false(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value='xxxx')
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock(return_value=False)
        result = self.x.validate()
        self.assertTrue(set_error_mock.called)
        self.assertIs(result, False)

    def test_validate_calls_verify_sig_dict_with_sig_dict_if_sig_dict_keys_valid(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value=self.valid_sig_dict)
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        verify_sig_mock = self.x.verify_sig_dict = MagicMock()
        result = self.x.validate()
        self.assertTrue(verify_sig_mock.called)

    def test_validate_returns_false_if_verify_sig_dict_is_false(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value='xxxx')
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        verify_sig_mock = self.x.verify_sig_dict = MagicMock(return_value=False)
        result = self.x.validate()
        self.assertIs(result, False)

    def test_validate_decodes_data_dict_string(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value=self.valid_sig_dict)
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        verify_sig_mock = self.x.verify_sig_dict = MagicMock(return_value=True)
        result = self.x.validate()
        json_decode_mock.assert_any_call(json_decode_mock.return_value['data'])

    def test_validate_calls_check_data_keys_if_verify_sig_is_true(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value=self.valid_sig_dict)
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        verify_sig_mock = self.x.verify_sig_dict = MagicMock(return_value=True)
        check_data_keys_mock = self.x.check_data_dict_keys = MagicMock()
        result = self.x.validate()
        self.assertTrue(check_data_keys_mock.called)

    def test_validate_sets_error_returns_false_if_data_dict_check_is_false(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value=self.valid_sig_dict)
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        verify_sig_mock = self.x.verify_sig_dict = MagicMock(return_value=True)
        check_data_keys_mock = self.x.check_data_dict_keys = MagicMock(return_value=False)
        result = self.x.validate()
        self.assertTrue(set_error_mock.called)
        self.assertIs(result, False)

    def test_validate_sets_valid_true_sets_data_dict_attribute_if_data_dict_check_true(self):
        check_payload_key_mock = self.x.check_payload_keys = MagicMock(return_value=True)
        set_error_mock = self.x.set_error = MagicMock()
        decrypt_method_mock = self.x.decrypt_ciphertext = MagicMock(return_value='xxxxx')
        json_decode_mock = self.x.decode_json_string = MagicMock(return_value=self.valid_sig_dict)
        check_sig_dict_keys_mock = self.x.check_sig_dict_keys = MagicMock(return_value=True)
        verify_sig_mock = self.x.verify_sig_dict = MagicMock(return_value=True)
        check_data_keys_mock = self.x.check_data_dict_keys = MagicMock(return_value=True)
        result = self.x.validate()
        self.assertTrue(self.x.valid)
        self.assertIs(result, True)
        self.assertIsNotNone(self.x.data_dict)

    def test_with_valid_message_from_factory(self):
        msg_dict = build_valid_message_payload_with_factory()
        validator = messagevalidator.MessageValidator(msg_dict, self.key_dir, self.passphrase)
        result = validator.validate()
        self.assertIs(result, True)



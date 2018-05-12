"""
test_keyring.py

Test suite for the KeyRing module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from disappeer.gpg.agents import keyring
import gnupg
from disappeer.gpg.agents import gpgagent


class TestImports(unittest.TestCase):

    def test_gpg_agent_import(self):
        self.assertEqual(gpgagent, keyring.gpgagent)


class TestKeyRing(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.k = keyring.KeyRing(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.k, keyring.KeyRing)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.k, gpgagent.GPGAgent)

    def test_keydir_attribute(self):
        self.assertEqual(self.keydir, self.k.home)

    def test_gpg_attribute(self):
        self.assertIsInstance(self.k.gpg, gnupg.GPG)


class TestKeyRingGetGPGMethod(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.k = keyring.KeyRing(self.keydir)

    def test_get_gpg_obj_result_instance(self):
        result = self.k.get_gpg_obj()
        self.assertIsInstance(result, gnupg.GPG)

    def test_get_gpg_obj_result_home_attr(self):
        result = self.k.get_gpg_obj()
        self.assertEqual(result.gnupghome, self.keydir)

    def test_get_gpg_obj_result_encoding_attr(self):
        result = self.k.get_gpg_obj()
        self.assertEqual(result.encoding, 'utf-8')


class TestKeyRingMethods(unittest.TestCase):

    def setUp(self):
        self.keydir = "tests/data/keys"
        self.alt = "tests/data/altkeys"
        self.mal = {'type': 'pub',
                    'trust': 'u',
                    'length': '2048',
                    'algo': '1',
                    'keyid': '190DB52959AC3560',
                    'date': '1523719389',
                    'expires': '1838174400',
                    'dummy': '',
                    'ownertrust': 'u',
                    'sig': '',
                    'uids': ['alice (in wonderland) <alice@email.com>'],
                    'sigs': [],
                    'subkeys': [['A58D508E0BE72B6D', 'e', 'AD7C46A3E9C993F2F174120CA58D508E0BE72B6D']],
                    'fingerprint': 'AA74BBFE8A31ADBC0E9ED26B190DB52959AC3560'}
        self.k = keyring.KeyRing(self.keydir)

    def test_attribute_get_key_list(self):
        name = 'get_raw_key_list'
        result = hasattr(self.k, name)
        self.assertTrue(result)

    def test_get_key_list_returns_list(self):
        result = self.k.get_raw_key_list()
        self.assertIsInstance(result, gnupg.ListKeys)

    def test_result_get_raw_key_list(self):
        result = self.k.get_raw_key_list()
        target_fingerprints = [d['fingerprint'] for d in result]
        self.assertIn(self.mal['fingerprint'], target_fingerprints)

    def test_result_get_raw_key_list_secret(self):
        result = self.k.get_raw_key_list(secret=True)
        final = result[0]
        self.assertEqual(final['type'], 'sec')

    def test_attribute_export_method(self):
        name = 'export_key'
        check = hasattr(self.k, name)
        self.assertTrue(check)

    def test_result_export_method_fingerprint_valid(self):
        result = self.k.export_key(self.mal['fingerprint'])
        self.assertIn("PUBLIC KEY BLOCK", result)

    def test_result_export_method_fingerprint_not_valid(self):
        result = self.k.export_key('XXX666')
        self.assertEqual(0, len(result))

    def test_attribute_import_method(self):
        name = 'import_key'
        check = hasattr(self.k, name)
        self.assertTrue(check)

    def test_result_import_method_valid(self):
        pub_key = self.k.export_key(self.mal['fingerprint'])
        import tempfile
        with tempfile.TemporaryDirectory() as temp_home_dir:
            k = keyring.KeyRing(temp_home_dir)
            result = k.import_key(pub_key)
            self.assertTrue(result.count > 0)

    def test_result_import_method_not_valid(self):
        pub_key = 'xxx666'
        import tempfile
        with tempfile.TemporaryDirectory() as temp_home_dir:
            k = keyring.KeyRing(temp_home_dir)
            result = k.import_key(pub_key)
            self.assertTrue(result.count == 0)
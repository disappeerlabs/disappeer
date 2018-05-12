"""
test_gpgpubkeyvalidator.py

Test suite for GPGPubKeyValidator class object and module.
Module takes gpg pubkey as input, imports to tempdir, validates.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.gpg.helpers import gpgpubkeyvalidator
from disappeer.gpg.agents import keyring
import tempfile
import copy


valid_pubkey = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
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

    def test_keyring(self):
        self.assertEqual(keyring, gpgpubkeyvalidator.keyring)

    def test_tempfile(self):
        self.assertEqual(tempfile, gpgpubkeyvalidator.tempfile)


class TestClassBasics(unittest.TestCase):

    valid_obj = gpgpubkeyvalidator.GPGPubKeyValidator(valid_pubkey)

    def setUp(self):
        self.valid_pubkey = valid_pubkey
        self.invalid_pubkey = 'xxxxx'
        self.x = copy.deepcopy(self.valid_obj) # gpgpubkeyvalidator.GPGPubKeyValidator(self.valid_pubkey)

    def test_instance(self):
        self.assertIsInstance(self.x, gpgpubkeyvalidator.GPGPubKeyValidator)

    def test_target_pub_key_attribute_set(self):
        self.assertEqual(self.x.target_pubkey, self.valid_pubkey)

    def test_valid_attribute_set(self):
        name = 'valid'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_result_attribute_set(self):
        name = 'result'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_key_dict_attribute_set(self):
        name = 'key_dict'
        check = hasattr(self.x, name)
        self.assertTrue(check)

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

    def test_key_ring_attribute_is_keyring_with_temp_dir(self):
        self.assertIsInstance(self.x.key_ring, keyring.KeyRing)
        self.assertEqual(self.x.key_ring.home, self.x.temp_dir_name)

    def test_import_pubkey_to_keyring_imports_key_from_data_record(self):
        result = self.x.import_pubkey_to_keyring()
        self.assertEqual(result.count, 1)

    def test_import_pubkey_to_keyring_sets_result_to_attribute(self):
        result = self.x.import_pubkey_to_keyring()
        self.assertEqual(self.x.result, result)

    def test_validate_calls_import_method(self):
        class MockResult:
            count = 1
        self.x.result = MockResult()
        target = self.x.import_pubkey_to_keyring = MagicMock()
        self.x.key_ring.get_raw_key_list = MagicMock(return_value=[123])
        self.x.validate()
        target.assert_called_with()

    def test_validate_sets_valid_true_on_valid_import(self):
        self.x.validate()
        self.assertTrue(self.x.valid)

    def test_validate_sets_valid_false_on_INVALID_input(self):
        x = gpgpubkeyvalidator.GPGPubKeyValidator(self.invalid_pubkey)
        x.validate()
        self.assertIs(x.valid, False)

    def test_validate_sets_key_dict_on_valid(self):
        self.x.validate()
        target = self.x.key_ring.get_raw_key_list()[0]
        self.assertEqual(target, self.x.key_dict)

    def test_validate_called_by_init(self):
        self.assertIsNotNone(self.x.valid)



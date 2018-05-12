"""
gpgcontrollersetupclass.py

Primary setup class for GPG Controller test cases

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import tkinter
from disappeer.models.db import databasefacade
from disappeer.root import rootparameters
from disappeer.models import gpgdatacontext
from disappeer.gpg import gpgcontroller
import time
import copy


class TestGPGControllerSetupClass(unittest.TestCase):
    command = "<ButtonRelease-1>"
    root = tkinter.Tk()
    root_view = MagicMock()
    queue = MagicMock()
    database_facade = MagicMock(spec=databasefacade.DatabaseFacade)
    mock_observer = MagicMock()
    root_params = rootparameters.RootParameters(root, root_view, queue, database_facade, mock_observer)
    mock_view_method = root_params.get_gpg_frame = MagicMock(return_value=MagicMock())
    view = mock_view_method.return_value

    key_dir = 'tests/data/keys'
    data_context = gpgdatacontext.GPGDataContext(key_dir)

    def setUp(self):
        self.data_context = copy.deepcopy(self.data_context)
        self.x = gpgcontroller.GPGController(self.root_params,
                                             self.data_context)

    def altsetup(self):
        x = gpgcontroller.GPGController(self.root_params,
                                        self.data_context)
        return x


"""
rootsetupclass.py

Helper class for RootController setup

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import time
import tkinter
from disappeer.root import rootcontroller
from disappeer.root import rootview
from disappeer.utilities import dirmaker
from disappeer import settings
from disappeer.models import gpgdatacontext
from disappeer.models.db import databasefacade
from disappeer.models import tordatacontext
import copy


class RootSetupClass(unittest.TestCase):
    root = tkinter.Tk()
    root_view_obj = rootview.RootView(root)
    root_test_dir = "tests/data/dirmaker/"

    dir_maker = dirmaker.DirMaker(root_test_dir)
    gpg_data_context = gpgdatacontext.GPGDataContext(dir_maker.get_keys_default_dir())
    database_facade = databasefacade.DatabaseFacade(gpg_data_context.get_host_key_observer(),
                                                    dir_maker.get_user_database_dir)
    tor_data_context = tordatacontext.TorDataContext(dir_maker.get_user_tor_keys_dir)
    gpg_data_context = gpgdatacontext.GPGDataContext(dir_maker.get_keys_default_dir())

    def setUp(self):
        self.root_view = MagicMock(spec=self.root_view_obj)
        self.copy_gpg_data_context = copy.deepcopy(self.gpg_data_context)
        self.copy_database_facade = copy.deepcopy(self.database_facade)
        self.copy_tor_data_context = copy.deepcopy(self.tor_data_context)
        self.x = rootcontroller.RootController(self.root, self.root_view, self.copy_gpg_data_context, self.copy_database_facade, self.copy_tor_data_context)

    def altsetup(self):
        x = rootcontroller.RootController(self.root, self.root_view, self.copy_gpg_data_context, self.copy_database_facade, self.copy_tor_data_context)
        return x

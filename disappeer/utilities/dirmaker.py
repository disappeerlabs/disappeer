"""
dirmaker.py

Module for DirMaker class object to check and create app data dirs.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import os


class DirMaker:

    keys_dir_name = 'keys/'
    data_dir_name = 'data/'
    log_dir_name = 'log/'
    default_dir_name = 'default/'
    tor_keys_dir_name = 'tor_keys/'
    databases_dir_name = 'databases/'

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.create_top_level_dirs()
        self.create_default_sub_dirs()

    ############################
    #  ROOT AND TOP LEVEL DIRS #
    ############################

    def get_root_dir(self):
        return self._create_and_return_dir_path(self.root_dir)

    def get_keys_dir(self):
        keys_dir = self.root_dir + self.keys_dir_name
        return self._create_and_return_dir_path(keys_dir)

    def get_data_dir(self):
        data_dir = self.root_dir + self.data_dir_name
        return self._create_and_return_dir_path(data_dir)

    def get_log_dir(self):
        log_dir = self.root_dir + self.log_dir_name
        return self._create_and_return_dir_path(log_dir)

    def create_top_level_dirs(self):
        self.get_root_dir()
        self.get_keys_dir()
        self.get_data_dir()
        self.get_log_dir()

    ######################
    #  SECOND LEVEL DIRS #
    ######################

    def get_keys_default_dir(self):
        target = self.root_dir + self.keys_dir_name + self.default_dir_name
        return self._create_and_return_dir_path(target)

    def create_default_sub_dirs(self):
        self.create_data_sub_dirs(self.default_dir_name)
        result = self.get_keys_default_dir()
        self.set_permissions(result)

    def create_user_sub_dirs(self, name):
        self.create_data_sub_dirs(name)

    def create_data_sub_dirs(self, name):
        target_dir_path = self.root_dir + self.data_dir_name + name
        result = self._create_and_return_dir_path(target_dir_path)
        self.create_tor_keys_sub_dir(result)
        self.create_databases_sub_dir(result)

    def create_tor_keys_sub_dir(self, super_dir_name):
        target_dir_path = super_dir_name + self.tor_keys_dir_name
        return self._create_and_return_dir_path(target_dir_path)

    def create_databases_sub_dir(self, super_dir_name):
        target_dir_path = super_dir_name + self.databases_dir_name
        return self._create_and_return_dir_path(target_dir_path)

    #############
    #  HELPERS  #
    #############

    def get_user_database_dir(self, name):
        target_dir_path = self.root_dir + self.data_dir_name + name
        result = self._create_and_return_dir_path(target_dir_path)
        return self.create_databases_sub_dir(result)

    def get_user_tor_keys_dir(self, name):
        target_dir_path = self.root_dir + self.data_dir_name + name
        result = self._create_and_return_dir_path(target_dir_path)
        return self.create_tor_keys_sub_dir(result)

    def set_permissions(self, path):
        os.chmod(path, 0o700)

    def _create_and_return_dir_path(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        return self._get_abs_path(dir_name)

    def _get_abs_path(self, item):
        return os.path.abspath(item) + '/'



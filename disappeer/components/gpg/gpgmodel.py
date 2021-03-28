"""
gpgmodel.py

Model module for the GPG widget

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import os 
from dptools.tkcomponents.baseapp import basemodel
from dptools.utilities import observable 



class GPGModel(basemodel.BaseModel):

    def __init__(self, args=None, root=None, queue=None):
        self.args = args
        self.root = root
        self.queue = queue
        self.home_dir = self.get_home_dir_from_args()
        self.home_dir_observable = self.config_home_dir_observable()


    def get_home_dir_from_args(self):
        val = self.args.home_dir
        # TODO: what to do if val not set in args? get val from settings
        # TODO: what to do if attribute does not exist in args object? catch error, sys exit
        return val 

    def config_home_dir_observable(self):
        home_dir_observable = observable.Observable()
        self.set_permissions(self.home_dir)
        home_dir_observable.set(self.home_dir)
        return home_dir_observable

    def set_permissions(self, path):
        os.chmod(path, 0o700)

    def add_home_dir_observer(self, observer):
        self.home_dir_observable.add_observer(observer)

    def set_home_dir_observable(self, val):
        self.home_dir_observable.set(val)
    
    def get_home_dir_observable(self): 
        return self.home_dir_observable.get()

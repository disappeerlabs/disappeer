"""
rootcontroller.py

RootController class object

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.baseapp.basepanelview import BasePanelView
from dptools.tkcomponents.baseapp.basecontroller import BaseController


class RootController(BaseController):

    def __init__(self, args=None, root=None):
        BaseController.__init__(self, args=args, root=root)
        self.root = root 
        self.args = args

    def set_root_view(self):
        return BasePanelView(self.root, title="IS THIS ON???")

    def exit(self):
        # TODO: add test to confirm quit called with exit 
        self.root.quit()

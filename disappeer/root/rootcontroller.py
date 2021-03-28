"""
rootcontroller.py

RootController class object

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

from dptools.tkcomponents.baseapp import basecontroller, basepanelview
from dptools.tkcomponents import debugwidget
from disappeer import metainfo


class RootController(basecontroller.BaseController):

    def __init__(self, args=None, root=None):
        basecontroller.BaseController.__init__(self, args=args, root=root)
        self.root = root 
        self.args = args
        self.debug = self.add_widget_left_panel(debugwidget)
        self.debug.click_debug_1_override(self.debug_1_override)
        self.debug.click_debug_2_override(self.debug_2_override)

    def set_root_view(self):
        return basepanelview.BasePanelView(self.root, title=metainfo.title)

    def exit(self):
        # TODO: add test to confirm quit called with exit 
        self.root.quit()

    def debug_1_override(self, event):
        print("CLICK DEBUG 1")

    def debug_2_override(self, event):
        print("CLICK DEBUG 2")
        self.debug.append_to_textbox("HELLO THERE")
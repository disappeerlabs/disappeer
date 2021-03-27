"""
rootcontroller.py

RootController class object

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

class RootController:

    def __init__(self, args, root):
        self.root = root 

    def exit(self):
        # TODO: add test to confirm quit called with exit 
        self.root.quit()

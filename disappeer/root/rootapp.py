"""
rootapp.py

RootApp class object

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import sys 
import tkinter
from dptools.utilities import applogger
from disappeer import metainfo
from disappeer.root import rootcontroller


class RootApp:
    
    def __init__(self, args):
        self.title = metainfo.title
        self.args = args
        self.root = tkinter.Tk()
        self.config_logger()
        self.root_controller = rootcontroller.RootController(self.args, self.root)
        self.config_exit_protocol()

    def config_logger(self):
        # TODO: enable log to file, should be able to toggle his from command line
        # log_file = settings.default_log_dir + 'app.log'
        self.log = applogger.AppLogger(self.title).create()
        sys.excepthook = self.log.handle_uncaught_system_exception
        self.root.report_callback_exception = self.log.handle_uncaught_tkinter_exception

    def config_exit_protocol(self):
        self.root.protocol("WM_DELETE_WINDOW", self.root_controller.exit)

    # TODO: add method to configure logo
    # def config_logo(self):
    #     pass

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log.info("Keyboard interrupt called. Shutting down.")
            sys.exit()

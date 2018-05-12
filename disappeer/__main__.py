"""
disappeer.py

Main app run module for the disappeer app.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
from disappeer.constants import constants
from disappeer.utilities import logger
from disappeer.root import rootcontroller
import sys
from disappeer.utilities import dirmaker
from disappeer.root import rootview
from disappeer import settings
from disappeer.models import gpgdatacontext
from disappeer.models.db import databasefacade
from disappeer.models import tordatacontext


class App:
    def __init__(self):
        self.title = constants.title
        self.root = tkinter.Tk()

        self.dir_maker = dirmaker.DirMaker(settings.root_data_dir)
        self.config_logger()
        self.config_logo()
        self.gpg_datacontext = gpgdatacontext.GPGDataContext(settings.default_key_dir)
        self.database_facade = databasefacade.DatabaseFacade(self.gpg_datacontext.get_host_key_observer(), self.dir_maker.get_user_database_dir)
        self.tor_datacontext = tordatacontext.TorDataContext(self.dir_maker.get_user_tor_keys_dir)
        self.root_view = rootview.RootView(self.root)
        self.controller = rootcontroller.RootController(self.root, self.root_view, self.gpg_datacontext, self.database_facade, self.tor_datacontext)
        self.config_exit_protocol()

    def config_exit_protocol(self):
        self.root.protocol("WM_DELETE_WINDOW", self.controller.exit)

    def config_logger(self):
        log_file = settings.default_log_dir + 'app.log'
        self.log = logger.AppLogger(self.title, file=log_file).create()
        sys.excepthook = self.log.handle_uncaught_system_exception
        self.root.report_callback_exception = self.log.handle_uncaught_tkinter_exception

    def config_logo(self):
        if constants.display_images:
            # This works to add icon to all windows
            from disappeer.utilities import helpers
            image_path = helpers.get_images_dir_path()
            img = tkinter.PhotoImage(file=image_path + 'logo_icon.png')
            self.root.tk.call('wm', 'iconphoto', self.root._w, '-default', img)

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log.info("Keyboard interrupt called. Shutting down.")
            sys.exit()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()

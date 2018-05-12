"""
rightpanel.py

right Panel View for Main Window Paneled View

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import logging
import tkinter
import tkinter.ttk as ttk
from disappeer.console import consoleframe
from disappeer.constants import constants
from disappeer.constants import styling

log = logging.getLogger(constants.title)


class RightPanelView:
    """
    Main right panel view for root window
    """

    def __init__(self, parent):
        self.parent = parent
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_notebook()
        self.parent.add(self.main_frame)

    def config_main_frame(self):
        """
        Main outermost frame for right panel.
        """
        self.main_frame = tkinter.Frame(self.parent, background=styling.background_color)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def config_notebook(self):
        """
        Configure ttk notebook widget and call methods for its tab widgets 
        """
        self.notebook = ttk.Notebook(self.main_frame, padding=(10, 5, 10, 10))

        self.config_console_tab()

        # Enable to configure more notebaook tabs in frame
        # tab1 = tkinter.Frame(self.notebook, background=styling.background_color)
        # self.notebook.add(tab1, text="Monitor")

        self.notebook.grid(row=0, column=0, sticky=styling.sticky_all)

    def config_console_tab(self):
        self.console_frame = consoleframe.ConsoleFrame(self.notebook)
        self.console_frame.grid(sticky=styling.sticky_all)
        self.notebook.add(self.console_frame, text="Console")


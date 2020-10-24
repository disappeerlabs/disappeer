"""
rootview.py
Root view for project

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
from disappeer.constants import constants
from disappeer.constants import styling
from disappeer.root import leftpanel
from disappeer.root import rightpanel
import logging
import functools
from disappeer.popups import popuplauncher

log = logging.getLogger(constants.title)


class RootView:
    """
    Root view for disappeer root controller
    """
    def __init__(self, root):
        # Configure root
        self.root = root
        self.root.minsize(200, 200)
        self.root.title(constants.title)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # Run setup
        self.setup()

        # Set focus
        self.root.focus()

    def setup(self):
        """
        Call all relevant config methods . . .
        """
        styling.config_ttk_styling()
        self.config_main_frame()
        self.config_elements()

    def config_main_frame(self):
        """
        Configure the main outer frame for the main view
        """
        self.main_frame = tkinter.Frame(self.root, background=styling.background_color)
        self.main_frame.grid(column=0, row=0, sticky=styling.sticky_all)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def config_elements(self):
        """
        Call all necessary config methods
        """
        self.config_menubar()
        self.config_main_pane()
        self.config_left_panel()
        self.config_right_panel()

    def config_menubar(self):
        """
        Add all styling for the menubar
        """

        self.root_menubar = tkinter.Menu(self.root, **styling.menu_bar_styling)
        self.root.config(menu=self.root_menubar)

        self.app_menu = tkinter.Menu(self.root_menubar, **styling.menu_bar_styling)
        self.root_menubar.add_cascade(label='App', menu=self.app_menu)

        self.file_menu = tkinter.Menu(self.root_menubar, **styling.menu_bar_styling)
        self.root_menubar.add_cascade(label='File', menu=self.file_menu)

        self.gpg_menu = tkinter.Menu(self.root_menubar, **styling.menu_bar_styling)
        self.root_menubar.add_cascade(label='GPG', menu=self.gpg_menu)

    def config_main_pane(self):
        """
        Configure the paned window for main view
        """
        self.main_pane = tkinter.PanedWindow(self.main_frame, orient="horizontal", sashwidth=10, background='black', borderwidth=0)
        self.main_pane.grid(row=0, column=0, sticky=styling.sticky_all)

    def config_left_panel(self):
        """
        Configure left panel for main pane
        """
        self.left_panel = leftpanel.LeftPanelView(self.main_pane)

    def config_right_panel(self):
        """
        Configure right panel for main pane
        """
        self.right_panel = rightpanel.RightPanelView(self.main_pane)

    def preferences_menu_command(self):
        result = popuplauncher.launch_alert_box_popup(self.root, "This is a popup")


"""
leftpanel.py

Left Panel View for Main Window Paneled View

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import logging
import tkinter
import tkinter.ttk as ttk

from disappeer.constants import constants
from disappeer.constants import styling
from disappeer.gpg import gpgframe
from disappeer.messages import messagesframe
from disappeer.requests import requestsframe
from disappeer.tornet import tornetframe

log = logging.getLogger(constants.title)


class LeftPanelView:
    """
    Main left panel view for root window
    """

    def __init__(self, parent):
        self.parent = parent

        # Init accessible instance attributes
        self.main_frame = None
        self.notebook = None

        self.style = ttk.Style()
        self.setup()

    def setup(self):
        self.config_main_frame()
        self.config_notebook()
        self.parent.add(self.main_frame)

    def config_main_frame(self):
        """
        Main outermost frame for left panel.
        """
        self.main_frame = tkinter.Frame(self.parent, background=styling.background_color)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def config_notebook(self):
        """
        Configure ttk notebook widget and call methods for its tab widgets 
        """
        self.notebook = ttk.Notebook(self.main_frame, padding=(10, 5, 10, 10))

        # Set the GPG tab: TAB 0
        self.config_gpg_tab()

        # Set tornet frame: TAB 1
        self.config_tornet_tab()

        # Set requests tab/frame: TAB 2
        self.config_requests_tab()

        # Set the messages tab: TAB 3
        self.config_messages_tab()

        # Set the debug tab: TAB 4
        # Uncomment line below to enable the debug tab
        # self.config_debug_tab()

        self.notebook.grid(row=0, column=0, sticky=styling.sticky_all)

    def config_tornet_tab(self):
        self.tor_net_frame = tornetframe.TorNetFrame(self.notebook)
        self.tor_net_frame.grid(sticky=styling.sticky_all)
        self.notebook.add(self.tor_net_frame, text='Network')

    def config_requests_tab(self):
        self.requests_frame = requestsframe.RequestsFrame(self.notebook)
        self.requests_frame.notebook_obj = self.notebook
        self.requests_frame.tab_id = 2
        self.requests_frame.grid(sticky=styling.sticky_all)
        self.notebook.add(self.requests_frame, text='Requests')

    def config_gpg_tab(self):
        """
        Configure the gpg frame component object and add to notebook: labelframes and widgets
        """
        self.gpg_frame = gpgframe.GPGFrame(self.notebook)
        self.gpg_frame.grid(sticky=styling.sticky_all)
        self.notebook.add(self.gpg_frame, text="GPG")

    def config_messages_tab(self):
        self.messages_frame = messagesframe.MessagesFrame(self.notebook)
        self.messages_frame.notebook_obj = self.notebook
        self.messages_frame.tab_id = 3
        self.messages_frame.grid(sticky=styling.sticky_all)
        self.notebook.add(self.messages_frame, text="Messages")

    ##################################
    #  Config Debug Notebook Tab     #
    ##################################

    def config_debug_tab(self):
        """
        Configure the debug object and add to notebook: textbox and button
        """
        debug_frame = tkinter.Frame(self.notebook, background=styling.background_color, padx=10, pady=10)

        debug_frame.rowconfigure(0, weight=1)
        debug_frame.columnconfigure(0, weight=1)
        debug_frame.rowconfigure(1, weight=0)
        debug_frame.rowconfigure(2, weight=0)

        self.debug_text_box = tkinter.Text(debug_frame, **styling.debug_text_area)
        self.debug_text_box.grid(row=0, column=0, sticky=styling.sticky_all)

        self.debug_button = ttk.Button(debug_frame, text="Debug")
        self.debug_button.grid(row=1, column=0, sticky=styling.sticky_ew,padx=(5, 0), pady=(10, 5))

        self.debug_button_2 = ttk.Button(debug_frame, text="Debug Two")
        self.debug_button_2.grid(row=2, column=0, sticky=styling.sticky_ew,padx=(5, 0), pady=(10, 5))

        # Add frame to notebook
        self.notebook.add(debug_frame, text="Debug")

    def print_to_debug(self, msg):
        """
        Clear debug text box and insert msg.
        """
        self.debug_text_box.delete('1.0', 'end')
        self.debug_text_box.insert('1.0', msg + "\n")

    def append_to_debug(self, msg):
        """
        Append msg to end of debug text box. Scroll to end of textbox.
        """
        self.debug_text_box.insert('end', msg + "\n")
        self.debug_text_box.see('end')
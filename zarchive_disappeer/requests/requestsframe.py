"""
requestsframe.py

GUI frame for Sent/Received Requests notbook tab view.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling
import logging
from disappeer.constants import constants
from disappeer import images
import os
from disappeer.utilities import helpers


class RequestsFrame(tkinter.Frame):
    """
    A tkinter frame containing necessary widgets for the networking view
    """

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, background=styling.background_color, padx=10, pady=15)
        self.parent = parent
        self.image_path = helpers.get_images_dir_path()
        self.image_obj = tkinter.PhotoImage(file=self.image_path + 'bullet_green_small.gif')
        self.no_image_obj = tkinter.PhotoImage(file=self.image_path + 'no_image.gif')
        self.setup()

    def setup(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)

        self.config_main_pane()
        self.config_sent_peers_frame()
        self.config_received_peers_frame()

    def config_main_pane(self):
        """
        Paned window view to contain all contents of the left panel.
        """
        self.main_pane = tkinter.PanedWindow(self, orient="vertical", sashwidth=10, background=styling.background_color)
        self.main_pane.grid(row=0, column=0, sticky=styling.sticky_all)

        self.main_pane.columnconfigure(0, weight=1)

        # row for sent requests tree view
        self.main_pane.rowconfigure(0, weight=1)

        # row for received requests treeview
        self.main_pane.rowconfigure(1, weight=1)

    def config_sent_peers_frame(self):
        """
        Treeview for Received Contact Requests
        """
        # Row for Peers frame
        sent_requests_frame = tkinter.LabelFrame(self.main_pane, text="Sent Requests", **styling.label_frame_args)
        sent_requests_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 20))
        sent_requests_frame.rowconfigure(0, weight=0)
        sent_requests_frame.rowconfigure(1, weight=1)
        sent_requests_frame.columnconfigure(0, weight=1)

        self.send_request_button = ttk.Button(sent_requests_frame, text="New Contact Request")
        self.send_request_button.grid(row=0, column=0, sticky=styling.sticky_ew, padx=(0, 0), pady=(5, 10))

        self.sent_requests_tree_view = ttk.Treeview(sent_requests_frame, columns='ID')
        self.sent_requests_tree_view.tag_configure('treeview_tag',
                                           background=styling.background_color,
                                           foreground=styling.foreground_color)

        self.sent_requests_tree_view.heading('#0', text="Name", anchor='n')
        self.sent_requests_tree_view.column('#0', width=130)

        self.sent_requests_tree_view.heading('#1', text="ID", anchor='n')
        self.sent_requests_tree_view.column('#1', width=130)
        self.sent_requests_tree_view.grid(row=1, column=0, sticky=styling.sticky_all)
        self.main_pane.add(sent_requests_frame)

    def clear_sent_requests(self):
        for i in self.sent_requests_tree_view.get_children():
            # log.critical("Deleting: {}".format(i))
            self.sent_requests_tree_view.delete(i)

    def append_item_to_sent_requests(self, data):
        result = self.sent_requests_tree_view.insert('',
                                             'end',
                                             text=data[0],
                                             values=data[1],
                                             tags='treeview_tag')

    def append_all_to_sent_requests(self, data_row_list):
        self.clear_sent_requests()
        for item in data_row_list:
            self.append_item_to_sent_requests(item)

    def get_clicked_sent_request_treeview_vals(self):
        try:
            item = self.sent_requests_tree_view.selection()[0]
            val_1 = self.sent_requests_tree_view.item(item, "text")
            val_2 = self.sent_requests_tree_view.item(item, 'values')[0]
            return val_1, val_2
        except IndexError as err:
            return None

    def config_received_peers_frame(self):
        """
        Treeview for Received Contact Requests
        """
        # Row for Peers frame
        received_requests_frame = tkinter.LabelFrame(self.main_pane, text="Received Requests", **styling.label_frame_args)
        received_requests_frame.grid(row=1, column=0, sticky=styling.sticky_all, pady=(0, 20))
        received_requests_frame.rowconfigure(0, weight=1)
        received_requests_frame.columnconfigure(0, weight=1)

        self.received_requests_tree_view = ttk.Treeview(received_requests_frame, columns='ID')
        self.received_requests_tree_view.tag_configure('treeview_tag',
                                                       background=styling.background_color,
                                                       foreground=styling.foreground_color)

        self.unread_image = tkinter.PhotoImage(file=self.image_path + 'bullet_green_small.gif')
        self.received_requests_tree_view.tag_configure('image_tag',
                                                       image=self.unread_image,
                                                       background=styling.background_color,
                                                       foreground=styling.foreground_color)

        self.received_requests_tree_view.heading('#0', text="Name", anchor='n')
        self.received_requests_tree_view.column('#0', width=130)

        self.received_requests_tree_view.heading('#1', text="ID", anchor='n')
        self.received_requests_tree_view.column('#1', width=130)
        self.received_requests_tree_view.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_pane.add(received_requests_frame)

    def clear_recevied_requests(self):
        for i in self.received_requests_tree_view.get_children():
            # log.critical("Deleting: {}".format(i))
            self.received_requests_tree_view.delete(i)

    def append_item_to_received_requests(self, data):
        if data[2] == 'unread':
            tag = 'image_tag'
        else:
            tag = 'treeview_tag'
        result = self.received_requests_tree_view.insert('',
                                             'end',
                                             text=data[0],
                                             values=data[1],
                                             tags=tag)

    def append_all_to_received_requests(self, data_row_list):
        self.clear_recevied_requests()
        for item in data_row_list:
            self.append_item_to_received_requests(item)
        self.toggle_tab_alert_image()

    def get_clicked_received_request_treeview_nonce(self):
        try:
            item = self.received_requests_tree_view.selection()[0]
            col_1 = self.received_requests_tree_view.item(item, "text")
            col_2 = self.received_requests_tree_view.item(item, 'values')[0]
            return col_2
        except IndexError as err:
            return None

    def toggle_tab_alert_image(self):
        tree = self.received_requests_tree_view
        received_children = tree.get_children()
        for iid in received_children:
            result = tree.item(iid, 'tags')
            tag_string = result[0]
            if tag_string == 'image_tag':
                self.notebook_obj.tab(self.tab_id, compound='right', image=self.image_obj)
                self.photo = self.image_obj
                return True
        self.notebook_obj.tab(self.tab_id, compound='right', image=self.no_image_obj)
        self.photo = self.no_image_obj
        return False
"""
messagesframe.py

GUI frame for sent and received messages treeview

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling
from disappeer.constants import constants
from disappeer.utilities import helpers


class MessagesFrame(tkinter.Frame):
    """
    Frame for sent and received messages treeviews notebook tab
    """

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, background=styling.background_color, padx=10, pady=15)
        self.parent = parent
        self.image_path = helpers.get_images_dir_path()
        self.image_obj = tkinter.PhotoImage(file=self.image_path + 'bullet_green_small.gif')
        self.no_image_obj = tkinter.PhotoImage(file=self.image_path + 'no_image.gif')
        self.setup()

    def setup(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.config_main_pane()
        self.config_message_tree()
        self.config_contacts_frame()

    def config_main_pane(self):
        """
        Paned window view to contain all contents of the left panel.
        """
        self.main_pane = tkinter.PanedWindow(self, orient="vertical", sashwidth=10, background=styling.background_color)
        self.main_pane.grid(row=0, column=0, sticky=styling.sticky_all)

        self.main_pane.columnconfigure(0, weight=1)

        # row for message tree view
        self.main_pane.rowconfigure(0, weight=1)

        # row for message viewer
        self.main_pane.rowconfigure(1, weight=1)

    def config_message_tree(self):
        """
        Label frame with treeview box to display messages.
        """
        self.message_tree_frame = tkinter.LabelFrame(self.main_pane, text='Messages', **styling.label_frame_args)
        self.message_tree_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        self.message_tree_frame.columnconfigure(0, weight=1)
        self.message_tree_frame.rowconfigure(0, weight=1)

        self.message_tree_view = ttk.Treeview(self.message_tree_frame, show='tree')
        self.message_tree_view.tag_configure('treeview_tag',
                                             background=styling.background_color,
                                             foreground=styling.foreground_color)

        # self.unread_image = tkinter.PhotoImage(file='images/bullet_green_small.gif')
        self.message_tree_view.tag_configure('image_tag',
                                             image=self.image_obj,
                                             background=styling.background_color,
                                             foreground=styling.foreground_color
                                             )

        self.message_tree_view.heading('#0', text="Name", anchor='n')

        self.message_tree_view.insert('', 'end', 'recv_id', text="Received", tags='treeview_tag')
        self.message_tree_view.insert('', 'end', 'sent_id', text="Sent", tags='treeview_tag')
        self.message_tree_view.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_pane.add(self.message_tree_frame)

    def toggle_tab_alert_image(self):
        msg_tree = self.message_tree_view
        received_children = msg_tree.get_children("recv_id")
        for iid in received_children:
            result = msg_tree.item(iid, 'tags')
            tag_string = result[0]
            if tag_string == 'image_tag':
                self.notebook_obj.tab(self.tab_id, compound='right', image=self.image_obj)
                self.photo = self.image_obj
                return True

        contact_tree = self.contacts_tree_view
        contact_children = contact_tree.get_children()
        for iid in contact_children:
            result = contact_tree.item(iid, 'tags')
            tag_string = result[0]
            if tag_string == 'image_tag':
                self.notebook_obj.tab(self.tab_id, compound='right', image=self.image_obj)
                self.photo = self.image_obj
                return True

        self.notebook_obj.tab(self.tab_id, compound='right', image=self.no_image_obj)
        self.photo = self.no_image_obj
        return False

    def update_message_tree_view_received(self, data_list):
        tree = self.message_tree_view
        tree.delete(*tree.get_children("recv_id"))
        for item in data_list:
            if item[1] == 'unread':
                tag = 'image_tag'
            else:
                tag = 'treeview_tag'
            tree.insert('recv_id', 'end', text=item[0], tags=tag)
        self.toggle_tab_alert_image()

    def update_message_tree_view_received_item_as_read(self, item):
        self.message_tree_view.item(item, tags='treeview_tag')
        self.toggle_tab_alert_image()

    def update_message_tree_view_sent(self, data_list):
        # Clear items from received and sent folders
        tree = self.message_tree_view
        tree.delete(*tree.get_children("sent_id"))
        for item in data_list:
            tree.insert('sent_id', 'end', text=item[0])

    def delete_message_treeview_item_by_iid(self, iid_num):
        self.message_tree_view.delete(iid_num)
        self.toggle_tab_alert_image()

    def get_clicked_treeview_item_parent_and_nonce(self):
        try:
            item_id = self.message_tree_view.selection()[0]
        except IndexError:
            return None

        top_level = ['recv_id', 'sent_id']
        if item_id in top_level:
            return None
        parent_iid = self.message_tree_view.parent(item_id)
        parent_text = self.message_tree_view.item(parent_iid)['text']
        current_text = self.message_tree_view.item(item_id)['text']
        return parent_text, current_text

    def get_clicked_treeview_item_parent_nonce_and_iid(self):
        try:
            item_id = self.message_tree_view.selection()[0]
        except IndexError:
            return None

        top_level = ['recv_id', 'sent_id']
        if item_id in top_level:
            return None
        parent_iid = self.message_tree_view.parent(item_id)
        parent_text = self.message_tree_view.item(parent_iid)['text']
        current_text = self.message_tree_view.item(item_id)['text']
        return parent_text, current_text, item_id

    def config_contacts_frame(self):
        """
        Treeview for confirmed, existing contacts.
        """
        # Row for Contacts frame
        contacts_frame = tkinter.LabelFrame(self.main_pane, text="Contacts", **styling.label_frame_args)
        contacts_frame.grid(row=1, column=0, sticky=styling.sticky_all, pady=(0, 20))
        contacts_frame.rowconfigure(0, weight=1)
        contacts_frame.columnconfigure(0, weight=1)

        self.contacts_tree_view = ttk.Treeview(contacts_frame, columns='ID')
        self.contacts_tree_view.tag_configure('treeview_tag',
                                              background=styling.background_color,
                                              foreground=styling.foreground_color)

        # self.unread_image = tkinter.PhotoImage(file='images/bullet_green_small.gif')
        self.contacts_tree_view.tag_configure('image_tag',
                                              image=self.image_obj,
                                              background=styling.background_color,
                                              foreground=styling.foreground_color)

        self.contacts_tree_view.heading('#0', text="Name", anchor='n')
        self.contacts_tree_view.column('#0', width=130)

        self.contacts_tree_view.heading('#1', text="ID", anchor='n')
        self.contacts_tree_view.column('#1', width=130)
        self.contacts_tree_view.grid(row=0, column=0, sticky=styling.sticky_all)
        self.main_pane.add(contacts_frame)

    def clear_contacts_treeview(self):
        for i in self.contacts_tree_view.get_children():
            # log.critical("Deleting: {}".format(i))
            self.contacts_tree_view.delete(i)

    def append_item_to_contacts_treeview(self, data):
        if data[2] == 'unread':
            tag = 'image_tag'
        else:
            tag = 'treeview_tag'

        result = self.contacts_tree_view.insert('',
                                                'end',
                                                text=data[0],
                                                values=data[1],
                                                tags=tag)

    def append_all_to_peer_contacts(self, data_row_list):
        self.clear_contacts_treeview()
        for item in data_row_list:
            self.append_item_to_contacts_treeview(item)
        self.toggle_tab_alert_image()

    def get_clicked_contacts_treeview_contact_id(self):
        try:
            item = self.contacts_tree_view.selection()[0]
            col_1 = self.contacts_tree_view.item(item, "text")
            col_2 = self.contacts_tree_view.item(item, 'values')[0]
            return col_2
        except IndexError as err:
            return None




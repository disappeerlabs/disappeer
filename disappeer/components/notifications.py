"""
notifications.py

A notifications box component, subclass of tkinter LabelFrame.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
from disappeer.constants import styling


class NotificationsBox(tkinter.LabelFrame):
    """
    A tkinter labelframe containing a textbox with styled print and append methods.
    """

    def __init__(self, parent, title="Notifications"):
        tkinter.LabelFrame.__init__(self, parent, text=title, **styling.label_frame_args)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.config_textbox()

    def config_textbox(self):
        self.text_box = tkinter.Text(self, **styling.debug_text_area)
        self.text_box.grid(row=0, column=0, sticky=styling.sticky_all)

    def print_msg(self, msg, level='Debug'):
        """
        Clear debug text box and insert msg.
        """
        self.config_level(level)
        self.text_box.delete('1.0', 'end')
        self.text_box.insert('1.0', msg + "\n")

    def append_msg(self, msg, level='Debug'):
        """
        Append msg to end of debug text box. Scroll to end of textbox.
        """
        self.config_level(level)
        self.text_box.insert('end', msg + "\n")
        self.text_box.see('end')

    def get_text_area(self):
        """
        :return: all current contents of text area 
        """
        result = self.text_box.get('1.0', 'end')
        return result

    def config_level(self, level):
        """
        configure the text box to print a different color
        :param level: level determines color
        """
        if level == 'Debug':
            self.text_box.configure(foreground='green')
        elif level == 'Info':
            self.text_box.configure(foreground='blue')
        else:
            self.text_box.configure(foreground='red')
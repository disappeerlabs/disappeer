"""
gpgframe.py

View module for GPG Widget

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from dptools.static import styling
from dptools.tkcomponents.notificationswidget import notificationsboxframe


class GPGFrame(tkinter.Frame):

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, background=styling.background_color, padx=10, pady=15)
        self.parent = parent
        self.home_dir_entry = None
        self.home_dir_entry_var = None
        self.setup()

    def setup(self):
        self.columnconfigure(0, weight=1)
        self.config_home_dir_frame()
        self.config_key_info_frame()
        self.config_manage_keys_frame()
        self.config_notifications_box_frame()

    def bind_home_dir_entry(self, command, function):
        self.home_dir_entry.bind(command, function)

    def config_home_dir_frame(self):
        # Row for Home Key Dir LabelFrame
        self.rowconfigure(0, weight=0)

        home_dir_frame = tkinter.LabelFrame(self, text="Home Directory", **styling.label_frame_args)
        home_dir_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 20))
        home_dir_frame.rowconfigure(0, weight=0)
        home_dir_frame.rowconfigure(1, weight=0)
        home_dir_frame.rowconfigure(2, weight=0)

        home_dir_frame.columnconfigure(0, weight=0)
        home_dir_frame.columnconfigure(1, weight=1)

        # Home dir label
        home_dir_label = tkinter.Label(home_dir_frame, text='Home:', **styling.label_args)
        home_dir_label.grid(row=0, column=0, sticky='E', padx=(0, 5))

        # Home dir entry
        self.home_dir_entry_var = tkinter.StringVar()
        self.home_dir_entry_var.set("Default Text Input")
        self.home_dir_entry = tkinter.Entry(home_dir_frame,
                                            textvariable=self.home_dir_entry_var,
                                            state='readonly',
                                            **styling.entry_field_readonly_args)
        self.home_dir_entry.grid(row=0, column=1, sticky=styling.sticky_ew, ipady=1)


        # Host key label
        host_key_label = tkinter.Label(home_dir_frame, text='Host Key:', **styling.label_args)
        host_key_label.grid(row=1, column=0, sticky='W', padx=(0, 5), pady=(0, 0))

        # Host key entry
        self.host_key_entry_var = tkinter.StringVar()
        self.host_key_entry_var.set("Key Name Here")

        self.host_key_entry = tkinter.Entry(home_dir_frame,
                                            textvariable=self.host_key_entry_var,
                                            state='readonly',
                                            **styling.entry_field_special_readonly_args)

        self.host_key_entry.grid(row=1, column=1, sticky=styling.sticky_ew, ipady=1, pady=(0, 0))

        # Set passphrase button
        self.set_passphrase_button = ttk.Button(home_dir_frame, text="Set Session Passphrase")
        self.set_passphrase_button.grid(row=2, column=0, columnspan=2, sticky=styling.sticky_ew, padx=(0, 0), pady=(15, 5))

    def config_key_info_frame(self):
        # Row for Key Info Frame
        self.rowconfigure(1, weight=0)

        # Make cols uniform size so widget does not expand when option selection changes
        key_info_frame = tkinter.LabelFrame(self, text='Key Info', **styling.label_frame_args)
        key_info_frame.grid(row=1, column=0, sticky=styling.sticky_ew, pady=(0, 20))
        key_info_frame.rowconfigure(0, weight=0)
        key_info_frame.columnconfigure(0, weight=1, uniform='size')
        key_info_frame.columnconfigure(1, weight=1, uniform='size')

        # Config Key Dropdown Menu Widget
        self.key_info_option_var = tkinter.StringVar()
        self.key_info_option_var.set("Select Key")

        temp_list = ["One", "Two", "Three"]
        self.key_info_dropdown = ttk.OptionMenu(key_info_frame,
                                                self.key_info_option_var,
                                                self.key_info_option_var.get(),
                                                *temp_list)

        # Styling for the dropdown itself
        self.key_info_dropdown = styling.config_local_dropdown(self.key_info_dropdown)
        self.key_info_dropdown.grid(row=0, column=0, sticky=styling.sticky_ew, padx=(0, 5), pady=(0, 5))

        # Key info button, should grab the val from the dropdown when clicked
        self.key_info_button = ttk.Button(key_info_frame, text="Key Info")
        self.key_info_button.grid(row=0, column=1, sticky=styling.sticky_ew, padx=(5, 0), pady=(0, 5))

        # INSTANTIATE KEY INFO DROPDOWN HANDLER CLASS
        self.key_info_dropdown_handler = KeyInfoDropdownHandler(self.key_info_option_var, self.key_info_dropdown)

    def config_manage_keys_frame(self):
        # Row for Manage Keys Frame
        self.rowconfigure(2, weight=0)

        manage_keys_frame = tkinter.LabelFrame(self, text='Manage Keys', **styling.label_frame_args)
        manage_keys_frame.grid(row=2, column=0, sticky=styling.sticky_ew, pady=(0, 20))
        manage_keys_frame.rowconfigure(0, weight=0)
        manage_keys_frame.columnconfigure(0, weight=1)
        manage_keys_frame.columnconfigure(1, weight=1)

        # Create new key button
        self.new_key_button = ttk.Button(manage_keys_frame, text='New Key')
        self.new_key_button.grid(row=0, column=0, sticky=styling.sticky_ew, padx=(0, 5))

        # Delete key button
        self.delete_key_button = ttk.Button(manage_keys_frame, text='Delete Key')
        self.delete_key_button.grid(row=0, column=1, sticky=styling.sticky_ew, padx=(5, 0))

    def config_notifications_box_frame(self):
        # Row for Notifications Box
        self.rowconfigure(3, weight=1)
        self.notifications_box = notificationsboxframe.NotificationsBox(self)
        self.notifications_box.grid(row=3, column=0, sticky=styling.sticky_all, pady=(0, 10))

    def config_image_frame(self):
        # Row for Image Icon
        self.rowconfigure(4, weight=0)

        # image_path = "images/small_gnupg_full_logo.png"
        # image = tkinter.PhotoImage(file=image_path)
        # label = tkinter.Label(self, image=image, background=styling.background_color)
        # label.photo = image
        # label.grid(row=4, column=0, sticky=styling.sticky_all, pady=(0, 10))


class KeyInfoDropdownHandler:

    def __init__(self, key_info_option_var, key_info_dropdown):
        self.key_info_option_var = key_info_option_var
        self.key_info_dropdown = key_info_dropdown

    def set(self, new_list):
        if len(new_list) == 0:
            new_list = ["No Keys in Home Dir"]
        self.key_info_option_var.set("Public Keys")
        self.key_info_dropdown['menu'].delete(0, 'end')
        for item in new_list:
            self.key_info_dropdown['menu'].add_command(label=item, command=lambda value=item: self.key_info_option_var.set(value))




"""
tornetframe.py

Notebook Tab frame for controlling tor proxy services and network services

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter
import tkinter.ttk as ttk
from disappeer.components import notifications
from disappeer.constants import styling
import logging
from disappeer.constants import constants
from disappeer.utilities import helpers

log = logging.getLogger(constants.title)


class TorNetFrame(tkinter.Frame):
    """
    A tkinter frame containing necessary widgets for the tor proxy and server controls view
    """

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, background=styling.background_color, padx=10, pady=15)
        self.parent = parent
        self.image_path = helpers.get_images_dir_path()
        self.setup()

    def setup(self):
        self.columnconfigure(0, weight=1)
        self.config_net_services_frame()

        # TODO: these frames need to be refactored, way too much code duplication
        if constants.display_images:
            self.config_tor_proxy_frame_with_images()
        else:
            self.config_tor_proxy_frame()
        self.config_notifications_box()

    def config_net_services_frame(self):
        self.rowconfigure(0, weight=0)

        label_frame = tkinter.LabelFrame(self, text="Network Services", **styling.label_frame_args)
        label_frame.grid(row=0, column=0, sticky=styling.sticky_all, pady=(0, 10))
        label_frame.rowconfigure(0, weight=0)
        label_frame.columnconfigure(0, weight=1)

        # SERVER CONTROL FRAME
        server_frame = tkinter.Frame(label_frame,background=styling.background_color)
        server_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        server_frame.rowconfigure(0, weight=0)
        server_frame.columnconfigure(0, weight=0)
        server_frame.columnconfigure(1, weight=0)
        server_frame.columnconfigure(2, weight=0)
        server_frame.columnconfigure(3, weight=0)

        # Contact Server label
        contact_server_label = tkinter.Label(server_frame, text='Servers:', **styling.label_args)
        contact_server_label.grid(row=0, column=0, sticky='W', padx=(15, 0))

        # Contact Server Radio Buttons
        self.net_server_radio_var = tkinter.IntVar()
        self.net_server_radio_var.set(0)
        self.net_server_on_button = tkinter.Radiobutton(server_frame, text='Start', variable=self.net_server_radio_var, value=1, **styling.radio_button_args)
        self.net_server_on_button.grid(row=0, column=1, sticky='W', padx=(5,0))

        self.net_server_off_button = tkinter.Radiobutton(server_frame, text='Stop', variable=self.net_server_radio_var, value=0, **styling.radio_button_args)
        self.net_server_off_button.grid(row=0, column=2, sticky='W', padx=(5,0))

        # Key Server Status Var
        self.net_server_status_var = tkinter.StringVar()
        self.net_server_status_var.set("Waiting...")
        contact_server_status_label = tkinter.Label(server_frame, textvariable=self.net_server_status_var, **styling.label_args)
        contact_server_status_label.grid(row=0, column=3, sticky='W', padx=(10, 0))

    def set_net_server_status_var(self, status_msg):
        self.net_server_status_var.set(status_msg)

    def get_net_server_radio_var(self):
        result = self.net_server_radio_var.get()
        return result

    def config_tor_proxy_frame(self):
        self.rowconfigure(1, weight=0)

        label_frame = tkinter.LabelFrame(self, text="Tor Proxy", **styling.label_frame_args)
        label_frame.grid(row=1, column=0, sticky=styling.sticky_all, pady=(0, 10))
        label_frame.rowconfigure(0, weight=0, pad=10)
        label_frame.rowconfigure(1, weight=0, pad=10)
        label_frame.rowconfigure(2, weight=0, pad=10)
        label_frame.columnconfigure(0, weight=1)

        # Proxy Type Radio Control Frame
        type_frame = tkinter.Frame(label_frame, background=styling.background_color)
        type_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        type_frame.rowconfigure(0, weight=0)
        type_frame.rowconfigure(1, weight=0)
        type_frame.columnconfigure(0, weight=0)

        # Proxy Type label
        type_label = tkinter.Label(type_frame, text='Persistent:', **styling.label_args)
        type_label.grid(row=0, column=0, sticky='E', padx=(1, 0))
        self.tor_proxy_persistent_var = tkinter.IntVar()
        self.proxy_type_check_button = tkinter.Checkbutton(type_frame, variable=self.tor_proxy_persistent_var, **styling.check_button_styling)
        self.proxy_type_check_button.grid(row=0, column=1, sticky='W', padx=(3, 0))

        # Start/Stop CONTROL FRAME
        service_frame = tkinter.Frame(label_frame, background=styling.background_color)
        service_frame.grid(row=1, column=0, sticky=styling.sticky_all, padx=(3, 0))
        service_frame.rowconfigure(0, weight=0)
        service_frame.columnconfigure(0, weight=0)

        # Start/Stop label
        tor_proxy_label = tkinter.Label(service_frame, text='Tor Proxy:', **styling.label_args)
        tor_proxy_label.grid(row=0, column=0, sticky='E', padx=(0, 0))

        # Start/Stop Radio Buttons
        self.tor_proxy_radio_var = tkinter.IntVar()
        self.tor_proxy_radio_var.set(0)
        self.tor_proxy_on_button = tkinter.Radiobutton(service_frame, text='Start', variable=self.tor_proxy_radio_var, value=1, **styling.radio_button_args)
        self.tor_proxy_on_button.grid(row=0, column=1, sticky='W', padx=(1, 0))

        self.tor_proxy_off_button = tkinter.Radiobutton(service_frame, text='Stop', variable=self.tor_proxy_radio_var, value=0, **styling.radio_button_args)
        self.tor_proxy_off_button.grid(row=0, column=2, sticky='W', padx=(5,0))

        # Start/Stop Status Var
        self.tor_proxy_status_var = tkinter.StringVar()
        self.tor_proxy_status_var.set("Waiting...")
        tor_proxy_status_label = tkinter.Label(service_frame, textvariable=self.tor_proxy_status_var, **styling.label_args)
        tor_proxy_status_label.grid(row=0, column=3, sticky='W', padx=(10, 0))

        # Onion Address Frame
        onion_frame = tkinter.Frame(label_frame, background=styling.background_color)
        onion_frame.grid(row=2, column=0, sticky=styling.sticky_all)
        onion_frame.rowconfigure(0, weight=0, pad=10)
        onion_frame.rowconfigure(1, weight=0, pad=10)
        onion_frame.rowconfigure(2, weight=0, pad=10)
        onion_frame.columnconfigure(0, weight=0)
        onion_frame.columnconfigure(1, weight=1)

        # Request address label
        request_onion_label = tkinter.Label(onion_frame, text='Request:', **styling.label_args)
        request_onion_label.grid(row=0, column=0, sticky='E', padx=(0, 0))


        self.request_onion_entry_var = tkinter.StringVar()
        self.request_onion_entry_var.set("Not Set")
        request_onion_entry = tkinter.Entry(onion_frame,
                                            textvariable=self.request_onion_entry_var,
                                            state='readonly',
                                            **styling.entry_field_label_clone_copy_paste_args)
        request_onion_entry.grid(row=0, column=1, sticky=styling.sticky_ew, padx=(12, 0))


        # Response address label
        response_onion_label = tkinter.Label(onion_frame, text='Response:', **styling.label_args)
        response_onion_label.grid(row=1, column=0, sticky='E')

        self.response_onion_entry_var = tkinter.StringVar()
        self.response_onion_entry_var.set("Not Set")
        response_onion_entry = tkinter.Entry(onion_frame,
                                            textvariable=self.response_onion_entry_var,
                                            state='readonly',
                                            **styling.entry_field_label_clone_copy_paste_args)
        response_onion_entry.grid(row=1, column=1, sticky=styling.sticky_ew, padx=(12, 0))


        # Message address label
        message_onion_label = tkinter.Label(onion_frame, text='Message:', **styling.label_args)
        message_onion_label.grid(row=2, column=0, sticky='E')

        self.message_onion_entry_var = tkinter.StringVar()
        self.message_onion_entry_var.set("Not Set")
        message_onion_entry = tkinter.Entry(onion_frame,
                                            textvariable=self.message_onion_entry_var,
                                            state='readonly',
                                            **styling.entry_field_label_clone_copy_paste_args)
        message_onion_entry.grid(row=2, column=1, sticky=styling.sticky_ew, padx=(12, 0))

    def config_tor_proxy_frame_with_images(self):
        self.rowconfigure(1, weight=0)

        label_frame = tkinter.LabelFrame(self, text="Tor Proxy", **styling.label_frame_args)
        label_frame.grid(row=1, column=0, sticky=styling.sticky_all, pady=(0, 10))
        label_frame.rowconfigure(0, weight=0, pad=10)
        label_frame.rowconfigure(1, weight=0, pad=10)
        label_frame.rowconfigure(2, weight=0, pad=10)
        label_frame.columnconfigure(0, weight=1)

        # Proxy Type Radio Control Frame
        type_frame = tkinter.Frame(label_frame, background=styling.background_color)
        type_frame.grid(row=0, column=0, sticky=styling.sticky_all)
        type_frame.rowconfigure(0, weight=0)
        type_frame.rowconfigure(1, weight=0)
        type_frame.columnconfigure(0, weight=0)

        # Proxy Type label
        type_label = tkinter.Label(type_frame, text='Persistent:', **styling.label_args)
        type_label.grid(row=0, column=0, sticky='E', padx=(1, 0))
        self.tor_proxy_persistent_var = tkinter.IntVar()
        self.proxy_type_check_button = tkinter.Checkbutton(type_frame, variable=self.tor_proxy_persistent_var, **styling.check_button_styling)
        self.proxy_type_check_button.grid(row=0, column=1, sticky='W', padx=(3, 0))

        # Start/Stop CONTROL FRAME
        service_frame = tkinter.Frame(label_frame, background=styling.background_color)
        service_frame.grid(row=1, column=0, sticky=styling.sticky_all, padx=(3, 0))
        service_frame.rowconfigure(0, weight=0)
        service_frame.columnconfigure(0, weight=0)

        # Start/Stop label
        tor_proxy_label = tkinter.Label(service_frame, text='Tor Proxy:', **styling.label_args)
        tor_proxy_label.grid(row=0, column=0, sticky='E', padx=(0, 0))

        # Start/Stop Radio Buttons
        self.tor_proxy_radio_var = tkinter.IntVar()
        self.tor_proxy_radio_var.set(0)
        self.tor_proxy_on_button = tkinter.Radiobutton(service_frame, text='Start', variable=self.tor_proxy_radio_var, value=1, **styling.radio_button_args)
        self.tor_proxy_on_button.grid(row=0, column=1, sticky='W', padx=(1, 0))

        self.tor_proxy_off_button = tkinter.Radiobutton(service_frame, text='Stop', variable=self.tor_proxy_radio_var, value=0, **styling.radio_button_args)
        self.tor_proxy_off_button.grid(row=0, column=2, sticky='W', padx=(5,0))

        # Start/Stop Status Var
        self.tor_proxy_status_var = tkinter.StringVar()
        self.tor_proxy_status_var.set("Waiting...")
        tor_proxy_status_label = tkinter.Label(service_frame, textvariable=self.tor_proxy_status_var, **styling.label_args)
        tor_proxy_status_label.grid(row=0, column=3, sticky='W', padx=(10, 0))

        # Onion Address Frame
        onion_frame = tkinter.Frame(label_frame, background=styling.background_color)
        onion_frame.grid(row=2, column=0, sticky=styling.sticky_all)
        onion_frame.rowconfigure(0, weight=0, pad=10)
        onion_frame.rowconfigure(1, weight=0, pad=10)
        onion_frame.rowconfigure(2, weight=0, pad=10)
        onion_frame.columnconfigure(0, weight=0)
        onion_frame.columnconfigure(1, weight=0)
        onion_frame.columnconfigure(2, weight=1)

        # Request address label
        request_onion_label = tkinter.Label(onion_frame, text='Request:', **styling.label_args)
        request_onion_label.grid(row=0, column=0, sticky='E', padx=(0, 0))

        onion_icon_image = tkinter.PhotoImage(file=self.image_path + 'tor_icon_small.gif')
        request_icon = tkinter.Label(onion_frame, image=onion_icon_image, **styling.icon_button_args)
        request_icon.photo = onion_icon_image
        request_icon.grid(row=0, column=1, padx=(12, 0))

        self.request_onion_entry_var = tkinter.StringVar()
        self.request_onion_entry_var.set("Not Set")
        request_onion_entry = tkinter.Entry(onion_frame,
                                            textvariable=self.request_onion_entry_var,
                                            state='readonly',
                                            **styling.entry_field_label_clone_copy_paste_args)
        request_onion_entry.grid(row=0, column=2, sticky=styling.sticky_ew, padx=(8, 0))


        # Response address label
        response_onion_label = tkinter.Label(onion_frame, text='Response:', **styling.label_args)
        response_onion_label.grid(row=1, column=0, sticky='E')

        onion_icon_image = tkinter.PhotoImage(file=self.image_path + 'tor_icon_small.gif')
        response_icon = tkinter.Label(onion_frame, image=onion_icon_image, **styling.icon_button_args)
        response_icon.photo = onion_icon_image
        response_icon.grid(row=1, column=1, padx=(12, 0))

        self.response_onion_entry_var = tkinter.StringVar()
        self.response_onion_entry_var.set("Not Set")
        response_onion_entry = tkinter.Entry(onion_frame,
                                            textvariable=self.response_onion_entry_var,
                                            state='readonly',
                                            **styling.entry_field_label_clone_copy_paste_args)
        response_onion_entry.grid(row=1, column=2, sticky=styling.sticky_ew, padx=(8, 0))


        # Message address label
        message_onion_label = tkinter.Label(onion_frame, text='Message:', **styling.label_args)
        message_onion_label.grid(row=2, column=0, sticky='E')

        onion_icon_image = tkinter.PhotoImage(file=self.image_path + 'tor_icon_small.gif')
        message_icon = tkinter.Label(onion_frame, image=onion_icon_image, **styling.icon_button_args)
        message_icon.photo = onion_icon_image
        message_icon.grid(row=2, column=1, padx=(12, 0))

        self.message_onion_entry_var = tkinter.StringVar()
        self.message_onion_entry_var.set("Not Set")
        message_onion_entry = tkinter.Entry(onion_frame,
                                            textvariable=self.message_onion_entry_var,
                                            state='readonly',
                                            **styling.entry_field_label_clone_copy_paste_args)
        message_onion_entry.grid(row=2, column=2, sticky=styling.sticky_ew, padx=(8, 0))

    def get_tor_proxy_persistent_checkbutton_var(self):
        result = self.tor_proxy_persistent_var.get()
        return result

    def disable_tor_proxy_persistent_checkbutton(self):
        self.proxy_type_check_button.configure(state=tkinter.DISABLED)

    def enable_tor_proxy_persistent_checkbutton(self):
        self.proxy_type_check_button.configure(state=tkinter.NORMAL)

    def get_tor_proxy_radio_var(self):
        result = self.tor_proxy_radio_var.get()
        return result

    def set_tor_proxy_status_var(self, status_msg):
        self.tor_proxy_status_var.set(status_msg)

    def set_tor_onion_request_addr(self, address_string):
        self.request_onion_entry_var.set(address_string)

    def set_tor_onion_response_addr(self, address_string):
        self.response_onion_entry_var.set(address_string)

    def set_tor_onion_message_addr(self, address_string):
        self.message_onion_entry_var.set(address_string)

    def config_notifications_box(self):
        # Row for Notifications Box
        self.rowconfigure(2, weight=1)
        self.notifications_box = notifications.NotificationsBox(self)
        self.notifications_box.grid(row=2, column=0, sticky=styling.sticky_all, pady=(0, 0))

    def disable_tor_proxy_on_button(self):
        self.tor_proxy_on_button.configure(state=tkinter.DISABLED)

    def enable_tor_proxy_on_button(self):
        self.tor_proxy_on_button.configure(state=tkinter.NORMAL)

    def disable_tor_proxy_off_button(self):
        self.tor_proxy_off_button.configure(state=tkinter.DISABLED)

    def enable_tor_proxy_off_button(self):
        self.tor_proxy_off_button.configure(state=tkinter.NORMAL)

    def disable_net_server_on_button(self):
        self.net_server_on_button.configure(state=tkinter.DISABLED)

    def enable_net_server_on_button(self):
        self.net_server_on_button.configure(state=tkinter.NORMAL)

    def disable_net_server_off_button(self):
        self.net_server_off_button.configure(state=tkinter.DISABLED)

    def enable_net_server_off_button(self):
        self.net_server_off_button.configure(state=tkinter.NORMAL)

    def handle_tor_proxy_on_clicked_actions(self):
        self.disable_tor_proxy_on_button()
        self.enable_tor_proxy_off_button()
        self.tor_proxy_radio_var.set(1)

    def handle_tor_proxy_off_clicked_actions(self):
        self.disable_tor_proxy_off_button()
        self.enable_tor_proxy_on_button()
        self.tor_proxy_radio_var.set(0)

    def handle_net_server_on_clicked_actions(self):
        self.disable_net_server_on_button()
        self.enable_net_server_off_button()

    def handle_net_server_off_clicked_actions(self):
        self.disable_net_server_off_button()
        self.enable_net_server_on_button()




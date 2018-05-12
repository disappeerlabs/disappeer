"""
consoleframe.py

Frame object component containing widgets for root window right panel console tab frame

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


import tkinter
import tkinter.ttk as ttk
from disappeer.constants import styling
from disappeer.constants import constants
from disappeer.utilities import helpers


class ConsoleFrame(tkinter.Frame):
    """
    A tkinter frame containing necessary widgets for the networking view
    """

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, background=styling.background_color, padx=10, pady=15)
        self.parent = parent
        self.image_path = helpers.get_images_dir_path()
        self.setup()

    def setup(self):
        self.columnconfigure(0, weight=1)

        # Row for top button frame
        self.rowconfigure(0, weight=0)

        # Row for console text area
        self.rowconfigure(1, weight=1)

        # Row for bottom button batch
        self.rowconfigure(2, weight=0)

        self.config_toolbar()
        self.key_info_dropdown_handler = KeyInfoDropdownHandler(self.console_key_option_var, self.console_key_dropdown)
        self.console_function_dropdown_handler = ConsoleFunctionDropdownHandler(self.console_function_option_var, self.console_function_dropdown)
        self.config_text_box()

    def config_toolbar(self):
        if constants.display_images:
            self.config_images_toolbar()
        else:
            self.config_text_toolbar()

    def config_text_toolbar(self):

        # TOP BUTTON FRAME
        top_button_frame = tkinter.Frame(self, background=styling.background_color)
        top_button_frame.grid(row=0, column=0, sticky=styling.sticky_new, pady=(0, 10))
        top_button_frame.rowconfigure(0, weight=0)

        # Icon Button Frame: config manually to play with weights
        top_button_frame.columnconfigure(0, weight=1)
        top_button_frame.columnconfigure(1, weight=1)
        top_button_frame.columnconfigure(2, weight=1)
        top_button_frame.columnconfigure(3, weight=0)
        top_button_frame.columnconfigure(4, weight=1)
        top_button_frame.columnconfigure(5, weight=1)
        top_button_frame.columnconfigure(6, weight=1)
        top_button_frame.columnconfigure(7, weight=1)
        top_button_frame.columnconfigure(8, weight=1)

        # File handling buttons
        self.save_button = ttk.Button(top_button_frame, text='Save')
        self.save_button.grid(row=0, column=0, sticky=styling.sticky_all)

        self.open_button = ttk.Button(top_button_frame, text='Open')
        self.open_button.grid(row=0, column=1, sticky=styling.sticky_all)

        self.clear_button = ttk.Button(top_button_frame, text='Clear')
        self.clear_button.grid(row=0, column=2, sticky=styling.sticky_all)

        # Separator
        separator = ttk.Separator(top_button_frame, orient='vertical')
        separator.grid(row=0, column=3, sticky=styling.sticky_all, padx=(10, 10))

        # Key dropdown var and menu
        self.console_key_option_var = tkinter.StringVar()
        self.console_key_option_var.set("Key")

        temp_list_1 = ["One", "Two", "Three"]
        self.console_key_dropdown = ttk.OptionMenu(top_button_frame,
                                                   self.console_key_option_var,
                                                   "Key",
                                                   *temp_list_1)
        # Give it a constant width so it does not resize when option selection changes
        self.console_key_dropdown.configure(width='15')
        self.console_key_dropdown = styling.config_local_dropdown(self.console_key_dropdown)
        self.console_key_dropdown.grid(row=0, column=4, sticky=styling.sticky_all, padx=(5, 10))

        # FUnction dropdown var and menu
        self.console_function_option_var = tkinter.StringVar()
        self.console_function_option_var.set("Function")

        temp_list_2 = ["TMP_Encrypt", "TMP_Decrypt", "TMP_Import", 'TMP_Export', 'TMP_Sign', 'TMP_Verify']
        self.console_function_dropdown = ttk.OptionMenu(top_button_frame,
                                                        self.console_function_option_var,
                                                        "Function",
                                                        *temp_list_2)
        self.console_function_dropdown = styling.config_local_dropdown(self.console_function_dropdown)
        self.console_function_dropdown.grid(row=0, column=5, sticky=styling.sticky_all, padx=(0, 10))

        self.run_button = ttk.Button(top_button_frame, text='Run')
        self.run_button.grid(row=0, column=6, sticky=styling.sticky_all, padx=(0, 10))

    def config_images_toolbar(self):

        # TOP BUTTON FRAME
        top_button_frame = tkinter.Frame(self, background=styling.background_color)
        top_button_frame.grid(row=0, column=0, sticky=styling.sticky_new, pady=(0, 10))
        top_button_frame.rowconfigure(0, weight=0)

        # Icon Button Frame: config manually to play with weights
        top_button_frame.columnconfigure(0, weight=0)
        top_button_frame.columnconfigure(1, weight=0)
        top_button_frame.columnconfigure(2, weight=0)
        top_button_frame.columnconfigure(3, weight=0)
        top_button_frame.columnconfigure(4, weight=0)
        top_button_frame.columnconfigure(5, weight=0)
        top_button_frame.columnconfigure(6, weight=0)
        top_button_frame.columnconfigure(7, weight=0)
        top_button_frame.columnconfigure(8, weight=0)

        # import os
        # from disappeer import images
        # image_path = os.path.dirname(images.__file__) + '/'

        # File handling buttons
        save_path = self.image_path + "save_icon.png"
        save_image = tkinter.PhotoImage(file=save_path)
        self.save_button = tkinter.Button(top_button_frame, text='Save', image=save_image, **styling.icon_button_args)
        self.save_button.photo = save_image
        self.save_button.grid(row=0, column=0, sticky=styling.sticky_all, padx=(10, 10))

        open_path = self.image_path + "open_icon.png"
        open_image = tkinter.PhotoImage(file=open_path)
        self.open_button = tkinter.Button(top_button_frame, image=open_image, **styling.icon_button_args)
        self.open_button.photo = open_image
        self.open_button.grid(row=0, column=1, sticky=styling.sticky_all, padx=(0, 10))

        delete_path = self.image_path + "delete_icon.png"
        delete_image = tkinter.PhotoImage(file=delete_path)
        self.clear_button = tkinter.Button(top_button_frame, image=delete_image, **styling.icon_button_args)
        self.clear_button.photo = delete_image
        self.clear_button.grid(row=0, column=2, sticky=styling.sticky_all, padx=(0, 10))

        # Separator
        separator = ttk.Separator(top_button_frame, orient='vertical')
        separator.grid(row=0, column=3, sticky=styling.sticky_all, padx=(10, 10))

        # Key dropdown var and menu
        self.console_key_option_var = tkinter.StringVar()
        self.console_key_option_var.set("Key")

        temp_list_1 = ["One", "Two", "Three"]
        self.console_key_dropdown = ttk.OptionMenu(top_button_frame,
                                                   self.console_key_option_var,
                                                   "Key",
                                                   *temp_list_1)
        # Give it a constant width so it does not resize when option selection changes
        self.console_key_dropdown.configure(width='15')
        self.console_key_dropdown = styling.config_local_dropdown(self.console_key_dropdown)
        self.console_key_dropdown.grid(row=0, column=4, sticky='W', padx=(15, 10))

        # FUnction dropdown var and menu
        self.console_function_option_var = tkinter.StringVar()
        self.console_function_option_var.set("Key")

        temp_list_2 = ["TMP_Encrypt", "TMP_Decrypt", "TMP_Import", 'TMP_Export', 'TMP_Sign', 'TMP_Verify']
        self.console_function_dropdown = ttk.OptionMenu(top_button_frame,
                                                        self.console_function_option_var,
                                                        "Function",
                                                        *temp_list_2)
        self.console_function_dropdown = styling.config_local_dropdown(self.console_function_dropdown)
        self.console_function_dropdown.grid(row=0, column=5, sticky='W', padx=(0, 10))

        run_path = self.image_path + "run_icon.png"
        run_image = tkinter.PhotoImage(file=run_path)
        self.run_button = tkinter.Button(top_button_frame, image=run_image, **styling.icon_button_args)
        self.run_button.photo = run_image
        self.run_button.grid(row=0, column=6, sticky='W', padx=(0, 10))

    def config_text_box(self):
        # TEXT AREA
        self.console_text_box = tkinter.Text(self, **styling.console_text_area_args)
        self.console_text_box.grid(row=1, column=0, sticky=styling.sticky_all, pady=(0, 10))

    def get_console_text(self):
        """
        Get text from console text box
        :return: text
        """
        text = self.console_text_box.get('1.0', 'end-1c')
        return text

    def clear_console_text_box(self):
        """
        Delete contents of console text box.
        """
        self.console_text_box.delete('1.0', 'end')

    def print_to_console_text_box(self, msg):
        self.clear_console_text_box()
        self.console_text_box.insert('1.0', msg)


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


class ConsoleFunctionDropdownHandler:

    def __init__(self, key_info_option_var, key_info_dropdown):
        self.key_info_option_var = key_info_option_var
        self.key_info_dropdown = key_info_dropdown

    def set(self, new_list):
        if len(new_list) == 0:
            new_list = ["ERROR"]
        self.key_info_option_var.set("Functions")
        self.key_info_dropdown['menu'].delete(0, 'end')
        for item in new_list:
            self.key_info_dropdown['menu'].add_command(label=item, command=lambda value=item: self.key_info_option_var.set(value))


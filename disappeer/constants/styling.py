"""
styling.py

Constants for view styling

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import tkinter.ttk as ttk

sticky_all = ('N', 'S', 'E', 'W')
sticky_ew = ('E', 'W')
sticky_new = ('N', 'E', 'W')

# Dark Theme

# Colors
dark_purple = '#992299'

background_color = '#39393a'
foreground_color = 'white'
active_background_color = 'grey33'
select_background_color = dark_purple

font_big = ("Helvetica", 14)
font_small = ("Helvetica", 12)
font_ten = ("Helvetica", 10)

label_args = dict(background=background_color,
                  foreground=foreground_color,
                  font=font_big)

label_args_small_font = dict(background=background_color,
                             foreground=foreground_color,
                             font=font_small)

label_frame_args = dict(background=background_color,
                        foreground='white',
                        labelanchor='n',
                        padx=20,
                        pady=10)

radio_button_args = dict(background=background_color,
                         activebackground=background_color,
                         foreground=foreground_color,
                         activeforeground=foreground_color,
                         relief='flat',
                         font=font_big,
                         highlightthickness=0,
                         selectcolor='black'
                         )

entry_field_args = dict(background='grey10',
                        foreground=foreground_color,
                        font=font_big,
                        highlightthickness=0,
                        insertbackground='white',
                        selectbackground=select_background_color,
                        readonlybackground='grey10'
                        )

entry_field_readonly_args = dict(background='grey10',
                                 foreground=foreground_color,
                                 font=font_big,
                                 highlightthickness=0,
                                 insertbackground='white',
                                 selectbackground='grey10',
                                 selectforeground=foreground_color,
                                 readonlybackground='grey10',
                                 )

entry_field_special_readonly_args = dict(background=background_color,
                                 foreground=foreground_color,
                                 font=font_big,
                                 highlightthickness=0,
                                 insertbackground=background_color,
                                 selectbackground=background_color,
                                 selectforeground=foreground_color,
                                 readonlybackground=background_color,
                                relief='flat'
                                 )

entry_field_label_clone_copy_paste_args = dict(background=background_color,
                                               foreground=foreground_color,
                                               font=font_big,
                                               highlightthickness=0,
                                               insertbackground=background_color,
                                               selectbackground=select_background_color,
                                               selectforeground=foreground_color,
                                               readonlybackground=background_color,
                                               relief='flat')

entry_field_label_clone_copy_paste_args_font_small = dict(background=background_color,
                                                          foreground=foreground_color,
                                                          font=font_small,
                                                          highlightthickness=0,
                                                          insertbackground=background_color,
                                                          selectbackground=select_background_color,
                                                          selectforeground=foreground_color,
                                                          readonlybackground=background_color,
                                                          relief='flat')

check_button_styling = dict(background=background_color,
                            foreground=foreground_color,
                            activebackground=background_color,
                            activeforeground=foreground_color,
                            font=font_big,
                            selectcolor='grey10',
                            highlightthickness=0)

# noinspection PyTypeChecker
menu_bar_styling = dict(tearoff=0,
                        background=background_color,
                        foreground=foreground_color,
                        activebackground=active_background_color,
                        activeforeground=foreground_color,
                        font=('Helvetica', 12, 'bold')
                        )

debug_text_area = dict(font=('Helvetica', 12),
                       borderwidth=0,
                       relief='flat',
                       height=10,
                       width=30,
                       highlightthickness=0,
                       foreground='white',
                       background='black',
                       insertbackground='white',
                       wrap='word'
                       )

console_text_area_args = dict(font=('Helvetica', 14),
                              borderwidth=0,
                              relief='flat',
                              highlightthickness=0,
                              foreground='white',
                              background='black',
                              insertbackground='white',
                              wrap='word',
                              padx=5,
                              pady=5
                              )

icon_button_args = dict(background=background_color,
                        activebackground=active_background_color,
                        borderwidth=0,
                        relief='flat',
                        highlightthickness=0)

# kwarg dictionaries for styling popup form frames
new_key_elements_frame = {'borderwidth': 2,
                          'relief': 'ridge',
                          'background': background_color,
                          'padx': 20,
                          'pady': 20
                          }

display_message_infobox_frame = {'borderwidth': 2,
                                 'relief': 'ridge',
                                 'background': background_color,
                                 'padx': 5,
                                 'pady': 5
                                 }

display_message_text_area_args = {'font': font_small,
                            'borderwidth': 0,
                            'relief': 'flat',
                            'highlightthickness': 0,
                            'highlightcolor': background_color,
                            'foreground': foreground_color,
                            'background': background_color,
                            'width': 50,
                            'wrap': 'word'
                            }

file_viewer_text_area_args = {'font': font_small,
                              'borderwidth': 1,
                              'relief': 'ridge',
                              'highlightthickness': 0,
                              'highlightcolor': background_color,
                              'foreground': foreground_color,
                              'background': 'black',
                              'width': 35,
                              'height': 10,
                              'wrap': 'word'
                              }

alert_box_text_area_args = {'font': font_big,
                            'borderwidth': 0,
                            'relief': 'flat',
                            'highlightthickness': 0,
                            'highlightcolor': background_color,
                            'foreground': foreground_color,
                            'background': background_color,
                            'width': 50,
                            'wrap': 'word'
                            }

alert_box_elements_frame = {'borderwidth': 2,
                            'relief': 'ridge',
                            'background': background_color,
                            'padx': 10,
                            'pady': 10
                            }


def config_ttk_styling():
    """
    Configure all necessary ttk  
    RUn this function locally in view classes as necessary for widget styling.
    See example: http://stackoverflow.com/questions/23038356/change-color-of-tab-header-in-ttk-notebook
    """

    # Init style, and default theme
    style = ttk.Style()
    style.theme_use("alt")

    # Style Notebook and Tabs
    style.configure('TNotebook',
                    tabmargins=(2, 10, 2, 0),
                    background=background_color,
                    borderwidth=1)
    style.configure('TNotebook.Tab',
                    padding=(5, 1),
                    background=background_color,
                    foreground=foreground_color,
                    font=font_big)
    style.map('TNotebook.Tab',
              background=[("selected", active_background_color)],
              foreground=[("selected", foreground_color)],
              expand=[("selected", [1, 1, 1, 0])]
              )

    # Style Basic Button
    style.configure('TButton',
                    foreground=foreground_color,
                    background=background_color,
                    font=font_big,
                    focuscolor='black')
    style.map('TButton', background=[('active', active_background_color)])

    # Style Basic Button
    style.configure('Small.TButton',
                    foreground=foreground_color,
                    background=background_color,
                    font=font_small,
                    focuscolor='black')

    # Style the drop down list/menu button
    # Dropdown menu object/widget itself must be styled locally
    style.configure('TMenubutton',
                    foreground=foreground_color,
                    background=background_color,
                    font=font_small)
    style.map('TMenubutton', background=[('active', active_background_color)])

    style.configure('Small.TMenubutton', font=font_ten)

    # Style Basic ttk Entry
    # style.configure('TEntry',
    #                 foreground=foreground_color,
    #                 fieldbackground='gray10',
    #                 selectbackground=select_background_color,
    #                 pady=20
    #                 )
    # # Style ReadOnly Entry
    # style.configure('Readonly.TEntry',
    #                 foreground=foreground_color,
    #                 selectbackground='black',
    #                 state='readonly'
    #                 )
    # style.map('Readonly.TEntry',
    #           fieldbackground=[('readonly', 'black')],
    #           fieldforeground=[('readonly', 'white')])

    # Separator object
    style.configure('TSeparator', background=active_background_color)



    # Style Treeview Object
    style.configure('Treeview',
                    background=background_color,
                    foreground=foreground_color,
                    fieldbackground=background_color,
                    indent=10
                    )

    style.configure('Treeview.Heading',
                    background=background_color,
                    foreground=foreground_color,
                    font=font_small)

    style.map('Treeview.Heading', background=[('active', background_color)])

    style.configure('Treeview.Cell', padding=0)


def config_local_dropdown(dropdown_widget, size=font_small):
    dropdown_widget['menu']['background'] = background_color
    dropdown_widget['menu']['foreground'] = foreground_color
    dropdown_widget['menu']['activebackground'] = active_background_color
    dropdown_widget['menu']['activeforeground'] = foreground_color
    dropdown_widget['menu']['font'] = size
    return dropdown_widget
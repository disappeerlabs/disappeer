"""
helpers.py

Module with app utility helper functions

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import datetime
import os
import pathlib


def get_date_time_stamp(secs):
    """
    Take epoch secs int as input, return datetime stamp
    """
    converted = float(secs)
    return datetime.datetime.fromtimestamp(converted).strftime('%m/%d/%Y')


def get_local_ipaddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 53))
    result = s.getsockname()[0]
    s.close()
    return result


def get_images_dir_path():
    from disappeer import images
    return os.path.dirname(images.__file__) + '/'


def get_user_home_dir():
    return pathlib.Path.home()

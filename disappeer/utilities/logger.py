"""
applogger.py

Custom logger object and some helpful decorators

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import logging
import sys
import types
from disappeer.constants import constants
import time
from functools import wraps
log = logging.getLogger(constants.title)


def func_debug(logger):
    def decorator(func):
        def debug_wrapper(*args, **kwargs):
            AppLogger.print_red('[FUNC DEBUG DECORATOR]')
            err = "Function called: {}.{}".format(func.__module__, func.__name__)
            logger.debug(err)
            AppLogger.print_red('[/FUNC DEBUG DECORATOR]')
            return func(*args, **kwargs)
        return debug_wrapper
    return decorator


def timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        t1 = time.time()
        result = f(*args, **kw)
        t2 = time.time()
        dif = round(t2 - t1, 3)
        msg = "{}: {}s".format( f.__qualname__, dif)
        AppLogger.print_green(msg)
        return result
    return wrap


class AppLogger:
    """
    Basic application logger class with colorized output stream.
    """

    colors = types.SimpleNamespace(green='\033[92m{}\033[00m',
                                   blue='\033[94m{}\033[00m',
                                   yellow='\033[93m{}\033[00m',
                                   red='\033[92m{}\033[00m',
                                   purple='\033[95m{}\033[00m')

    format_config = '[%(module)s][ln:%(lineno)d][%(funcName)s][%(asctime)s.%(msecs)d]\n    %(levelname)s: %(message)s'
    alt_format_config = '[%(asctime)s.%(msecs)d][%(funcName)s][%(module)s][ln:%(lineno)d]\n    %(levelname)s: %(message)s'
    msg_format_config = '%(message)s'
    time_config = '%H:%M:%S'

    def __init__(self, name,  level=logging.DEBUG, stream=True, file=None):
        self.name = name
        self.level = level
        self.stream = stream
        self.file = file
        self.debug_formatter = logging.Formatter(self.format_config, self.time_config)
        self.alt_formatter = logging.Formatter(self.alt_format_config)
        self.msg_formatter = logging.Formatter(self.msg_format_config)
        self.applogger = None
        self.stream_handler = None
        self.file_handler = None

    def create(self):
        self.applogger = logging.getLogger(self.name)
        self.applogger.setLevel(self.level)
        if self.stream:
            self.stream_handler = self.add_stream_handler()
        if self.file is None:
            self.add_colors()
        if self.file is not None:
            self.file_handler = self.add_file_handler()
        self.add_custom_methods()
        return self.applogger

    def add_custom_methods(self):
        method_list = [self.handle_uncaught_system_exception, self.handle_uncaught_tkinter_exception,
                       self.get_stack, self.write_to_level, self.inspect_dict, self.inspect_obj,
                       self.print_red, self.print_cyan, self.print_black, self.print_green, self.print_lightgray,
                       self.print_lightpurple, self.print_purple, self.print_yellow]
        for item in method_list:
            setattr(self.applogger, item.__name__, item)

    def add_file_handler(self):
        from logging import handlers
        file_handler = handlers.RotatingFileHandler(self.file, maxBytes=1024*1024, backupCount=5)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(self.alt_formatter)
        self.applogger.addHandler(file_handler)
        return file_handler

    def add_stream_handler(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.level)
        stream_handler.setFormatter(self.debug_formatter)
        self.applogger.addHandler(stream_handler)
        return stream_handler

    def handle_uncaught_system_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.print_red('[UNCAUGHT SYSTEM EXCEPTION]')
        self.applogger.critical("UNCAUGHT EXCEPTION", exc_info=(exc_type, exc_value, exc_traceback), stack_info=True)
        self.print_red('[/UNCAUGHT SYSTEM EXCEPTION]')
        sys.exit()

    def handle_uncaught_tkinter_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.print_red('[UNCAUGHT TKINTER EXCEPTION]')
        self.applogger.critical("UNCAUGHT EXCEPTION", exc_info=(exc_type, exc_value, exc_traceback), stack_info=True)
        self.print_red('[/UNCAUGHT TKINTER EXCEPTION]')
        # sys.exit()

    def add_colors(self):
        """
        Add colors to each logging level.
        """
        logging.addLevelName(logging.DEBUG, self.colors.green.format(logging.getLevelName(logging.DEBUG)))
        logging.addLevelName(logging.INFO, self.colors.blue.format(logging.getLevelName(logging.INFO)))
        logging.addLevelName(logging.WARNING, self.colors.yellow.format(logging.getLevelName(logging.WARNING)))
        logging.addLevelName(logging.ERROR, self.colors.purple.format(logging.getLevelName(logging.ERROR)))
        logging.addLevelName(logging.CRITICAL, self.colors.red.format(logging.getLevelName(logging.CRITICAL)))

    def get_stack(self, msg, level=logging.DEBUG):
        self.print_red('')
        self.print_red("[BEGIN STACK TRACE]")
        self.applogger.log(self.level, msg, stack_info=True)
        self.print_red("[/END STACK TRACE]")
        self.print_red('')

    def write_to_level(self, level, log_string):
        if level in [logging.DEBUG, 'd']:
            self.applogger.debug(log_string)
        elif level in [logging.INFO, 'i']:
            self.applogger.info(log_string)
        elif level in [logging.ERROR, 'e']:
            self.applogger.error(log_string)
        elif level in [logging.WARNING, 'w']:
            self.applogger.warning(log_string)
        elif level in [logging.CRITICAL, 'c']:
            self.applogger.critical(log_string)

    def inspect_obj(self, obj, level=logging.DEBUG):
        """
        Log basic info on obj
        """
        parameters = (id(obj), type(obj), len(obj), sys.getsizeof(obj), obj, sys._getframe().f_back.f_code.co_name)

        log_string = \
            "***** Object Info *****\n"\
            "\t   id: {}\n"\
            "\t   type: {}\n"\
            "\t   len: {}\n"\
            "\t   size: {}\n"\
            "\t   self: {}\n"\
            "\t   caller: {}\n"\

        log_string = log_string.format(*parameters)
        self.write_to_level(level, log_string)

    def inspect_dict(self, d, level=logging.DEBUG):
        """
        Log basic info on dictionary d.
        :param d: dictionary to display
        :param level: to log
        """
        if not isinstance(d, type({})):
            self.write_to_level('error', "LogError: {} is not a dict.".format(d))
            return

        log_string = ''
        # Header
        log_string += "***** Dictionary Info *****\n"
        # Num keys
        log_string += "\t   Num Keys: {}\n".format(len(d.keys()))
        # Secondary Header
        log_string += "\t   *** Key/Val Pairs ***\n"
        # Key val pairs
        for item in d:
            current = "\t   {}: {}\n".format(item,  d[item])
            log_string += current

        self.write_to_level(level, log_string)

    # Lambda functions to print in color
    # Source: http://stackoverflow.com/a/34443116
    @staticmethod
    def print_red(prt): print("\033[91m{}\033[00m".format(prt))

    @staticmethod
    def print_green(prt): print("\033[92m{}\033[00m".format(prt))

    @staticmethod
    def print_yellow(prt): print("\033[93m{}\033[00m".format(prt))

    @staticmethod
    def print_lightpurple(prt): print("\033[94m{}\033[00m".format(prt))

    @staticmethod
    def print_purple(prt): print("\033[95m{}\033[00m".format(prt))

    @staticmethod
    def print_cyan(prt): print("\033[96m{}\033[00m".format(prt))

    @staticmethod
    def print_lightgray(prt): print("\033[97m{}\033[00m".format(prt))

    @staticmethod
    def print_black(prt): print("\033[98m{}\033[00m".format(prt))


if __name__ == '__main__':
    applogger = AppLogger("DefaultLogger", file='log.txt').create()
    applogger.info("Testing INFO")
    applogger.debug("Testing DEBUG")
    applogger.warning("Testing WARNING")
    applogger.error("Testing ERROR")
    applogger.critical("Testing CRITICAL")
    d = dict(key1='val1', key2='val2')
    applogger.inspect_dict(d, level=logging.INFO)
    applogger.inspect_dict(d, level=logging.WARNING)
    applogger.inspect_obj(d)
    applogger.print_cyan('hello there, this is colorized')
    applogger.get_stack('trying to get stack')

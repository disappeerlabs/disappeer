"""
invoker.py

Module for command pattern Invoker object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


class Invoker:

    @classmethod
    def execute(cls, command):
        command.execute()

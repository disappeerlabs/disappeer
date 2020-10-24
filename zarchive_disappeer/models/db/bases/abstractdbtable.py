"""
abstractdbtable.py

Module for AbstractDBTable class object, interface for all DB Table classes

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import abc
import collections
from disappeer.models.db import dbexecutor


class AbstractDBTable(dbexecutor.DBExecutor, metaclass=abc.ABCMeta):

    def __init__(self, db_file_path):
        super().__init__(db_file_path)
        self.create_table()

    @property
    @abc.abstractmethod
    def table_name(self):
        """Name for this table"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def data_row_name(self):
        """Name for table data row named tuple objects"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def column_names_tuple(self):
        """Tuple of strings with table column names"""
        raise NotImplementedError

    @property
    def create_table_string(self):
        prefix_string = "create table if not exists {} (id integer primary key autoincrement, ".format(self.table_name)
        postfix_string = ");"
        final = prefix_string + self.col_def_string + postfix_string
        return final

    @property
    def col_def_string(self):
        """Default creates all text cols, override for custom defs"""
        col_name_string_list = [x + ' TEXT' for x in self.column_names_tuple]
        joined = ", ".join(col_name_string_list)
        return joined

    def create_table(self):
        self.execute(self.create_table_string)

    def create_empty_named_tuple(self):
        row_tuple_obj = collections.namedtuple(self.data_row_name, self.column_names_tuple)
        return row_tuple_obj

    def build_named_tuple(self, data_row):
        row_tuple_obj = self.create_empty_named_tuple()
        final = row_tuple_obj(*data_row)
        return final

    @property
    def insert_command_string(self):
        prefix_string = 'insert into {} values(null, '.format(self.table_name)
        postfix_string = ')'
        var_string = ['?' for x in self.column_names_tuple]
        joined = ", ".join(var_string)
        final = prefix_string + joined + postfix_string
        return final

    def insert_data_row(self, data_row):
        command = self.insert_command_string
        self.execute(command, data_row)

    def fetch_last_record(self):
        command = 'select * from {} where ID = (select max(ID) from {})'.format(self.table_name, self.table_name)
        result = self.fetch_all(command)
        final = self.build_named_tuple(result[0][1:])
        return final

    def delete_record_where_x_equals_y(self, col_name, value):
        command = "delete from {} where {}='{}'".format(self.table_name, col_name, value)
        self.execute(command)

    def update_record_col_to_val_where_x_equals_y(self, target_col, new_val, where_col, where_val):
        command = "update {} set {}='{}' where {}='{}'".format(self.table_name,
                                                               target_col,
                                                               new_val,
                                                               where_col,
                                                               where_val)
        self.execute(command)
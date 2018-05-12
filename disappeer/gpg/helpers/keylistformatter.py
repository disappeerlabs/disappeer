"""
keylistformatter.py

Module for KeyListFormatter class object.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""


class KeyListFormatter:

    def format(self, raw_key_list):
        userid_and_key_id_tuple_list = self.create_userid_and_keyid_tuple_list(raw_key_list)
        result = self.process_key_dropdown_list_strings(userid_and_key_id_tuple_list)
        return result

    def create_userid_and_keyid_tuple_list(self, raw_key_list):
        userid_and_keyid_tuple_list = []
        for item in raw_key_list:
            name = item['uids'][0]
            key_id = item['keyid']
            pack = (name, key_id)
            userid_and_keyid_tuple_list.append(pack)
        return userid_and_keyid_tuple_list

    def process_key_dropdown_list_strings(self, key_tuple_list):
        processed = []
        for item in key_tuple_list:
            name_tuple = self.process_key_uid(item[0])
            key_id = item[1]
            spacer = ', '
            structured = name_tuple[0] + spacer + name_tuple[-1] + spacer + key_id
            processed.append(structured)
        return processed

    def process_key_uid(self, key_uid):
        split = key_uid.split()
        result = (split[0], split[-1])
        return result


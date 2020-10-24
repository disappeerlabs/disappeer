"""
test_databasefacade.py

Test suite for the DatabaseFacade module and class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
from disappeer.models.db import databasefacade
from disappeer.utilities import observable
from disappeer.models.db import dbcontactrequesttable
from disappeer.models.db import dbpendingcontactresponsetable
from disappeer.models.db import dbpeercontactstable
from disappeer.models.db import dbsentmessagestable
from disappeer.models.db import dbreceivedmessagestable
from disappeer.models.db import dbserversynctable
import os
from disappeer import settings
from disappeer.utilities import dirmaker
import shutil


class TestImports(unittest.TestCase):

    def test_observable(self):
        self.assertEqual(observable, databasefacade.observable)

    def test_dbcontactrequesttable(self):
        self.assertEqual(dbcontactrequesttable, databasefacade.dbcontactrequesttable)

    def test_dbpendingcontactresponsetable(self):
        self.assertEqual(dbpendingcontactresponsetable, databasefacade.dbpendingcontactresponsetable)

    def test_dbpeercontactstable(self):
        self.assertEqual(dbpeercontactstable, databasefacade.dbpeercontactstable)

    def test_dbsentmessagestable(self):
        self.assertEqual(dbsentmessagestable, databasefacade.dbsentmessagestable)

    def test_dbreceivedmessagestable(self):
        self.assertEqual(dbreceivedmessagestable, databasefacade.dbreceivedmessagestable)

    def test_settings(self):
        self.assertEqual(settings, databasefacade.settings)

    def test_dbserversynctable(self):
        self.assertEqual(dbserversynctable, databasefacade.dbserversynctable)


class TestClassBasics(unittest.TestCase):

    def setUp(self):
        self.tmp_db_path = 'models/db/tests/tmpfacadedb.sqlite'
        self.key_text = 'xxx,yyy,zzz'
        self.alt_key_text = 'aaa,bbb,ccc'
        self.host_key_observer = observable.Observable(self.key_text)
        self.dir_maker_test_dir = 'tests/dbfacadetest/'
        self.dir_maker = dirmaker.DirMaker(self.dir_maker_test_dir)
        self.x = databasefacade.DatabaseFacade(self.host_key_observer, self.dir_maker.get_user_database_dir)

    def tearDown(self):
        if os.path.isfile(self.x.get_full_db_file_path()):
            os.remove(self.x.get_full_db_file_path())
        if os.path.isfile(self.x.get_server_sync_db_path()):
            os.remove(self.x.get_server_sync_db_path())
        if os.path.exists(self.dir_maker_test_dir):
            shutil.rmtree(self.dir_maker_test_dir)

    ###################
    #  CONFIG Methods #
    ###################

    def test_instance(self):
        self.assertIsInstance(self.x, databasefacade.DatabaseFacade)

    def test_host_key_observer_attr_set(self):
        self.assertEqual(self.x.host_key_observer, self.host_key_observer)

    def test_get_user_database_dir_method_attr_set_(self):
        self.assertEqual(self.x.get_user_database_dir_method, self.dir_maker.get_user_database_dir)

    def test_get_database_dir_calls_arg_as_method_returns_result(self):
        arg = 'key_id_name'
        val = 'xxx'
        target = self.x.get_user_database_dir_method = MagicMock(return_value=val)
        result = self.x.get_database_dir(arg)
        target.assert_called_with(arg)
        self.assertEqual(result, target.return_value)

    def test_get_full_db_file_path_creates_string(self):
        key_vals = self.host_key_observer.get()
        split = key_vals.split(',')
        key_id = split.pop().strip()
        suffix = '.sqlite'
        file_name = key_id + suffix
        target = self.x.get_database_dir(key_id) + file_name
        result = self.x.get_full_db_file_path()
        self.assertEqual(result, target)

    def test_set_db_tables_sets_db_table_attr_to_instances_with_current_db_file_obs_val(self):
        target = self.x.get_full_db_file_path()
        self.x.set_db_tables(None)

        self.assertIsInstance(self.x.contact_request_table, dbcontactrequesttable.DBContactRequestTable)
        self.assertEqual(self.x.contact_request_table.database, target)

        self.assertIsInstance(self.x.pending_contact_response_table, dbpendingcontactresponsetable.DBPendingContactResponseTable)
        self.assertEqual(self.x.pending_contact_response_table.database, target)

        self.assertIsInstance(self.x.peer_contacts_table, dbpeercontactstable.DBPPeerContactsTable)
        self.assertEqual(self.x.peer_contacts_table.database, target)

        self.assertIsInstance(self.x.sent_messages_table, dbsentmessagestable.DBPSentMessagesTable)
        self.assertEqual(self.x.sent_messages_table.database, target)

        self.assertIsInstance(self.x.received_messages_table, dbreceivedmessagestable.DBPReceivedMessagesTable)
        self.assertEqual(self.x.received_messages_table.database, target)

    def test_config_data_context_adds_set_db_tables_method_to_path_obs_callbacks(self):
        self.x.config_data_context()
        self.assertIn(self.x.set_db_tables, self.x.host_key_observer.callbacks)

    def test_config_data_context_called_by_init(self):
        self.assertIn(self.x.set_db_tables, self.x.host_key_observer.callbacks)

    def test_set_db_tables_called_by_init(self):
        self.assertEqual(self.x.get_full_db_file_path(), self.x.contact_request_table.database)

    def test_new_database_created_when_host_key_changes(self):
        self.host_key_observer.set(self.alt_key_text)
        new_dir = self.x.get_full_db_file_path()
        name = self.alt_key_text.split(',').pop().strip()
        self.assertIn(name, self.x.contact_request_table.database)

    ###################
    #  Insert Methods #
    ###################

    def test_insert_contact_request_table_calls_handle_new_payload_on_contact_req_table(self):
        target = self.x.contact_request_table.handle_new_payload = MagicMock()
        payload = dict()
        self.x.insert_contact_request(payload)
        target.assert_called_with(payload)

    def test_insert_pending_contact_response_table_calls_handle_new_payload_on_pending_contact_res_table(self):
        target = self.x.pending_contact_response_table.handle_new_payload = MagicMock()
        payload = dict()
        self.x.insert_pending_contact_response(payload)
        target.assert_called_with(payload)

    def test_insert_pending_contact_response_table_calls_update_server_sync_method(self):
        sub = self.x.pending_contact_response_table.handle_new_payload = MagicMock()
        payload = dict()
        target = self.x.update_server_sync_db = MagicMock()
        self.x.insert_pending_contact_response(payload)
        target.assert_called_with()

    def test_insert_peer_contacts_table_calls_handle_new_payload_on_peer_contacts_table(self):
        target = self.x.peer_contacts_table.handle_new_payload = MagicMock()
        payload = dict()
        self.x.insert_peer_contact(payload)
        target.assert_called_with(payload)

    def test_insert_sent_messages_table_calls_handle_new_payload_on_sent_messages_table(self):
        target = self.x.sent_messages_table.handle_new_payload = MagicMock()
        payload = dict()
        self.x.insert_sent_message(payload)
        target.assert_called_with(payload)

    def test_insert_recvd_messages_table_calls_handle_new_payload_on_recvd_messages_table(self):
        target = self.x.received_messages_table.handle_new_payload = MagicMock()
        payload = dict()
        self.x.insert_received_message(payload)
        target.assert_called_with(payload)

    ###################
    #  Delete Methods #
    ###################

    def test_delete_contact_request_table_where_x_is_y_calls_delete_on_contact_req_table(self):
        target = self.x.contact_request_table.delete_record_where_x_equals_y = MagicMock()
        x = 1
        y = 2
        self.x.delete_contact_request_where_x_is_y(x, y)
        target.assert_called_with(x, y)

    def test_delete_pending_contact_response_where_x_is_y_calls_delete_on_pending_res_table(self):
        target = self.x.pending_contact_response_table.delete_record_where_x_equals_y = MagicMock()
        x = 1
        y = 2
        self.x.delete_pending_contact_response_where_x_is_y(x, y)
        target.assert_called_with(x, y)

    def test_delete_pending_contact_response_where_x_is_y_calls_update_server_sync_method(self):
        sub = self.x.pending_contact_response_table.delete_record_where_x_equals_y = MagicMock()
        x = 1
        y = 2
        target = self.x.update_server_sync_db = MagicMock()
        self.x.delete_pending_contact_response_where_x_is_y(x, y)
        target.assert_called_with()

    def test_delete_peer_contact_where_x_is_y_calls_delete_on_peer_contacts_table(self):
        target = self.x.peer_contacts_table.delete_record_where_x_equals_y = MagicMock()
        x = 1
        y = 2
        self.x.delete_peer_contact_where_x_is_y(x, y)
        target.assert_called_with(x, y)

    def test_delete_peer_contact_by_fingerprint_calls_delete_on_peer_contacts_table(self):
        target = self.x.peer_contacts_table.delete_record_where_x_equals_y = MagicMock()
        x = 'gpg_fingerprint'
        y = 2
        self.x.delete_peer_contact_by_fingerprint(y)
        target.assert_called_with(x, y)

    def test_delete_sent_message_where_x_is_y_calls_delete_on_sent_msg_table(self):
        target = self.x.sent_messages_table.delete_record_where_x_equals_y = MagicMock()
        x = 1
        y = 2
        self.x.delete_sent_message_where_x_is_y(x, y)
        target.assert_called_with(x, y)

    def test_delete_recvd_message_where_x_is_y_calls_delete_on_recvd_msg_table(self):
        target = self.x.received_messages_table.delete_record_where_x_equals_y = MagicMock()
        x = 1
        y = 2
        self.x.delete_received_message_where_x_is_y(x, y)
        target.assert_called_with(x, y)

    ###################
    #  Fetch Methods  #
    ###################

    def test_fetch_contact_request_pub_key_by_nonce_calls_method_on_table(self):
        nonce_string = 'nonce_string'
        val = 'val'
        target = self.x.contact_request_table.fetch_gpg_pub_key_by_nonce = MagicMock(return_value=val)
        result = self.x.fetch_contact_request_pub_key_by_nonce(nonce_string)
        target.assert_called_with(nonce_string)
        self.assertEqual(result, target.return_value)

    def test_fetch_contact_response_pub_key_by_nonce_calls_method_on_table(self):
        nonce_string = 'nonce_string'
        val = 'val'
        target = self.x.pending_contact_response_table.fetch_gpg_pub_key_by_nonce = MagicMock(return_value=val)
        result = self.x.fetch_contact_response_pub_key_by_nonce(nonce_string)
        target.assert_called_with(nonce_string)
        self.assertEqual(result, target.return_value)

    def test_fetch_contact_response_pub_key_by_fingerprint_calls_method_on_table(self):
        fingerprint_string = 'fingerprint_string'
        val = 'val'
        target = self.x.pending_contact_response_table.fetch_gpg_pub_key_by_fingerprint = MagicMock(return_value=val)
        result = self.x.fetch_contact_response_pub_key_by_fingerprint(fingerprint_string)
        target.assert_called_with(fingerprint_string)
        self.assertEqual(result, target.return_value)

    def test_fetch_peer_contact_tuple_row_by_fingerprint_calls_method_on_table(self):
        fingerprint = 'fingerprint_string'
        val = 'val'
        target = self.x.peer_contacts_table.fetch_named_tuple_row_by_fingerprint = MagicMock(return_value=val)
        result = self.x.fetch_peer_contact_tuple_row_by_fingerprint(fingerprint)
        target.assert_called_with(fingerprint)
        self.assertEqual(result, target.return_value)

    def test_fetch_all_contact_request_address_and_nonce_calls_method_on_table(self):
        val = 'val'
        target = self.x.contact_request_table.fetch_all_address_and_nonce = MagicMock(return_value=val)
        result = self.x.fetch_all_contact_request_address_and_nonce()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_fetch_all_contact_request_address_and_nonce_with_status_calls_method_on_table(self):
        val = 'val'
        target = self.x.contact_request_table.fetch_all_address_and_nonce_with_status = MagicMock(return_value=val)
        result = self.x.fetch_all_contact_request_address_and_nonce_with_status()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_fetch_one_contact_request_by_nonce_calls_method_on_table(self):
        nonce = 'nonce_string'
        val = 'val'
        target = self.x.contact_request_table.fetch_one_by_nonce = MagicMock(return_value=val)
        result = self.x.fetch_one_contact_request_by_nonce(nonce)
        target.assert_called_with(nonce)
        self.assertEqual(result, target.return_value)

    def test_fetch_all_pending_contact_response_hosts_and_fingerprints_calls_method_on_table(self):
        val = 'val'
        target = self.x.pending_contact_response_table.fetch_all_hosts_and_fingerprints = MagicMock(return_value=val)
        result = self.x.fetch_all_pending_contact_response_hosts_and_fingerprints()
        target.assert_called_with()
        self.assertEqual(target.return_value, result)

    def test_fetch_all_peer_contact_uids_and_fingerprints_calls_method_on_table(self):
        val = 'val'
        target = self.x.peer_contacts_table.fetch_all_uids_and_fingerprints = MagicMock(return_value=val)
        result = self.x.fetch_all_peer_contact_uids_and_fingerprints()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_fetch_all_peer_contact_uids_and_fingerprints_with_status_calls_method_on_table(self):
        val = 'val'
        target = self.x.peer_contacts_table.fetch_all_uids_and_fingerprints_and_status = MagicMock(return_value=val)
        result = self.x.fetch_all_peer_contact_uids_and_fingerprints_with_status()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_fetch_one_peer_contact_named_tuple_row_by_fingerprint_calls_method_on_table(self):
        val = 'val'
        fingerprint = 'fingerprint'
        target = self.x.peer_contacts_table.fetch_named_tuple_row_by_fingerprint = MagicMock(return_value=val)
        result = self.x.fetch_one_peer_contact_named_tuple_row_by_fingerprint(fingerprint)
        target.assert_called_with(fingerprint)
        self.assertEqual(result, target.return_value)

    def test_fetch_all_sent_message_nonces_calls_method_on_table(self):
        val = 'val'
        target = self.x.sent_messages_table.fetch_all_nonces = MagicMock(return_value=val)
        result = self.x.fetch_all_sent_message_nonces()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_fetch_one_sent_message_named_tuple_by_nonce_calls_method_on_table(self):
        val = 'val'
        nonce = 'nonce'
        target = self.x.sent_messages_table.fetch_named_tuple_by_nonce = MagicMock(return_value=val)
        result = self.x.fetch_one_sent_message_named_tuple_by_nonce(nonce)
        target.assert_called_with(nonce)
        self.assertEqual(result, target.return_value)

    def test_fetch_all_received_message_nonces_calls_method_on_table(self):
        val = 'val'
        target = self.x.received_messages_table.fetch_all_nonces = MagicMock(return_value=val)
        result = self.x.fetch_all_received_message_nonces()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_fetch_all_received_message_nonces_with_status_calls_method_on_table(self):
        val = 'val'
        target = self.x.received_messages_table.fetch_all_nonces_with_status = MagicMock(return_value=val)
        result = self.x.fetch_all_received_message_nonces_with_status()
        target.assert_called_with()
        self.assertEqual(result, target.return_value)

    def test_fetch_one_received_message_named_tuple_by_nonce_calls_method_on_table(self):
        val = 'val'
        nonce = 'nonce'
        target = self.x.received_messages_table.fetch_named_tuple_by_nonce = MagicMock(return_value=val)
        result = self.x.fetch_one_received_message_named_tuple_by_nonce(nonce)
        target.assert_called_with(nonce)
        self.assertEqual(result, target.return_value)

    ####################
    #  Update Methods  #
    ####################

    def test_update_received_message_to_read(self):
        nonce = 'nonce_string'
        target = self.x.received_messages_table.update_record_status_to_read = MagicMock()
        self.x.update_received_message_to_read(nonce)
        target.assert_called_with(nonce)

    def test_update_contact_request_col_to_val_where_x_is_y_calls_method_on_table(self):
        target = self.x.contact_request_table.update_record_col_to_val_where_x_equals_y = MagicMock()
        self.x.update_contact_request_col_to_val_where_x_is_y(1, 2, 3, 4)
        target.assert_called_with(1, 2, 3, 4)

    def test_update_peer_contact_address_from_fingerprint_updates_address(self):
        target = self.x.peer_contacts_table.update_record_col_to_val_where_x_equals_y = MagicMock()
        new_addr = 'new_address'
        fingerprint = 'fingerprint_string'
        self.x.update_peer_contact_address_from_fingerprint(new_addr, fingerprint)
        target.assert_called_with('address_host', new_addr, 'gpg_fingerprint', fingerprint)

    def test_update_peer_contact_port_from_fingerprint_updates_port(self):
        target = self.x.peer_contacts_table.update_record_col_to_val_where_x_equals_y = MagicMock()
        new_port = 'new_address'
        fingerprint = 'fingerprint_string'
        self.x.update_peer_contact_port_from_fingerprint(new_port, fingerprint)
        target.assert_called_with('address_port', new_port, 'gpg_fingerprint', fingerprint)

    def test_update_peer_contact_status_to_read(self):
        fingerprint = 'fingerprint_string'
        target = self.x.peer_contacts_table.update_record_status_to_read_by_fingerprint = MagicMock()
        self.x.update_peer_contact_status_to_read(fingerprint)
        target.assert_called_with(fingerprint)

    ###########################
    #  Get Table Ref Methods  #
    ###########################

    def test_get_pending_contact_response_table(self):
        result = self.x.get_pending_contact_response_table()
        self.assertEqual(result, self.x.pending_contact_response_table)

    ###########################
    #  Server Sync DB Related #
    ###########################

    def test_get_server_sync_db_path_returns_correct_path(self):
        name = 'server_sync.sqlite'
        key_vals = self.host_key_observer.get()
        split = key_vals.split(',')
        key_id = split.pop().strip()
        target = self.x.get_database_dir(key_id) + name
        result = self.x.get_server_sync_db_path()
        self.assertEqual(result, target)

    def test_set_server_sync_db_table_called_by_constructor_method(self):
        self.assertIsInstance(self.x.server_sync_table, dbserversynctable.DBServerSyncTable)

    def test_set_server_sync_db_table_sets_attr(self):
        self.x.set_server_sync_db_table()
        self.assertIsInstance(self.x.server_sync_table, dbserversynctable.DBServerSyncTable)
        self.assertEqual(self.x.server_sync_table.database, self.x.get_server_sync_db_path())

    def test_set_server_sync_db_table_calls_update_server_sync_db(self):
        target = self.x.update_server_sync_db = MagicMock()
        self.x.set_server_sync_db_table()
        target.assert_called_with()

    def test_update_server_sync_db(self):
        example_db_pending_row_1 = ('status', 'nonce_1', 'gpg_pub_key', 'gpg_fingerprint', 'host')
        example_db_pending_row_2 = ('status', 'nonce_2', 'gpg_pub_key', 'gpg_fingerprint', 'host')
        self.x.pending_contact_response_table.insert_data_row(example_db_pending_row_1)
        self.x.pending_contact_response_table.insert_data_row(example_db_pending_row_2)
        target = self.x.pending_contact_response_table.fetch_all_nonces()

        self.x.update_server_sync_db()
        result = self.x.server_sync_table.fetch_all_nonces()
        self.assertEqual(result, target)

    def test_set_db_tables_calls_update_server_sync_method(self):
        target = self.x.update_server_sync_db = MagicMock()
        self.x.set_db_tables(None)
        target.assert_called_with()

"""
test_rootcontroller.py

Test suite for root controller module

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.root import rootcontroller
import queue
from disappeer.constants import constants
from disappeer.gpg import gpgcontroller
from disappeer.console import consolecontroller
from disappeer.utilities import queueconsumer
from disappeer.models import gpgdatacontext
from disappeer.net.message import messagefactory
from disappeer.popups import popuplauncher
import types
from disappeer.net.message import messagevalidator
from disappeer.messages import messagescontroller
from disappeer.models import tordatacontext
from disappeer.tornet import tornetcontroller
from disappeer.requests import requestscontroller
from disappeer.root import rootparameters
from disappeer.utilities import logger
from disappeer.models.db import databasefacade
import functools
from disappeer.root.tests.rootsetupclass import RootSetupClass
from disappeer.executor import controllermediator
from disappeer.executor import commandclient


class TestImports(unittest.TestCase):

    def test_constants(self):
        self.assertEqual(constants, rootcontroller.constants)

    def test_log(self):
        self.assertEqual(logger.log, rootcontroller.log)

    def test_gpgcontroller(self):
        self.assertEqual(gpgcontroller, rootcontroller.gpgcontroller)

    def test_queueconsumer(self):
        self.assertEqual(queueconsumer, rootcontroller.queueconsumer)

    def test_consolecontroller(self):
        self.assertEqual(consolecontroller, rootcontroller.consolecontroller)

    def test_popuplauncher(self):
        self.assertEqual(popuplauncher, rootcontroller.popuplauncher)

    def test_messagescontroller(self):
        self.assertEqual(messagescontroller, rootcontroller.messagescontroller)

    def test_tornetcontroller(self):
        self.assertEqual(tornetcontroller, rootcontroller.tornetcontroller)

    def test_requestscontroller(self):
        self.assertEqual(requestscontroller, rootcontroller.requestscontroller)

    def test_root_parameters(self):
        self.assertEqual(rootparameters, rootcontroller.rootparameters)

    def test_functools(self):
        self.assertEqual(functools, rootcontroller.functools)

    def test_controllermediator(self):
        self.assertEqual(controllermediator, rootcontroller.controllermediator)

    def test_commandclient(self):
        self.assertEqual(commandclient, rootcontroller.commandclient)


class TestRootControllerBasicsAndQueueMethods(RootSetupClass):

    payload_dict = dict(desc='Test', data='wtf')
    payload_dict_bad = dict(data='wtf')

    def test_instance(self):
        self.assertIsInstance(self.x, rootcontroller.RootController)

    def test_instance_queue_consumer(self):
        self.assertIsInstance(self.x, queueconsumer.QueueConsumer)

    def test_view_attribute(self):
        name = 'view'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_view_attr_set(self):
        self.assertEqual(self.x.view, self.root_view)

    def test_queue_attribute_is_queue(self):
        self.assertIsInstance(self.x.queue, queue.Queue)

    def test_root_parameters_attr_set(self):
        self.assertIsInstance(self.x.root_params, rootparameters.RootParameters)
        self.assertEqual(self.x.root_params.root, self.x.root)
        self.assertEqual(self.x.root_params.root_view, self.x.view)
        self.assertEqual(self.x.root_params.root_queue, self.x.queue)
        self.assertEqual(self.x.root_params.host_key_observer, self.x.gpg_datacontext.host_key_observer)

    def test_gpg_datacontext_attribute_is_gpgdatacontext(self):
        self.assertIsInstance(self.x.gpg_datacontext, gpgdatacontext.GPGDataContext)

    def test_tor_datacontext_attr_is_tor_datacontect_with_arg(self):
        self.assertIsInstance(self.x.tor_datacontext, tordatacontext.TorDataContext)

    def test_controller_mediator_is_controller_mediator_with_correct_args(self):
        self.assertIsInstance(self.x.controller_mediator, controllermediator.ControllerMediator)
        self.assertEqual(self.x.controller_mediator.database_facade, self.x.database_facade)
        self.assertEqual(self.x.controller_mediator.gpg_datacontext, self.x.gpg_datacontext)
        self.assertEqual(self.x.controller_mediator.tor_datacontext, self.x.tor_datacontext)
        self.assertEqual(self.x.controller_mediator.requests_controller, self.x.requests_controller)
        self.assertEqual(self.x.controller_mediator.message_controller, self.x.message_controller)
        self.assertEqual(self.x.controller_mediator.console_controller, self.x.console_controller)

    def test_command_client_is_command_client_with_controller_mediator_arg(self):
        self.assertIsInstance(self.x.command_client, commandclient.CommandClient)
        self.assertEqual(self.x.command_client.controller_mediator, self.x.controller_mediator)

    @patch.object(rootcontroller.popuplauncher, 'launch_alert_box_popup')
    def test_launch_alert_log_launches_alert_and_log_with_msg(self, alertbox):
        msg = ''
        self.x.launch_alert_log(msg)
        alertbox.assert_called_with(self.x.root, msg)

    def test_update_all_treeviews_calls_update_methods_on_child_controllers(self):
        target_1 = self.x.requests_controller.update_all_treeviews = MagicMock()
        target_2 = self.x.message_controller.update_all_treeviews = MagicMock()
        self.x.update_all_treeviews()
        target_1.assert_called_with()
        target_2.assert_called_with()

    def test_delay_update_all_treeviews_method_calls_root_after_with_update_all_treeviews_method(self):
        target = self.x.root.after = MagicMock()
        self.x.delay_update_all_treeviews(None)
        target.assert_called_with(2000, self.x.update_all_treeviews)

    def test_delay_update_all_treeviews_method_is_added_as_callback_for_host_key_observer(self):
        self.assertIn(self.x.delay_update_all_treeviews, self.x.gpg_datacontext.host_key_observer.callbacks)

    def test_config_menubar_configs_app_menu(self):
        mock_menu = MagicMock()
        target = self.x.root_params.get_app_menu_obj = MagicMock(return_value = mock_menu)
        self.x.config_menubar()
        target.assert_called_with()
        self.assertTrue(mock_menu.add_command.called)

    @patch.object(rootcontroller.RootController, 'config_menubar')
    def test_constructor_calls_config_menubar(self, mocked_method):
        x = self.altsetup()
        self.assertTrue(mocked_method.called)

    def test_exit_method_exits_calls_destroy(self):
        target_net = self.x.tornet_controller.stop_network_services = MagicMock()
        target_tor = self.x.tornet_controller.tor_proxy_controller.stop_all_proxies = MagicMock()
        target_root = self.x.root.quit = MagicMock()
        self.x.exit()
        target_net.assert_called_with()
        target_tor.assert_called_with()
        target_root.assert_called_with()


class TestRootControllerGPGRelated(RootSetupClass):

    def test_gpgcontroller_attribute(self):
        name = 'gpg_controller'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_gpgcontroller_is_gpg_controller(self):
        self.assertIsInstance(self.x.gpg_controller, gpgcontroller.GPGController)

    def test_gpg_controller_root_arg(self):
        self.assertEqual(self.x.gpg_controller.root, self.x.root)

    def test_gpg_controller_view_arg(self):
        self.assertEqual(self.x.gpg_controller.view, self.x.view.left_panel.gpg_frame)

    def test_gpg_controller_queue_arg(self):
        self.assertEqual(self.x.gpg_controller.root_queue, self.x.queue)

    def test_database_facade_is_database_facade_with_args(self):
        self.assertIsInstance(self.x.database_facade, databasefacade.DatabaseFacade)

class TestRootControllerConsoleRelated(RootSetupClass):

    def test_consolecontroller_attribute(self):
        name = 'console_controller'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_console_controller_root_arg(self):
        self.assertEqual(self.x.console_controller.root, self.x.root)

    def test_console_controller_view_arg(self):
        self.assertEqual(self.x.console_controller.view, self.x.view.right_panel.console_frame)

    def test_console_controller_queue_arg(self):
        self.assertEqual(self.x.console_controller.root_queue, self.x.queue)

    def test_console_controller_data_context(self):
        self.assertEqual(self.x.console_controller.gpg_data_context, self.x.gpg_datacontext)


gpg_pub_key_string = '''-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQENBFkV2wYBCADhSKS5957Y/3NPYUO6RVYpTPScMxULQ5fR2bwIZYMvSjZ7rdPM
zlcCg7MbXvFBrzbRKebzt1tmhntBjzi0HnpPcsTslQZyOfiZ3plfiQXGZMdL83t4
g/nxP6i3+TfXafalUnr2Zp3vk9ClWyBFS1Bmzqz97w4S8uhrvMal/TklDJ+3MY8F
vsPpaOgZvCgG27vyoQnay+mVkWgC+bOFnl9tjXCSr2a1seHJpUCmJgT/qba3wVI2
NUdq9fHChY9ug1BHTFm7HvFWntRKPT+682lm3iS8kssdacxFxpheRwj6Qdk+yRQO
Ht+I8T/GtCEF0HlscYhg+7JbLnxMdYhKctTjABEBAAG0N21hY3Rvd2VyIChEZWZh
dWx0IGNvbW1lbnQgbWVzc2FnZSkgPG1hY3Rvd2VyQGVtYWlsLmNvbT6JAT4EEwEC
ACgFAlkV2wYCGy8FCQGqfjoGCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEFWk
Wpn+ReVA4i8IAIW0JB7VEI+q0n2+exWu7uITB6OmSvJ+xadEP6sUwf02Eghppiyg
u181ZE9TpspMNscTxyv03bK9yMqbNgpNQ6LUKzD90Qlut9gl9whxCVDI78VGrCXf
YjTfG5kowCU2mIhJIpUAdb8ufvqZFYo2BnRrsj/heu9+JSYRevs+yTADo2gJGOZQ
LOm+ra8BXyw5SYAwfO+YzyuXw5ITkXppxvL2jvLf62OGNSPF3nEbS/EebJZENtw7
F0fh+9xKao+mJIX6bjAgUlIWvaqsu6W7DKeNf/flYoCnddnP06FvgjCMC9G2II9p
qVw+Ytr7XLZuvjqx84VimuK6y4+DY6shhOC5Ag0EWRXbBhAIALCVLle15qOSsQwr
0sbJ2+sN57ZzNfYOZMUqZbC9YCOPDDu54UtY2nB6oJ54PJZBGp4Fmd5oQgBYuntL
9BMj22MFgWH9Ia8RUuAImGScaGT0/BVyueeWygag0T7AuCN2Mkoed7GaA3Vv3rJf
YdBwlY6rGiIy68iWMFd4E4LCf8XTC6twufvaw0gKS4LuFLCmxEsKYIrRfYDT/MtU
b+tz+g+mxAmolGN7j7WyAdhYNNGKSh3N+AZQbBDUK0Mbrr0sdKOEJBCrN72jygGm
BfIgAkJFQ4XaG/AJ/sOgvXN3vXvzEFQrPgOVVmmVPoBOdU97kzETcEg+ZyQtOSAg
fFi20bMAAwUH/2KnoIigeKqhs8MbGGxEFJHsVxTAMxCj8A+p73+KLEtwm4DSziff
ggxnsPxEAPqwopIErB6DB2DPNVr6b4txQVIh/oe4zMhEpONi9GyTgINChNcjf7VW
Gu7So4s7y1FE2e14Xx/CsI7pICQa/FYZPmTEFOxF6vgPqnp3H2gfR7rG3FsrXZdr
mn9Aov4jCBbOBJ8Ucgfv3F0AIDs32qvuCusjYHRFggzdgtK4D92H5VidE+F0sdJK
314VtZVGcCnrvyNV/OKJ+LsKnskgGOWyYItEm5XJ8BIz1b9MBvXcGrSPPUeAonbE
6Ayl6ogjCn6l1Gn/h/JcsvawNSZLz2rYBjSJASUEGAECAA8FAlkV2wYCGwwFCQGq
fjoACgkQVaRamf5F5UCSkAgAx7gC2263ZPSTQZCJE8uJHeD9Ybik7o1/txaIICMV
vzBxIOBOSSOMVjwxJhQwkj3//WQjBmqNghlsIq5Rfwnj4bNSTrZj8pqDtoqYv1fg
WVhZv4mFF7Uw+O42Y/TC9rAU/pzvDIyUW6pLEOUMv0uUT7vqWFN8+ELGZrWQwSVL
8q6eBOhLuwq67ee4wFWc3EUh3BL1nTWfoUeJgWLJqgUIWsXK0UMhkTjuIJTRArxA
Htuy1Idq3WBJq0xL2apEfuaZTYlcbaKabieg62kseAwMsALEetBDljtUK7tkCWIS
9bB+QnZSJ1naxflAI/TtxVoLlyWRz3Mw5MxzDayjI7nYxA==
=IF8v
-----END PGP PUBLIC KEY BLOCK-----'''


def build_valid_message_payload_with_factory():
    host_addr = 'host_addr_string'
    key_dir = 'tests/data/keys'
    message = "Hello world"
    host_key_fingerprint = '989241C552F4FD50C3475DBB55A45A99FE45E540'
    passphrase = 'passphrase'
    factory = messagefactory.MessageFactory(host_addr, key_dir, gpg_pub_key_string, host_key_fingerprint, message, passphrase)
    result = factory.build()
    return result


class TestRootControllerNetRelated(RootSetupClass):
    key_dir = 'tests/data/keys'

    def test_message_controller_att_is_message_controller(self):
        self.assertIsInstance(self.x.message_controller, messagescontroller.MessagesController)
        self.assertEqual(self.x.message_controller.root, self.root)
        self.assertEqual(self.x.message_controller.view, self.x.view.left_panel.messages_frame)
        self.assertEqual(self.x.message_controller.root_queue, self.x.queue)
        self.assertEqual(self.x.message_controller.gpg_home_dir_observer, self.x.gpg_datacontext.home_dir_observer)

    def test_handle_queue_payload_calls_handle_server_error_with_server_error_payload(self):
        payload = dict(desc=constants.command_list.Server_Error, error='Error thing')
        target = self.x.handle_server_error = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_send_new_message_with_send_new_mesage_payload(self):
        payload = dict(desc=constants.command_list.Send_New_Message)
        target = self.x.handle_send_new_message = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_received_new_message_with_received_new_mesage_payload(self):
        payload = dict(desc=constants.command_list.Received_New_Message)
        target = self.x.handle_received_new_message = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_send_new_message_client_error_with_send_new_message_client_error_payload(self):
        payload = dict(desc=constants.command_list.Send_New_Message_Client_Err)
        target = self.x.handle_send_new_message_client_error = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_send_new_message_client_response_with_send_new_message_client_response_payload(self):
        payload = dict(desc=constants.command_list.Send_New_Message_Client_Res)
        target = self.x.handle_send_new_message_client_response = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_queue_payload_calls_handle_inspect_message_client_response_with_inspect_message_payload(self):
        payload = dict(desc=constants.command_list.Inspect_Message)
        target = self.x.handle_inspect_message = MagicMock()
        self.x.handle_queue_payload(payload)
        target.assert_called_with(payload)

    def test_handle_inspect_message_prints_argspace_msg_to_console(self):
        msg_space = types.SimpleNamespace(message_text='text string stuff')
        payload = dict(desc=constants.command_list.Inspect_Message,
                       payload=msg_space)
        target = self.x.console_controller.print_to_console = MagicMock()
        self.x.handle_inspect_message(payload)
        target.assert_called_with(msg_space.message_text)

    def test_handle_send_new_message_calls_command_client_run_with_args(self):
        payload = dict()
        payload_dict = dict(payload=payload)
        target = self.x.command_client = MagicMock()
        result = self.x.handle_send_new_message(payload)
        target.run.assert_called_with(constants.command_list.Send_New_Message, **payload_dict)

    # TODO: is this method deprecated???
    def build_and_return_valid_message_validator(self):
        msg_dict = build_valid_message_payload_with_factory()
        validator = messagevalidator.MessageValidator(msg_dict, self.key_dir, 'passphrase')
        result = validator.validate()
        return validator

    def test_handle_send_new_message_client_response_calls_command_client_with_args(self):
        payload = dict(nonce_valid=False)
        payload_dict = dict(payload=payload)
        target = self.x.command_client = MagicMock()
        result = self.x.handle_send_new_message_client_response(payload)
        target.run.assert_called_with(constants.command_list.Send_New_Message_Client_Res, **payload_dict)

    def test_handle_send_new_message_client_error_calls_alert_log(self):
        mock_payload = dict(error='error_msg')
        alert_targ = self.x.launch_alert_log = MagicMock()
        self.x.handle_send_new_message_client_error(mock_payload)
        self.assertTrue(alert_targ.called)


class TestRootControllerEventBindings(RootSetupClass):

    def test_config_event__bindings_attribute(self):
        name = 'config_event_bindings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch.object(rootcontroller.RootController, 'config_event_bindings')
    def test_constructor_calls_config_event_bindings(self, mocked_method):
        x = self.altsetup()
        self.assertTrue(mocked_method.called)


class TestRootControllerTorNetControllerRelated(RootSetupClass):

    def test_tornet_controller_attr_set(self):
        self.assertIsInstance(self.x.tornet_controller, tornetcontroller.TorNetController)
        self.assertEqual(self.x.tornet_controller.root, self.x.root)
        self.assertEqual(self.x.tornet_controller.view, self.x.view.left_panel.tor_net_frame)
        self.assertEqual(self.x.tornet_controller.root_queue, self.x.queue)
        self.assertEqual(self.x.tornet_controller.tor_datacontext, self.x.tor_datacontext)


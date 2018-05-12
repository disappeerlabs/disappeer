"""
test_popuplauncher.py

Test suite for the popuplauncher module and its functions

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from disappeer.popups import popuplauncher
from disappeer.popups.keyinfo.keyinfocontroller import KeyInfoController
from disappeer.popups.newkey.newkeycontroller import NewKeyController
from disappeer.popups.deletekey.deletekeycontroller import DeleteKeyController
from disappeer.popups.alertbox.alertboxcontroller import AlertBoxController
from disappeer.popups.getpassphrase.getpassphrasecontroller import GetPassphraseController
from disappeer.popups.getsessionpassphrase.getsessionpassphrasecontroller import GetSessionPassphraseController
from disappeer.popups.peerconnect.peerconnectcontroller import PeerConnectController
from disappeer.popups.contactrequest.contactrequestcontroller import ContactRequestController
from disappeer.popups.peercontact.peercontactcontroller import PeerContactController
from disappeer.popups.sendmessage.sendmessagecontroller import SendMessageController
from disappeer.popups.displaymessage.displaymessagecontroller import DisplayMessageController
from disappeer.popups.displaysentrequest.displaysentrequestcontroller import DisplaySentRequestController
from disappeer.popups.blinkalert.blinkalertcontroller import BlinkAlertController
from disappeer.popups.aboutbox.aboutboxcontroller import AboutBoxController


class TestImports(unittest.TestCase):

    def test_keyinfocontroller(self):
        self.assertEqual(KeyInfoController, popuplauncher.KeyInfoController)

    def test_newkeycontroller(self):
        self.assertEqual(NewKeyController, popuplauncher.NewKeyController)

    def test_deletekeycontroller(self):
        self.assertEqual(DeleteKeyController, popuplauncher.DeleteKeyController)

    def test_alertboxcontroller(self):
        self.assertEqual(AlertBoxController, popuplauncher.AlertBoxController)

    def test_getpassphrasecontroller(self):
        self.assertEqual(GetPassphraseController, popuplauncher.GetPassphraseController)

    def test_getpeercontroller(self):
        self.assertEqual(PeerConnectController, popuplauncher.PeerConnectController)

    def test_contactrequestcontroller(self):
        self.assertEqual(ContactRequestController, popuplauncher.ContactRequestController)

    def test_peercontactcontroller(self):
        self.assertEqual(PeerContactController, popuplauncher.PeerContactController)

    def test_sendmessagecontroller(self):
        self.assertEqual(SendMessageController, popuplauncher.SendMessageController)

    def test_DisplayMessageController(self):
        self.assertEqual(DisplayMessageController, popuplauncher.DisplayMessageController)

    def test_GetSessionPassphraseController(self):
        self.assertEqual(GetSessionPassphraseController, popuplauncher.GetSessionPassphraseController)

    def test_DisplaySentRequestController(self):
        self.assertEqual(DisplaySentRequestController, popuplauncher.DisplaySentRequestController)

    def test_BlinkAlertController(self):
        self.assertEqual(BlinkAlertController, popuplauncher.BlinkAlertController)

    def test_AboutBoxController(self):
        self.assertEqual(AboutBoxController, popuplauncher.AboutBoxController)


class TestLaunchKeyInfo(unittest.TestCase):

    def test_launch_key_info_attribute(self):
        name = 'launch_key_info_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'KeyInfoController')
    def test_launch_key_info_takes_two_args(self, mocked):
        one = MagicMock()
        two = MagicMock()
        result = popuplauncher.launch_key_info_popup(one, two)
        mocked.assert_called_with(one, two)

    @patch.object(popuplauncher, 'KeyInfoController')
    def test_launch_key_info_calls_show_test(self, mocked):
        one = MagicMock()
        two = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_key_info_popup(one, two)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestLaunchNewKey(unittest.TestCase):

    def test_launch_new_key_attribute(self):
        name = 'launch_new_key_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'NewKeyController')
    def test_launch_new_key_takes_arg(self, mocked):
        one = MagicMock()
        result = popuplauncher.launch_new_key_popup(one)
        mocked.assert_called_with(one)

    @patch.object(popuplauncher, 'NewKeyController')
    def test_launch_new_key_calls_show(self, mocked):
        one = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_new_key_popup(one)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestDeleteKey(unittest.TestCase):

    def test_launch_delete_key_attribute(self):
        name = 'launch_delete_key_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'DeleteKeyController')
    def test_launch_delete_key_takes_two_args(self, mocked):
        one = MagicMock()
        two = MagicMock()
        result = popuplauncher.launch_delete_key_popup(one, two)
        mocked.assert_called_with(one, two)

    @patch.object(popuplauncher, 'DeleteKeyController')
    def test_launch_delete_key_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_delete_key_popup(one, two)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestAlertBox(unittest.TestCase):
    def test_launch_alert_box_attribute(self):
        name = 'launch_alert_box_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'AlertBoxController')
    def test_launch_alert_box_takes_two_args(self, mocked):
        one = MagicMock()
        two = MagicMock()
        result = popuplauncher.launch_alert_box_popup(one, two)
        mocked.assert_called_with(one, two)

    @patch.object(popuplauncher, 'AlertBoxController')
    def test_launch_alert_box_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_alert_box_popup(one, two)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestGetPassphrase(unittest.TestCase):
    def test_launch_getpassphrase_attribute(self):
        name = 'launch_get_passphrase_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'GetPassphraseController')
    def test_launch_get_passphrase_takes_arg(self, mocked):
        one = MagicMock()
        result = popuplauncher.launch_get_passphrase_popup(one)
        mocked.assert_called_with(one)

    @patch.object(popuplauncher, 'GetPassphraseController')
    def test_launch_get_passphrase_calls_show(self, mocked):
        one = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_get_passphrase_popup(one)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestGetSessionPassphrase(unittest.TestCase):
    def test_launch_getsessionpassphrase_attribute(self):
        name = 'launch_get_session_passphrase_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'GetSessionPassphraseController')
    def test_launch_get_session_passphrase_takes_arg(self, mocked):
        one = MagicMock()
        result = popuplauncher.launch_get_session_passphrase_popup(one)
        mocked.assert_called_with(one)

    @patch.object(popuplauncher, 'GetSessionPassphraseController')
    def test_launch_get_session_passphrase_calls_show(self, mocked):
        one = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_get_session_passphrase_popup(one)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)



class TestPeerConnect(unittest.TestCase):
    def test_launch_peerconnect_attribute(self):
        name = 'launch_peerconnect_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'PeerConnectController')
    def test_launch_peer_connect_takes_arg(self, mocked):
        one = MagicMock()
        result = popuplauncher.launch_peerconnect_popup(one)
        mocked.assert_called_with(one)

    @patch.object(popuplauncher, 'PeerConnectController')
    def test_launch_peer_connect_calls_show(self, mocked):
        one = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_peerconnect_popup(one)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestContactRequest(unittest.TestCase):
    def test_launch_contactrequest_attribute(self):
        name = 'launch_contactrequest_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'ContactRequestController')
    def test_launch_contactrequest_takes_arg(self, mocked):
        one = MagicMock()
        two = MagicMock()
        result = popuplauncher.launch_contactrequest_popup(one, two)
        mocked.assert_called_with(one, two)

    @patch.object(popuplauncher, 'ContactRequestController')
    def test_launch_contactrequest_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_contactrequest_popup(one, two)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestPeerContact(unittest.TestCase):
    def test_launch_peercontact_attribute(self):
        name = 'launch_peercontact_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'PeerContactController')
    def test_launch_peercontact_takes_arg(self, mocked):
        one = MagicMock()
        two = MagicMock()
        result = popuplauncher.launch_peercontact_popup(one, two)
        mocked.assert_called_with(one, two)

    @patch.object(popuplauncher, 'PeerContactController')
    def test_launch_peercontact_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_peercontact_popup(one, two)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestSendMessage(unittest.TestCase):
    def test_launch_sendmessage_attribute(self):
        name = 'launch_sendmessage_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'SendMessageController')
    def test_launch_sendmessage_takes_arg(self, mocked):
        one = MagicMock()
        two = MagicMock()
        three = MagicMock()
        result = popuplauncher.launch_sendmessage_popup(one, two, three)
        mocked.assert_called_with(one, two, three)

    @patch.object(popuplauncher, 'SendMessageController')
    def test_launch_sendmessage_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        three = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_sendmessage_popup(one, two, three)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestDisplayMessage(unittest.TestCase):

    def test_launch_display_message_attribute(self):
        name = 'launch_displaymessage_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'DisplayMessageController')
    def test_launch_displaymessage_takes_arg(self, mocked):
        one = MagicMock()
        two = MagicMock()
        result = popuplauncher.launch_displaymessage_popup(one, two)
        mocked.assert_called_with(one, two)

    @patch.object(popuplauncher, 'DisplayMessageController')
    def test_launch_displaymessage_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_displaymessage_popup(one, two)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestDisplaySentRequest(unittest.TestCase):
    def test_launch_display_sent_request_attribute(self):
        name = 'launch_display_sent_request_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'DisplaySentRequestController')
    def test_launch_display_sent_request_takes_args(self, mocked):
        one = MagicMock()
        two = MagicMock()
        three = MagicMock()
        result = popuplauncher.launch_display_sent_request_popup(one, two, three)
        mocked.assert_called_with(one, two, three)

    @patch.object(popuplauncher, 'DisplaySentRequestController')
    def test_launch_peercontact_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        three = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_display_sent_request_popup(one, two, three)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestBlinkAlert(unittest.TestCase):

    def test_launch_blink_alert_attribute(self):
        name = 'launch_blink_alert_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'BlinkAlertController')
    def test_launch_alert_box_takes_two_args(self, mocked):
        one = MagicMock()
        two = MagicMock()
        result = popuplauncher.launch_blink_alert_popup(one, two)
        mocked.assert_called_with(one, two)

    @patch.object(popuplauncher, 'BlinkAlertController')
    def test_launch_alert_box_calls_show(self, mocked):
        one = MagicMock()
        two = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_blink_alert_popup(one, two)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)


class TestAboutBox(unittest.TestCase):
    def test_launch_about_box_attribute(self):
        name = 'launch_about_box_popup'
        check = hasattr(popuplauncher, name)
        self.assertTrue(check)

    @patch.object(popuplauncher, 'AboutBoxController')
    def test_launch_about_box_takes_two_args(self, mocked):
        one = MagicMock()
        result = popuplauncher.launch_about_box_popup(one)
        mocked.assert_called_with(one)

    @patch.object(popuplauncher, 'AboutBoxController')
    def test_launch_about_box_calls_show(self, mocked):
        one = MagicMock()
        val = MagicMock()
        val.return_value = 'xxx'
        mocked.return_value = val
        result = popuplauncher.launch_about_box_popup(one)
        mocked.return_value.show.assert_called_with()
        self.assertEqual(result, mocked.return_value.show.return_value)




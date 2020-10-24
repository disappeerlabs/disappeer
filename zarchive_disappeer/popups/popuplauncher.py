"""
popuplauncher.py

Module with functions to launch popup windows

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from disappeer.popups.keyinfo.keyinfocontroller import KeyInfoController
from disappeer.popups.newkey.newkeycontroller import NewKeyController
from disappeer.popups.deletekey.deletekeycontroller import DeleteKeyController
from disappeer.popups.alertbox.alertboxcontroller import AlertBoxController
from disappeer.popups.getpassphrase.getpassphrasecontroller import GetPassphraseController
from disappeer.popups.peerconnect.peerconnectcontroller import PeerConnectController
from disappeer.popups.contactrequest.contactrequestcontroller import ContactRequestController
from disappeer.popups.peercontact.peercontactcontroller import PeerContactController
from disappeer.popups.sendmessage.sendmessagecontroller import SendMessageController
from disappeer.popups.displaymessage.displaymessagecontroller import DisplayMessageController
from disappeer.popups.getsessionpassphrase.getsessionpassphrasecontroller import GetSessionPassphraseController
from disappeer.popups.displaysentrequest.displaysentrequestcontroller import DisplaySentRequestController
from disappeer.popups.blinkalert.blinkalertcontroller import BlinkAlertController
from disappeer.popups.aboutbox.aboutboxcontroller import AboutBoxController


def launch_key_info_popup(root, key_dict):
    window = KeyInfoController(root, key_dict)
    result = window.show()
    return result


def launch_new_key_popup(root):
    window = NewKeyController(root)
    result = window.show()
    return result


def launch_delete_key_popup(root, key_list):
    window = DeleteKeyController(root, key_list)
    result = window.show()
    return result


def launch_alert_box_popup(root, message):
    window = AlertBoxController(root, message)
    result = window.show()
    return result


def launch_get_passphrase_popup(root):
    window = GetPassphraseController(root)
    result = window.show()
    return result


def launch_get_session_passphrase_popup(root):
    window = GetSessionPassphraseController(root)
    result = window.show()
    return result


def launch_peerconnect_popup(root):
    window = PeerConnectController(root)
    result = window.show()
    return result


def launch_contactrequest_popup(root, request_record):
    window = ContactRequestController(root, request_record)
    result = window.show()
    return result


def launch_peercontact_popup(root, data_record):
    window = PeerContactController(root, data_record)
    result = window.show()
    return result


def launch_sendmessage_popup(root, recipient_data_record, console_text):
    window = SendMessageController(root, recipient_data_record, console_text)
    result = window.show()
    return result


def launch_displaymessage_popup(root, argnamespace):
    window = DisplayMessageController(root, argnamespace)
    result = window.show()
    return result


def launch_display_sent_request_popup(root, gpg_pub_key, address):
    window = DisplaySentRequestController(root, gpg_pub_key, address)
    result = window.show()
    return result


def launch_blink_alert_popup(root, message):
    window = BlinkAlertController(root, message)
    result = window.show()
    return result


def launch_about_box_popup(root):
    window = AboutBoxController(root)
    result = window.show()
    return result

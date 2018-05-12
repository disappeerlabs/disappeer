"""
abstractclient.py

Module for the AbstractClient base class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import abc
import socket
import socks


class AbstractClient(metaclass=abc.ABCMeta):

    def __init__(self, argnamespace):
        self.argnamespace = argnamespace
        self.sock = None
        self.protocol = None
        self.error = None

    @property
    def host(self):
        return self.argnamespace.host

    @property
    def port(self):
        return self.argnamespace.port

    @property
    def interface(self):
        return self.host, self.port

    @property
    def payload_dict(self):
        return self.argnamespace.payload_dict

    @property
    def nonce(self):
        return self.argnamespace.nonce

    @property
    def command(self):
        return self.argnamespace.command

    @property
    def queue(self):
        return self.argnamespace.queue

    def create_socket(self):
        # Original socket object
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.settimeout(10)
        # return self.sock

        # # Second version, with bytes string
        # self.sock = socks.socksocket()
        # self.sock.set_proxy(socks.PROXY_TYPE_SOCKS5, b'127.0.0.1', 9050, True)
        # return self.sock

        self.sock = socks.socksocket()
        self.sock.set_proxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050, True)
        return self.sock

    def connect(self):
        self.sock.connect(self.interface)

    @abc.abstractmethod
    def wrap_socket(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_protocol(self):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self):
        raise NotImplementedError

    @abc.abstractmethod
    def handle_response(self):
        raise NotImplementedError

    def stop(self):
        self.sock.close()

    def configure_transport(self):
        try:
            self.create_socket()
            self.connect()
            self.wrap_socket()
        except (socket.error, ConnectionRefusedError) as err:
            self.error = err
            return err
        self.set_protocol()

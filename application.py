# -*- coding: utf-8 -*-
import json
import socket
import threading
import messages
import model
import view
import client


BUFFER_SIZE = 2 ** 10


class Application(object):

    instance = None

    def __init__(self, args):
        self.args = args
        self.closing = False
        self.host = None
        self.port = None
        self.receive_worker = None
        self.username = None
        self.ui = view.EzChatUI(self)
        self.client = client.Client()
        self.last_reciever = None
        self.last_message = None
        Application.instance = self

    def execute(self):
        if not self.ui.show():
            return
        self.client.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.sock.connect((self.host, self.port))
        except (socket.error, OverflowError):
            self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)
            return
        self.receive_worker = threading.Thread(target=self.receive)
        self.receive_worker.start()
        self.send()
        self.ui.loop()

    def receive(self):
        while True:
            try:
                message = model.Message(**json.loads(self.receive_all()))
            except (ConnectionAbortedError, ConnectionResetError):
                if not self.closing:
                    self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)
                return

            if message.message.find("Now {} lead".format(self.username)) == 0:
                self.ui.show_send_button()
                self.ui.show_message(message)
            else:
                if message.message.isdigit():
                    if not self.last_reciever == self.username:
                        self.ui.show_send_button()
                    if self.last_message.isdigit():
                        self.ui.show_timer(message)
                else:
                    self.ui.disable_send_button()
                    self.ui.show_message(message)

            if not message.username == messages.SERVER:
                self.last_reciever = message.username
            self.last_message = message.message

    def receive_all(self):
        buffer = ""
        while not buffer.endswith(model.END_CHARACTER):
            buffer += self.client.sock.recv(BUFFER_SIZE).decode(model.TARGET_ENCODING)
        return buffer[:-1]

    def send(self, event=None):
        message = self.ui.message.get()
        if len(message) == 0:
            return
#        self.ui.message.set("")
        message = model.Message(username=self.username, message=message, quit=False)
        try:
            self.client.sock.sendall(message.marshal())
        except (ConnectionAbortedError, ConnectionResetError):
            if not self.closing:
                self.ui.alert(messages.ERROR, messages.CONNECTION_ERROR)

    def exit(self):
        self.closing = True
        try:
            self.client.sock.sendall(model.Message(username=self.username, message="", quit=True).marshal())
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            print(messages.CONNECTION_ERROR)
        finally:
            self.client.sock.close()
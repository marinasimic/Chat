import socket
import threading
from backend import config, utils


class Client(object):
    def __init__(self) -> None:
        self.server_address = ""
        self.username = ""
        self.client_socket = None
        self.chatting = False

        self.messages = []
        self.message_thread = threading.Thread(target=self.receive_messages)
        self.message_mutex = threading.Lock()

    def start_receiving_messages(self):
        self.chatting = True
        self.message_thread.start()

    def stop_receiving_messages(self):
        self.chatting = False
        self.message_thread.join(1)

    def receive_messages(self):
        while self.chatting:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')

                # if utils.SEND_ACTIVE_USERS in message:
                #     continue

                with self.message_mutex:
                    self.messages.append(message)
            except:
                continue

    def get_messages(self):
        messages = []
        with self.message_mutex:
            messages = self.messages[:]
            self.messages.clear()

        return messages
    
    def get_active_users(self):
        self.client_socket.send(utils.SEND_ACTIVE_USERS.encode('utf-8'))

        try:
            message = self.client_socket.recv(1024).decode('utf-8')
            return message
        except:
            return ""

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

    def enter_username(self, username):
        self.client_socket.send(username.encode('utf-8'))

        try:
            message = self.client_socket.recv(1024).decode('utf-8')
        except:
            return (False, "Couldn't connect to the server!")

        if message == utils.INVALID_USERNAME:
            return (False, "Username already in use!")
        
        self.username = username
        self.start_receiving_messages()
        return (True, "You have entered the chat as " + username)

    def connect_to_server(self, server_address):
        if not utils.validate_server_address(server_address):
            return (False, "Invalid server address!")

        try:
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5)
            self.client_socket.connect((server_address, config.PORT))
        except TimeoutError:
            return (False, "Timeout has been reached!")
        except:
            return (False, "Connection has been refused!")

        self.server_address = server_address

        return (True, "Connection has been established!")

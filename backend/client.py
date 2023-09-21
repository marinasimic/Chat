import socket
import config
import utils


class Client(object):
    def __init__(self) -> None:
        self.server_address = ""
        self.username = ""
        self.client_socket = None

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                print(message)
            except:
                break

    def send_messages(self):
        while True:
            message = input()
            if message.lower() == 'exit':
                break
            self.client_socket.send(message.encode('utf-8'))

    def enter_username(self, username):
        self.client_socket.send(username.encode('utf-8'))

        try:
            message = self.client_socket.recv(1024).decode('utf-8')
        except:
            return (False, "Couldn't connect to the server!")

        if message == utils.INVALID_USERNAME:
            return (False, "Username already in use!")
        elif message == utils.USERNAME_VALID:
            self.username = username
            return (True, "You have entered the chat as " + username)

        return (False, "Couldn't connect to the server!")

    def connect_to_server(self, server_address):
        if not utils.validate_server_address(server_address):
            return (False, "Invalid server address!")

        try:
            self.client_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(3)
            self.client_socket.connect((server_address, config.PORT))
        except TimeoutError:
            return (False, "Timeout has been reached!")
        except:
            return (False, "Connection has been refused!")

        self.server_address = server_address

        return (True, "Connection has been established!")

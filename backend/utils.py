import socket
import cryptocode

INVALID_USERNAME = "Invalid username"
USERNAME_VALID = "Valid username"

ENCRYPTION_STRING = 'MessageEncryptionString'

def validate_server_address(server_address):
    try:
        socket.inet_aton(server_address)
    except socket.error:
        return False

    return True

def send_message(client_socket, message):
    message = cryptocode.encrypt(message, ENCRYPTION_STRING)

    client_socket.send(message.encode('utf-8'))

def receive_message(client_socket):
    message = client_socket.recv(1024).decode('utf-8')

    return cryptocode.decrypt(message, ENCRYPTION_STRING)
import socket

INVALID_USERNAME = "Invalid username"
USERNAME_VALID = "Valid username"


def validate_server_address(server_address):
    try:
        socket.inet_aton(server_address)
    except socket.error:
        return False

    return True

import socket

INVALID_USERNAME = "Invalid username"
USERNAME_VALID = "Valid username"

SEND_ACTIVE_USERS = "Send active users"


def validate_server_address(server_address):
    try:
        socket.inet_aton(server_address)
    except socket.error:
        return False

    return True

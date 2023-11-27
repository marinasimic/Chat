import socket
import threading
import config
import utils
import time

clients = {}


def broadcast_message(message, client_socket=None):
    for client in clients.values():
        if client != client_socket:
            utils.send_message(client, message)


def request_username(client_socket):
    try:
        # Check if the username exist
        # Request the new one if username is already in use
        while True:
            username = utils.receive_message(client_socket)

            if username not in clients.keys():
                utils.send_message(client_socket, utils.USERNAME_VALID)
                return username

            utils.send_message(client_socket, utils.INVALID_USERNAME)
    except:
        raise Exception("User has left the chat.")


def send_active_users():
    while True:
        active_users = ""
        for client in clients.keys():
            if active_users != "":
                active_users += "<br>"
            active_users += client

        message = '{"type": "active_users", "users":"' + active_users + '"}'

        broadcast_message(message)

        time.sleep(2)


def handle_client(client_socket):
    try:
        username = request_username(client_socket)
        clients[username] = client_socket
        broadcast_message(
            '{"type": "user_status", "status": "User '
            + username
            + ' has joined the chat."}',
            client_socket,
        )
    except:
        return

    while True:
        try:
            input_message = utils.receive_message(client_socket)
            if not input_message:
                break

            message = (
                '{"type": "message", "user":"'
                + username
                + '", "text":"'
                + input_message
                + '"}'
            )

            broadcast_message(message)
        except:
            break

    broadcast_message(
        '{"type": "user_status", "status": "User ' + username + ' has left the chat."}',
        client_socket,
    )

    # Remove the client from the dictionary
    del clients[username]
    client_socket.close()


def wait_for_connection():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", config.PORT))
    server_socket.listen(5)
    print(f"Server listening on port {config.PORT}...")

    active_users_handler = threading.Thread(target=send_active_users)
    active_users_handler.start()

    client_connection_handler = threading.Thread(target=wait_for_connection)
    client_connection_handler.start()

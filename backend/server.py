import socket
import threading
import config
import utils

clients = {}


def broadcast_message(message, client_socket=None):
    for client in clients.values():
        if client != client_socket:
            client.send(message.encode('utf-8'))


def request_username(client_socket):
    try:
        # Check if the username exist
        # Request the new one if username is already in use
        while True:
            username = client_socket.recv(1024).decode('utf-8')

            if username not in clients.keys():
                client_socket.send(utils.USERNAME_VALID
                                   .format(username)
                                   .encode('utf-8'))
                return username

            client_socket.send(utils.INVALID_USERNAME
                               .format(username)
                               .encode('utf-8'))
    except:
        raise Exception("User has left the chat.")


def handle_client(client_socket):
    try:
        username = request_username(client_socket)
        clients[username] = client_socket
        broadcast_message("<span style=\"color:red;\">User {} has joined the chat.<span>".format(
            username), client_socket)
    except:
        return

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                broadcast_message("<span style=\"color:red;\">User {} has left the chat.<span>".format(
                    username), client_socket)
                break

            # if message == utils.SEND_ACTIVE_USERS:
            #     active_users = ""
            #     for client in clients.keys():
            #         active_users += client
            #         active_users += ","
            #         client_socket.send(active_users.format(username)
            #                            .encode('utf-8'))
            #         continue

            message = "<b>" + username + ":</b> " + message

            broadcast_message(message)
        except:
            broadcast_message("<span style=\"color:red;\">User {} has left the chat.<span>".format(
                username), client_socket)
            break

    # Remove the client from the dictionary
    del clients[username]
    client_socket.close()


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", config.PORT))
    server_socket.listen(5)
    print(f"Server listening on port {config.PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,))
        client_handler.start()

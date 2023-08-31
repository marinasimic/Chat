import socket
import threading
import config

def validate_server_address(server_address):
    try:
        socket.inet_aton(server_address)
    except socket.error:
        return False

    return True

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

def send_messages(client_socket):
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

if __name__ == '__main__':
    server_address = "127.0.0.1"#input("Enter the server address: ")

    if not validate_server_address(server_address):
        print("Server address not valid!")
        exit()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, config.PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_messages(client_socket)

    client_socket.close()

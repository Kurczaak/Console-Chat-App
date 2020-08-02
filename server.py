import socket
import select


IP = "127.0.0.1"
PORT = 1234
HEADER_SIZE = 10


def send_message(socket, message, header_size):
    header = f'{len(message):<{header_size}}'
    full_message = header + message
    socket.send(full_message.encode("UTF-8"))


def receive_message(socket, header_size):
    try:
        header = socket.recv(header_size).decode("UTF-8")  # receive just the header of a new message
        msg_len = int(header)
        if not msg_len:  # if the header is empty return False
            return False
        else:  # receive a new message of the length specified in header
            return socket.recv(msg_len).decode("UTF-8")
    # if the connection has been close abruptly return False
    except:
        return False

# create a new server socket
# AF_INET - IPv4 protocol, SOCK_STREAM - TCP connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to given IP and port
server_socket.bind((IP, PORT))

# start listening to incoming connections
server_socket.listen()

sockets_list = [server_socket]  # list of all sockets to check if notified
clients = {}  # list of all the currently connected clients

# infinite loop waiting for incoming connections and messages
while True:
    # select.select is a blocking call, supervising sockets given in a list if any is notified
    read_sockets, _, error_sockets = select.select(sockets_list, [], sockets_list)

    # if data is to be received (new connections or messages)
    # iterate through sockets containing new data and handle it appropriately
    for notified_socket in read_sockets:

        # server socket is notified - receive a new connection
        if notified_socket == server_socket:

            client_socket, address = server_socket.accept()
            # the very first message is the username
            username = receive_message(client_socket, HEADER_SIZE)
            if username is False:
                continue

            # add new socket to the list and a new user to the dictionary
            sockets_list.append(client_socket)
            clients[client_socket] = username

            print(f"New connection from {address}")
            send_message(client_socket, f"Welcome to the server {username}!", HEADER_SIZE)

        # notified socket is a client socket - new message to receive and propagate
        else:
            msg = receive_message(notified_socket, HEADER_SIZE)
            if msg is False:
                if notified_socket in clients:
                    print(f"Closed connection from {clients[notified_socket]}")
                    sockets_list.remove(client_socket)
                    del clients[notified_socket]
                continue
            print(f"{clients[notified_socket]}: {msg}")

            # send the message to all the sockets but not to the sender
            for client in clients:
                if client != notified_socket :
                    send_message(client, msg, HEADER_SIZE)

        for socket in error_sockets:
            sockets_list.remove(socket)
            del clients[socket]

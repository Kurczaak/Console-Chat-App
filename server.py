import socket
import select


def send_welcome_message(socket, message, header_size):
    header = f'{len(message):<{header_size}}'
    full_message = header + message
    socket.send(full_message.encode("UTF-8"))


def receive_message(socket, header_size):
    try:
        msg_len = int(socket.recv(HEADER_SIZE))
        msg = client_socket.recv(msg_len)
        if len(msg) == msg_len:
            return msg
    except:
        return False


IP = "127.0.0.1"
PORT = 1234
HEADER_SIZE = 10
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

sockets = [server_socket]
clients = []

while True:
    read_sockets, _, error_sockets = select.select(sockets, [], sockets)
    for notified_socket in read_sockets:
        # send a new message
        if notified_socket == server_socket:
            client_socket, address = server_socket.accept()
            sockets.append(client_socket)
            print(f"New connection from {address}")
            send_welcome_message(client_socket, "Welcome to the server", HEADER_SIZE)
        else:
            msg = receive_message(client_socket, HEADER_SIZE)
            if msg is False:
                print("Closed connection")
                sockets.remove(client_socket)
                continue
            print(msg.decode("UTF-8"))
            print(len(read_sockets))
        for notified_socket in error_sockets:
            sockets.remove(notified_socket)

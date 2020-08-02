import socket
import select


def send_welcome_message(socket, message, header_size):
    header = f'{len(message):<{header_size}}'
    full_message = header + message
    socket.send(full_message.encode("UTF-8"))


def receive_message(socket, header_size):
    try:

        # Receive our "header" containing message length, it's size is defined and constant
        message_header = socket.recv(header_size)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return socket.recv(1024)

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
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

sockets_list = [server_socket]
clients = []

while True:
    read_sockets, _, error_sockets = select.select(sockets_list, [], sockets_list, 0.1)

    for notified_socket in read_sockets:
        # send a new message
        if notified_socket == server_socket:
            client_socket, address = server_socket.accept()
            sockets_list.append(client_socket)
            print(f"New connection from {address}")
            #send_welcome_message(client_socket, "Welcome to the server", HEADER_SIZE)
        else:
            msg = receive_message(notified_socket, HEADER_SIZE)
            if msg is False:
                print("Closed connection")
                sockets_list.remove(client_socket)
                continue
            print(msg.decode("UTF-8"))
        for notified_socket in error_sockets:
            sockets_list.remove(notified_socket)

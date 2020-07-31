import socket
import errno
import sys

IP = "127.0.0.1"
PORT = 1234
HEADER_SIZE = 10
PACKET_SIZE = 2
# create a new server socket
# AF_INET - IPv4 protocol, SOCK_STREAM - TCP connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server socket
client_socket.connect((IP, PORT))
# set the socket to be non-blocking
client_socket.setblocking(False)

while True:
    try:
        message_len = int(client_socket.recv(HEADER_SIZE).decode("UTF-8"))
        if not message_len:
            continue
        full_message = ''
        while len(full_message) != message_len:
            message = client_socket.recv(PACKET_SIZE).decode("UTF-8")
            full_message += message
        print(full_message)
    except BlockingIOError as e:
        continue



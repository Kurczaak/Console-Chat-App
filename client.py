import socket
import errno
import sys


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
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server socket
client_socket.connect((IP, PORT))
# set the socket to be non-blocking
client_socket.setblocking(False)

# initial message - enter your username
username = input("Enter your username: ")
send_message(client_socket, username, HEADER_SIZE)

recv_msg = False
while recv_msg is False:
    recv_msg = receive_message(client_socket, HEADER_SIZE)

print(recv_msg)

while True:
    try:
        my_message = input(">")
        send_message(client_socket, my_message, HEADER_SIZE)
        received_message = receive_message(client_socket, HEADER_SIZE)
        if received_message:
            print(received_message)
        else:
            continue
    except IOError as e:
        continue


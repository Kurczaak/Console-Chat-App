import socket


IP = "127.0.0.1"
PORT = 1234
HEADER_SIZE = 10
# create a new server socket
# AF_INET - IPv4 protocol, SOCK_STREAM - TCP connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to given IP and port
server_socket.bind((IP, PORT))

# start listening to incoming connections
server_socket.listen()
while True:
    client_socket, address = server_socket.accept()
    print(f"New connection from {address}")
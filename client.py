import sys
import socket
import select
import errno

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8000

class Client:
    def __init__(self, client_socket, username):
        self.client_socket = client_socket
        self.username = my_username.encode('utf-8')
        self.username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(self.username_header + self.username)
    
    def send_message(self, message):
        if not message:
            return
        message = message.encode('utf-8')
        message = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8') + message
        self.client_socket.send(message)
    
    def recieve_message(self):
        username_header = self.client_socket.recv(HEADER_LENGTH)
        if not len(username_header):
            print("Connection closed by the server")
            sys.exit()

        username_length = int(username_header.decode('utf-8'))
        username = self.client_socket.recv(username_length).decode('utf-8')

        message_header = self.client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8'))
        message = self.client_socket.recv(message_length).decode('utf-8')

        print(f"{username} > {message}")

my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False) # recv() won't be blocked

client = Client(client_socket, my_username)

while True:
    client.send_message(input(f"{my_username} > "))
    try:
        while True:
            client.recieve_message()
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error ", str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General Error ", str(e))
        sys.exit()

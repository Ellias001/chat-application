import socket
import select
import errno
import sys

class Client:
    def __init__(self, IP = '127.0.0.1', PORT = 8000, HEADER_LENGTH = 10):
        try:
            self._create_socket(IP, PORT)
        except:
            print("Client socket creation failed")
            sys.exit()

        self.HEADER_LENGTH = HEADER_LENGTH
        self.username = input("Username: ").encode('utf-8')
        self.username_header = f"{len(self.username):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(self.username_header + self.username)
    
    def _create_socket(self, IP, PORT):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.client_socket.setblocking(False) # recv() won't be blocked

    def send_message(self, message):
        if message == '':
            return
        message = message.encode('utf-8')
        message = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8') + message
        self.client_socket.send(message)
    
    def recieve_message(self):
        username_header = self.client_socket.recv(self.HEADER_LENGTH)
        if not len(username_header):
            print("Connection closed by the server")
            sys.exit()

        username_length = int(username_header.decode('utf-8'))
        username = self.client_socket.recv(username_length).decode('utf-8')

        message_header = self.client_socket.recv(self.HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8'))
        message = self.client_socket.recv(message_length).decode('utf-8')

        print(f"{username} > {message}")


def main():
    client = Client()

    while True:
        client.send_message(input(f"{client.username.decode('utf-8')} > "))
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

if __name__ == '__main__':
    main()

import socket
import select
import sys

class Server:
    def __init__(self, IP = '127.0.0.1', PORT = 8000, HEADER_LENGTH = 10):
        try:
            self._create_socket(IP, PORT)
        except:
            print("Server socket creation failed")
            sys.exit()

        self.HEADER_LENGTH = HEADER_LENGTH
        self.sockets_list = [self.server_socket]
        self.clients = {} # cliet socket is key and user data (username) will be the value

    def _create_socket(self, IP, PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen(5)

    def accept_connection(self):
        client_socket, client_address = self.server_socket.accept()
        user = self._recieve_data(client_socket)

        if user is False:
            return

        self.sockets_list.append(client_socket)
        self.clients[client_socket] = user
        print(f"Accepted new connection from {client_address}")

    def _recieve_data(self, client_socket):
        try:
            header = client_socket.recv(self.HEADER_LENGTH)
            if not len(header):
                return False

            message_length = int(header.decode("utf-8"))
            return {"header": header, "data": client_socket.recv(message_length)}
        except:
            return False

    def recieve_send_message(self, client_socket):
        try:
            message = self._recieve_data(client_socket)
            if message is False:
                return

            user = self.clients[client_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            self.send_message(client_socket, user, message)
        except:
            return

    def send_message(self, notified_socket, user, message):
        for client_socket in self.clients:
            if client_socket is not notified_socket:
                print(f'Sending message from {user["data"].decode("utf-8")} to {self.clients[client_socket]["data"].decode("utf-8")}')
                client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    def delete_exception_sockets(self, exception_sockets):
        for notified_socket in exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.cliets[notified_socket]

    def close_connection(self, client_socket):
        print(f"Connection from {self.clients[notified_socket]} is closed")
        self.sockets_list.remove(client_socket)
        del self.clients[client_socket]


def main():
    server = Server()

    while True:
        # readable, writable, exceptional = select.select(inputs, outputs, inputs)
        read_sockets, _, exception_sockets = select.select(server.sockets_list, [], server.sockets_list)
    
        for notified_socket in read_sockets:
            if notified_socket is server.server_socket:
                server.accept_connection()
            else:
                server.recieve_send_message(notified_socket)
    
        server.delete_exception_sockets(exception_sockets)

if __name__ == '__main__':
    main()

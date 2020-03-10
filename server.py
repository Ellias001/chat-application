import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8000

class Server:
    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.sockets_list = [server_socket]
        self.clients = {} # cliet socket is key and user data (username) will be the value

    def accept_connection(self):
        client_socket, client_address = self.server_socket.accept()
        user = self.recieve_data(client_socket)
        if user is False:
            return
        else:
            self.sockets_list.append(client_socket)
            self.clients[client_socket] = user
            print(f"Accepted new connection from {client_address}")

    def recieve_data(self, client_socket):
        try:
            header = client_socket.recv(HEADER_LENGTH)
            if not len(header):
                return False

            message_length = int(header.decode("utf-8"))
            return {"header": header, "data": client_socket.recv(message_length)}
        except:
            return False

    def recieve_send_message(self, client_socket):
        try:
            message = self.recieve_data(client_socket)
            if message is False:
                return

            user = self.clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            self.send_message(notified_socket, user, message)
        except:
            return

    def send_message(self, notified_socket, user, message):
        for client_socket in self.clients:
            if client_socket is not notified_socket:
                client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    def delete_exception_sockets(self, exception_sockets):
        for notified_socket in exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.cliets[notified_socket]

    def close_connection(self, client_socket):
        print(f"Connection from {self.clients[notified_socket]} is closed")
        self.sockets_list.remove(client_socket)
        del self.clients[client_socket]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

server_socket.listen(5)

server = Server(server_socket)

while True:
    # readable, writable, exceptional = select.select(inputs, outputs, inputs)
    read_sockets, _, exception_sockets = select.select(server.sockets_list, [], server.sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket is server_socket:
            server.accept_connection()
        else:
            server.recieve_send_message(notified_socket)
    
    server.delete_exception_sockets(exception_sockets)

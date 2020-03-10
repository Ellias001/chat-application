import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8000

def recieve_message(client_socket, sockets_list, clients):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            close_connection(client_socket, sockets_list, clients)

        message_length = int(message_header.decode("utf-8"))
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        close_connection(client_socket, sockets_list, clients)

def close_connection(client_socket, sockets_list, clients):
    print(f"Connection from {clients[notified_socket]} is closed")
    sockets_list.remove(notified_socket)
    del clients[client_socket]

def accept_connection(sockets_list, clients):
    client_socket, client_address = server_socket.accept()
    user = recieve_message(client_socket)
    if user is False:
        return
    else:
        sockets_list.append(client_socket)
        clients[client_socket] = user
        print(f"Accepted new connection from {client_address}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))

server_socket.listen(5)

sockets_list = [server_socket]
clients = {} # cliet socket is key and user data (username) will be the value

while True:
    # readable, writable, exceptional = select.select(inputs, outputs, inputs)
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket is server_socket:
            accept_connection(sockets_list, client)
        else:
            message = recieve_message(notified_socket)
            user = clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            # sends recieved message to all clients connected to server
            for client_socket in clients:
                if client_socket is not notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del cliets[notified_socket]
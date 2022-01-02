import threading
import socket

host = 'localhost'
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients_addr = []
username = []


def broadcast(message):
    for client in clients_addr:
        client.send(message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients_addr.index(client)
            clients_addr.remove(client)
            client.close()
            name = username[index]
            broadcast(f'{name} has left the chat room!'.encode('utf-8'))
            username.remove(name)
            break


def Main():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('username?'.encode('utf-8'))
        name = client.recv(1024)
        username.append(name)
        clients_addr.append(client)
        print(f'{name} is connected now!'.encode('utf-8'))
        broadcast(f'{name} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    Main()

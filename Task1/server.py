import threading
import socket

host = 'localhost'
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients_addr = []
username = []


def broadcast(message,name):
    for client in clients_addr:
        index = clients_addr.index(client)
        if username[index]==name:
            client.send(f"You: {message}".encode('utf-8'))
        else:
            client.send(f"{name}: {message}".encode('utf-8'))


def handle_client(client,name):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            broadcast(message,name)
        except:
            index = clients_addr.index(client)
            clients_addr.remove(client)
            client.close()
            name = username[index]
            print(f'{name} has left the chat room!')
            username.remove(name)
            break


def Main():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('username?'.encode('utf-8'))
        name = client.recv(1024).decode("utf-8")
        username.append(name)
        clients_addr.append(client)
        print(f'{name} is connected now!')
        # broadcast(f'has connected to the chat room',name)
        # client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,name,))
        thread.start()


if __name__ == "__main__":
    Main()

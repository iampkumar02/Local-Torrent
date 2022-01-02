import threading
import socket
import os

host = 'localhost'
port = 12345
tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp_s.bind((host, port))
udp_s.bind((host, port))
tcp_s.listen()
clients_addr = []
username = []


def broadcast(message):
    for client in clients_addr:
        client.send(message)


def msg(client):
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


def file():
    while True:
        data, addr = udp_s.recvfrom(1024)
        data = str(data.decode("utf-8")).split("@")
        cmd = data[0]
        if cmd == "GET":
            dirname = os.getcwd()
            files = os.listdir(f"{dirname}/server_data")
            if data[1] in files:
                with open(f"{dirname}/server_data/{data[1]}", "r") as f:
                    text = f.read()
                udp_s.sendto(text.encode("utf-8"), addr)
            else:
                udp_s.sendto("File not found.".encode("utf-8"), addr)
            udp_s.sendto("OK@Thank You".encode("utf-8"), addr)
        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            dirname = os.getcwd()
            filepath = os.path.join(f"{dirname}/client_data", name)
            with open(filepath, "w") as f:
                f.write(text)
            send_data = "OK@File uploaded successfully."
            udp_s.sendto(send_data.encode("ascii"), addr)


def handle_client(client):
    msg_thread = threading.Thread(target=msg, args=(client,))
    msg_thread.start()

    file_thread = threading.Thread(target=file, args=())
    file_thread.start()


def Main():
    while True:
        print('Server is running and listening ...')
        client, address = tcp_s.accept()
        print(f'connection is established with {str(address)}')
        client.send('username?'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        username.append(name)
        clients_addr.append(client)
        print(f'{name} is connected now!')
        broadcast(f'{name} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    Main()

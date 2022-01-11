from socket import *


def client():

    host = '192.168.1.7'
    port = 2345
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((host, port))
    print("Connected to the server...")

    while True:
        data = input("> ")
        client.send(data.encode("utf-8"))
        msg = client.recv(1024).decode('utf-8')

        if not msg:
            break
        print(f"Received from server: {msg}")
    client.close()


if __name__ == '__main__':
    client()

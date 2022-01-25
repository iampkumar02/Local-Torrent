from socket import *
import threading
import os


def connection():
    hostname = gethostname()
    ip = gethostbyname(hostname)
    port = 44444
    ADDR = (ip, port)
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    return server,ADDR


# dictionary containing key-value pairs (username,(ip,addr)) of peers
users = ["Devansh", "Prashant"]
ip_list = {"Devansh": ("192.168.1.8", 12020),
           "Prashant": ("192.168.1.3", 12020)}
client_conn = []



def connect_to_peers(client, username):
    pass

if __name__ == "__main__":
    server, ADDR = connection()
    while True:
        print(f'Server is running and listening on {ADDR}....')
        conn, addr = server.accept()
        print(f'connection is established with {str(addr)}')
        # taking username from client and add it to dictionary with its address
        username = conn.recv(1024).decode('utf-8')
        print(username)
        ip_list[username] = addr
        print(ip_list)
        users.append(username)
        client_conn.append(conn)
        print("Total no of clients connected: ", (ip_list))

        thread = threading.Thread(target=connect_to_peers, args=(conn, username,))
        thread.start()

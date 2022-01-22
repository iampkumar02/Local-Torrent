from socket import *
import threading

hostname = gethostname()
ip = gethostbyname(hostname)
port = 44444
ADDR = (ip, port)
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.listen()

# dictionary containing key-value pairs (ip,addr) of peers
ip_list = {}

def client_disconnect(client,username):
    ip_list[username].pop()
    client.close()
    print("{} is disconnected from server".format(username))
    print("Connected devices(IP,PORT): ",ip_list)


def broadcast(message):
    for client in ip_list:
        client.send(message)


def handle_client(client,username):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            client_disconnect(client,username)
            break


def connect_to_peers(client,username):
    peer_name=client.recv(1024).decode("utf-8")
    IP, PORT = ip_list[peer_name]
    client.send("{} {}".format(IP,PORT).encode("utf-8"))
    made_choice=client.recv(1024).decode("utf-8")
    if made_choice==2:
        handle_client(client,username)


while True:
    print(f'Server is running and listening on {ADDR}....')
    conn, addr = server.accept()
    print(f'connection is established with {str(addr)}')
    # taking username from client and add it to dictionary with its address
    username = conn.recv(1024).decode('utf-8')
    ip_list[username] = addr

    thread = threading.Thread(target=connect_to_peers, args=(conn,username,))
    thread.start()

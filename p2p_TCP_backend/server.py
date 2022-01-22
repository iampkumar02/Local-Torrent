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
client_conn = []


def client_disconnect(client, username):
    ip_list[username].pop()
    client.close()
    print("{} is disconnected from server".format(username))
    print("Connected devices(IP,PORT): ", ip_list)


def broadcast(message):
    # print("Inside broadcasting!!!!!!", len(client_conn))
    for client in client_conn:
        # message is received in bytes
        client.send(message)


def handle_client(client, username):
    # print("Inside handle_client!!!!!!")
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            client_disconnect(client, username)
            break


def connect_to_peers(client, username):
    made_choice = client.recv(1024).decode("utf-8")
    made_choice = int(made_choice)
    if made_choice == 2:
        # print("You made a choice!!!! ",made_choice)
        handle_client(client, username)
    elif made_choice == 1:
        print("You made a choice!!!! ", made_choice)
        peer_name = client.recv(1024).decode("utf-8")
        IP, PORT = ip_list[peer_name]
        client.send("{} {}".format(IP, PORT).encode("utf-8"))
    else:
        print("You made a choice!!!! ", made_choice)
        peer_name = client.recv(1024).decode("utf-8")
        IP, PORT = ip_list[peer_name]
        # sending all file names to client from database
        list_from_db = [""]
        client.send(list_from_db.encode("utf-8"))
        while True:
            file_no = int(client.recv(1024).decode("utf-8"))
            # cnt is the count of all file_name present in database
            cnt = 10
            if 1 <= file_no <= cnt:
                client.send("{} {}".format(IP, PORT).encode("utf-8"))
                break
            else:
                client.send("You choosed wrong fle no")


while True:
    print(f'Server is running and listening on {ADDR}....')
    conn, addr = server.accept()
    print(f'connection is established with {str(addr)}')
    # taking username from client and add it to dictionary with its address
    username = conn.recv(1024).decode('utf-8')
    ip_list[username] = addr
    client_conn.append(conn)
    print("Total no of clients connected: ", (ip_list))

    thread = threading.Thread(target=connect_to_peers, args=(conn, username,))
    thread.start()

from socket import *
import threading
from tqdm import tqdm
import json
import os
import sys
# import sqlite3

# db = sqlite3.connect("torrent.db")
# db_conn = db.cursor()
FORMAT = "utf-8"
ip = "192.168.1.7"
port = 44444
ADDR = (ip, port)
username = input("Enter your username: ")

# query = f'INSERT INTO users(user_name) VALUES("{username}")'
# db_conn.execute(query)

# add username to database
# pass

# uploading all files to database from your directory
# pass


# creating connection with server
c_server = socket(AF_INET, SOCK_STREAM)
c_server.connect(ADDR)
c_server.send(username.encode("utf-8"))
peers_ip_list = {}

ADDR1 = ("localhost", 12000)


# Group messaging---------------------------------


def client_receive():
    while True:
        try:
            message = c_server.recv(1024).decode('utf-8')
            print(message)
        except:
            print('Error!')
            c_server.close()
            break


def client_send():
    while True:
        message = f'{username}: {input("")}'
        # print(message)
        c_server.send(message.encode('utf-8'))


def group_msg():
    print("Good to GO!")
    receive_thread = threading.Thread(target=client_receive, args=())
    receive_thread.start()

    send_thread = threading.Thread(target=client_send, args=())
    send_thread.start()

    receive_thread.join()
    send_thread.join()

# private messaging with other peer---------------------
# while receiving it acts as a server for making TCP connection for messaging


def pvt_client_receive(msg_conn):
    # print("func pv_client_receive executed")

    while True:
        try:
            message = msg_conn.recv(1024).decode('utf-8')
            print(message)
        except:
            print('Error!')
            msg_conn.close()
            break


def pvt_client_send(c_msg_send):
    # print("func pv_client_receive executed")
    while True:
        message = f'{username}: {input("")}'
        print(message)
        c_msg_send.send(message.encode('utf-8'))


def creating_msg_connection():
    # Making new connection as server------------------------
    c_msg_recv = socket(AF_INET, SOCK_STREAM)
    hostname = gethostname()
    local_ip = gethostbyname(hostname)

    # local_ip = "192.168.1.4"
    print("Local IP: ", local_ip)
    c_msg_recv.bind((local_ip, 12000))
    c_msg_recv.listen()

    print(f"{local_ip} and 12000 is ready to connect...")
    msg_conn, msg_addr = c_msg_recv.accept()
    print("New connection is established for pvt message with ", msg_addr)
    pvt_client_receive(msg_conn)


def accepting_msg_connection(ip_new):
    # Making new connection as client by connecting to other peer as server------------------------

    # print("In fun private_msg, IP_NEW[0]: ", ip_new[0])
    c_msg_send = socket(AF_INET, SOCK_STREAM)
    c_msg_send.connect((ip_new[0], 12000))

    # print("Connection established with " + ip_new[0])
    pvt_client_send(c_msg_send)


def private_msg(ip_new):
    print("Good to GO!")
    thread = threading.Thread(target=creating_msg_connection, args=())
    thread.start()

    accept_thread = threading.Thread(
        target=accepting_msg_connection, args=(ip_new,))
    accept_thread.start()

    thread.join()
    accept_thread.join()

# File transferring starts from here---------------------------------


def temp_file_fetch(user, cnt):
    with open('temp_file.json', 'r') as g:
        json_data = json.load(g)
        user1 = json_data['users']
        l = len(user1)
        for i in range(0, l):
            name = user1[i]['username']
            if name == user:
                user1[i]['count'] = cnt
                break

        with open('temp_file.json', 'w') as g:
            g.write(json.dumps(json_data))
    g.close()

# while receiving it acts as a server for making TCP connection for file transfer


def pvt_client_receive_file(file_conn):
    # print("func pv_client_receive executed")
    file_conn.send(username.encode("utf-8"))

    data = file_conn.recv(1024).decode('utf-8')

    item = data.split("@")
    FILENAME = item[0]
    FILESIZE = int(item[1])

    """ Data transfer """
    bar = tqdm(range(FILESIZE), f"Receiving long.txt",
               unit="B", unit_scale=True, unit_divisor=1024)

    with open("E:\Computer Network\Local-torrent\client_data\\text.txt", "w") as f:
        g = open('temp_file.json')
        data = json.load(g)
        v = 0
        for i in data['users']:
            name = i['username']
            if name == username:
                v = i['count']
                f.seek(v)
                break
        j = 0
        while j < v/1024:
            j += 1
            bar.update(1024)

        g.close()
        while True:
            data = file_conn.recv(1024).decode("utf-8")
            # if cnt == 40000 or cnt == 60000:
            #     input("Press Enter to continue...")
            if not data:
                break

            f.write(data)
            bar.update(len(data))

    file_conn.close()


def pvt_client_send_file(c_msg_send):
    # print("func pv_client_receive executed")
    FILENAME = "E:\Computer Network\Local-torrent\server_data\\share.txt"
    FILESIZE = os.path.getsize(FILENAME)

    user = c_msg_send.recv(1024).decode("utf-8")

    f = open('temp_file.json')
    data = json.load(f)

    c = 0
    for i in data['users']:
        v = i['username']
        if v == user:
            c = 1
            break
    if not c:
        j = {"username": user, "count": 0}

        with open('temp_file.json', "r+") as file:
            file_data = json.load(file)
            file_data["users"].append(j)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    data = f"{FILENAME}@{FILESIZE}"
    c_msg_send.send(data.encode(FORMAT))
    msg = c_msg_send.recv(1024).decode(FORMAT)
    print(f"SERVER: {msg}")
    cnt = 0
    """ Data transfer. """
    bar = tqdm(range(FILESIZE), f"Sending long.txt",
               unit="B", unit_scale=True, unit_divisor=1024)

    with open("E:\Computer Network\Local-torrent\server_data\share.txt", "r") as f:
        g = open('temp_file.json')
        data = json.load(g)
        v = 0
        for i in data['users']:
            name = i['username']
            if name == user:
                v = i['count']
                f.seek(v)
                break
        j = 0
        while j < v/1024:
            j += 1
            bar.update(1024)

        g.close()
        cnt1 = 0
        while True:
            data = f.read(1024)

            if not data:
                break
            cnt += 1
            try:
                c_msg_send.send(data.encode(FORMAT))
                c_msg_send.send(data.encode(FORMAT))
                bar.update(len(data))
            except:
                print("\nClient stopped receiving!")
                cnt -= 1
                print(f"Total No. of Packets sended: {cnt}")
                cnt1 = 1
                cnt = v+(cnt*1024)
                temp_file_fetch(user, cnt)
                sys.exit()
        if not cnt1:
            temp_file_fetch(user, 0)

    c_msg_send.close()
    # print(f"\nTotal No. of Packets sended: {cnt}")


def creating_file_connection():
    # Making new connection as server------------------------
    c_msg_recv = socket(AF_INET, SOCK_STREAM)
    hostname = gethostname()
    local_ip = gethostbyname(hostname)

    # local_ip = "192.168.1.4"
    print("Local IP: ", local_ip)
    c_msg_recv.bind((local_ip, 13000))
    c_msg_recv.listen()

    print(f"{local_ip} and 13000 is ready to connect...")
    file_conn, msg_addr = c_msg_recv.accept()
    print("New connection is established for pvt message with ", msg_addr)
    pvt_client_receive_file(file_conn)


def accepting_file_connection(ip_new):
    # Making new connection as client by connecting to other peer as server------------------------

    # print("In fun private_msg, IP_NEW[0]: ", ip_new[0])
    c_msg_send = socket(AF_INET, SOCK_STREAM)
    c_msg_send.connect((ip_new[0], 13000))

    # print("Connection established with " + ip_new[0])
    pvt_client_send_file(c_msg_send)


def file_transfer(ip_new):
    print("Good to GO!")
    thread = threading.Thread(target=creating_file_connection, args=())
    thread.start()

    accept_thread = threading.Thread(
        target=accepting_file_connection, args=(ip_new,))
    accept_thread.start()

    thread.join()
    accept_thread.join()


while True:
    # choose an option out of three options--------------------
    print("Enter: \n1. Private Message\n2. Group Message\n3. File transfer\n")
    choice = int(input("Input: "))
    print("Your choice is:", choice)

    if choice == 1:
        c_server.send(str(choice).encode("utf-8"))
        peer_name = input("Enter the peer name to connect with: ")
        c_server.send(peer_name.encode("utf-8"))
        # get ip address of other peers from server-----------
        data = c_server.recv(1024).decode("utf-8")
        data = data.split(" ")
        ip_new, port_new = data
        ip_new = (ip_new, port_new)
        print("IP address of peer received from server:", ip_new)
        peers_ip_list[peer_name] = ip_new

        thread = threading.Thread(target=private_msg, args=(ip_new,))
        thread.start()
        thread.join()
    elif choice == 2:
        c_server.send(str(choice).encode("utf-8"))
        thread = threading.Thread(target=group_msg, args=())
        thread.start()
        thread.join()
    elif choice == 3:
        c_server.send(str(choice).encode("utf-8"))
        peer_name = input("Enter the peer name to connect with: ")
        c_server.send(peer_name.encode("utf-8"))
        filelist_from_server = c_server.recv(1024).decode("utf-8")
        print(filelist_from_server)
        while True:
            file_no = input("Enter the file no to receive: ")
            c_server.send(file_no.encode("utf-8"))

            reply = c_server.recv(1024).decode("utf-8")
            print(reply)
            if reply == "You choosed wrong fle no":
                print("Please choose a file from the list.")
            else:
                break

        if reply == "The server directory is empty":
            continue
        # get ip address of other peers from server-----------
        data = reply.split(" ")
        ip_new, port_new = data
        ip_new = (ip_new, port_new)
        print("IP address of peer received from server:", ip_new)
        peers_ip_list[peer_name] = ip_new

        thread = threading.Thread(target=file_transfer, args=(ip_new,))
        thread.start()
        thread.join()
    else:
        print("Invalid choice, Please try again!")

    # thread = threading.Thread(target=diff_options, args=(ip_new,))
    # thread.start()

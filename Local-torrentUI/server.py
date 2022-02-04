from ast import In
import threading
import socket
import sys
import os
from dotenv import load_dotenv
import mysql.connector as mysql
import time

load_dotenv()

try:
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd=os.getenv('password'),
        database="datacamp"
    )
    print("Connected to database...")
except Exception as e:
    print("Database not connected", e)
    sys.exit()

cursor = db.cursor()


def connect_method():
    host = 'localhost'
    port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    return server


# dictionary containing key-value pairs (username,(ip,addr)) of peers
# ip_list = {"Devansh": ("192.168.1.8", 12020),
#            "Prashant": ("192.168.1.3", 12020)}
# client_conn = []
# users = []
users = []
ip_list = []
client_conn = []


def broadcast(message, name):

    for client in client_conn:
        index = client_conn.index(client)
        msg = message.split('#')
        if msg[0] == "USERNAME" or msg[0] == "IP_LIST":
            client.send(message.encode('utf-8'))
        else:
            if users[index] == name:
                client.send(f"You: {message}".encode('utf-8'))
            else:
                client.send(f"{name}: {message}".encode('utf-8'))

# Here the server is sending the list of files to user by fetching it from database-------

def sendingFiles(client, name, msg):
    client_name = msg[1]
    print(f"Getting files of {msg[1]}")
    # Get files of client_name (msg[1]) from database
    q_user = "SELECT file_id FROM users WHERE username=%s"
    values_user = ('Niklaus',)
    cursor.execute(q_user, values_user)
    records = cursor.fetchall()

    q = "SELECT * FROM uploaded_file_list WHERE id = %s"
    values = (records[0][0],)

    cursor.execute(q, values)
    allFiles = cursor.fetchall()

    tag = "FILE_LIST#"
    # file_list = tag+f"{allFiles}"

    client.send(f"{tag}@{client_name}".encode('utf-8'))
    print("Window opened!")
    for i in range(len(allFiles)-15):
        time.sleep(1)
        print(f"Sending file {i+1}")
        client.send(f"{tag}FILE_NAME@{allFiles[i]}".encode('utf-8'))

# Here one to one chatting can be done (Privately)------------------------------

def sendingPvtMsg(client, name, msg):
    client_col, msg = msg[1].split("@")
    if not msg == "":
        print("Not Opening Window from server")
        print(f"Sending Message {msg} to user {client_col}")
        tag = "PVT_MSG#"
        msg_curr = tag+f"{name}: {msg}"
        # msg_clien_col = tag+f"{client_col}: {msg}"

        print(msg_curr)
        # print(msg_clien_col)
        try:
            print("Index found!")
            index2 = users.index(client_col)
            print("index2: ", index2)
        except IndexError as In:
            print("Index not found!", In)

        print("Sending one time to itself")
        client.send(msg_curr.encode('utf-8'))
        try:
            print("Sending one time to client")
            client_conn[index2].send(msg_curr.encode('utf-8'))
        except Exception as e:
            print("Error (Client Not Found): ", e)
    else:
        client.send(f"PVT_MSG#@{client_col}".encode('utf-8'))
        print("Opening Pvt Window from server")

# This function will get enough information for P2P file transfer from database
# And send this info to other client------------------------------------------

def downloadFile(client, name, msg):
    # file_name,curr_username,down_dir_current_user
    print("Info: ",msg[1])
    file_name, client_name = msg[1].split("@")
    # print("File Name: ",file_name)
    try:
        query = "SELECT file_down_dir FROM users WHERE username=%s"
        values = ("Niklaus",)
        cursor.execute(query, values)
        down_dir_current_user = cursor.fetchall()
        print("Rec1: ", down_dir_current_user)
    except Exception as e:
        print("Unable to find file_down_dir: ",e)

    try:
        q_user = "SELECT file_id FROM users WHERE username=%s"
        values_user = ('Niklaus',)
        cursor.execute(q_user, values_user)
        records = cursor.fetchall()
        print("Rec2: ", records)
    except Exception as e:
        print("Unable to find file_id: ",e)

    # Here id and file_name/dir makes composite primary key
    try:
        client_file_dir_query = "SELECT dir FROM uploaded_file_list WHERE file_name=%s AND id=%s"
        value1 = (file_name,records[0][0],)
        cursor.execute(client_file_dir_query, value1)
        upload_file_dir = cursor.fetchall()

        tag = "DOWNLOAD_PORT#"
        info = tag+upload_file_dir[0][0]+"@"+name+"@"+down_dir_current_user[0][0]
        print("Sending Info: ",info)

        try:
            client_name=client_name[0:3]
            client_index = users.index(client_name)
            client_conn[client_index].send(info.encode('utf-8'))
        except Exception as e:
            print("Client index not found")
            print("Error: ",e)
    except Exception as e:
        print("Unable to find uploaded file dir: ",e)


# This function will receive every message coming from each users----------------------
# And each function inside this, using thread so that each functions execute independently

def handle_client(client, name):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            msg = message.split("#")
            if msg[0] == "FILE_LIST":
                file_thread = threading.Thread(
                    target=sendingFiles, args=(client, name, msg,))
                file_thread.start()
            elif msg[0] == "PVT_MSG":
                pvt_msg_thread = threading.Thread(
                    target=sendingPvtMsg, args=(client, name, msg,))
                pvt_msg_thread.start()
            elif msg[0] == "DOWNLOAD":
                down_file_thread = threading.Thread(
                    target=downloadFile, args=(client, name,msg))
                down_file_thread.start()
                down_file_thread.join()
            else:
                broadcast_thread = threading.Thread(
                    target=broadcast, args=(message, name,))
                broadcast_thread.start()

        except Exception as e:
            print("Error: ", e)
            index = client_conn.index(client)
            client_conn.remove(client)
            ip_list.pop(index)

            name = users[index]

            client.close()
            print(f'{name} has left the chat room!')
            users.remove(name)

            broadcast(f"USERNAME#{users}", name)
            broadcast(f"IP_LIST#{ip_list}", name)
            break


def Main():
    server = connect_method()
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('username?'.encode('utf-8'))
        name = client.recv(1024).decode("utf-8")
        ip_list.append(address)
        # Sending ip_list to client
        users.append(name)
        client_conn.append(client)
        print(f'{name} is connected now!')

        broadcast(f"USERNAME#{users}", name)
        broadcast(f"IP_LIST#{ip_list}", name)

        thread = threading.Thread(target=handle_client, args=(client, name,))
        thread.start()


if __name__ == "__main__":
    Main()

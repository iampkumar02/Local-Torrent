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
    try:
        q_user = "SELECT file_id FROM users WHERE username=%s"
        values_user = (client_name,)
        cursor.execute(q_user, values_user)
        records = cursor.fetchall()
    except Exception as e:
        print("Unable to find file_id: ",e)

    try:
        q = "SELECT * FROM uploaded_file_list WHERE id = %s"
        values = (records[0][0],)

        cursor.execute(q, values)
        allFiles = cursor.fetchall()

        tag = "FILE_LIST#"
        # file_list = tag+f"{allFiles}"

        client.send(f"{tag}@{client_name}".encode('utf-8'))
        print("Window opened!")
        for i in range(len(allFiles)):
            time.sleep(1)
            print(f"Sending file {i+1}")
            client.send(f"{tag}FILE_NAME@{allFiles[i]}".encode('utf-8'))
            
    except Exception as e:
        print("Unable to find uploaded_file_list: ",e)

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
        values = (client_name,)
        cursor.execute(query, values)
        down_dir_current_user = cursor.fetchall()
        print("Rec1: ", down_dir_current_user)
    except Exception as e:
        print("Unable to find file_down_dir: ",e)

    try:
        q_user = "SELECT file_id FROM users WHERE username=%s"
        values_user = (client_name,)
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
            # client_name=client_name[0:3]
            client_index = users.index(client_name)
            client_conn[client_index].send(info.encode('utf-8'))
        except Exception as e:
            print("Client index not found")
            print("Error: ",e)
    except Exception as e:
        print("Unable to find uploaded file dir: ",e)


def databaseNameCheck(client, msg):
    try:
        query_name = "SELECT username FROM users"
        # values_name = ("Niklaus",)
        cursor.execute(query_name)
        db_names = cursor.fetchall()
        print("NAMES: ", db_names)

        name_already=False
        tag = "DATABASECHECK#"
        for n in db_names:
            print(n[0])
            if n[0] == msg[1]:
                name_already=True
                client.send(f"{tag}Username already exists@{msg[1]}".encode('utf-8'))
                break
        if not name_already:
            client.send(f"{tag}All OK@{msg[1]}".encode('utf-8'))

    except Exception as e:
        print("Unable to find file_down_dir: ", e)


def insertIntoDatabase(client, name, msg):
    user,downl_dir,upload_dir,data1=msg.split("@")
    print("INSERTING INTO database!!")

    try:
        query = "INSERT INTO users (username,file_down_dir) VALUES (%s,%s)"
        values = (user, downl_dir,)
        cursor.execute(query, values)
        print("Successfully inserted into database: ")
    except Exception as e:
        print("Unable to find file_down_dir: ", e)

    db.commit()

    try:
        q_id="SELECT file_id FROM users WHERE username=%s"
        v_id=(user,)
        cursor.execute(q_id, v_id)
        id = cursor.fetchall()
        print("Successfully get id from database")
    except Exception as e:
        print("Unable to find file_id: ", e)

    print("\nID: ", id)

    file_dir_list, file_list, sizes = data1.split("$")
    file_dir_list = file_dir_list.split("'")[1::2]
    file_list = file_list.split("'")[1::2]
    sizes = sizes.split("'")[1::2]

    print("Final All: ", file_list)

    query_ls = "INSERT INTO uploaded_file_list(id,dir,file_name,file_size) VALUES (%s,%s,%s,%s)"
    for i in range(len(file_dir_list)):
        try:
            ls_values = (id[0][0], file_dir_list[i], file_list[i], sizes[i],)
            cursor.execute(query_ls, ls_values)
        except Exception as e:
            print(f"Error{i}: ", e)
            break

    db.commit()


# This function will receive every message coming from each users----------------------
# And each function inside this, using thread so that each functions execute independently

def handle_client(client,address):
    while True:
        name = client.recv(1024).decode("utf-8")
        if name == "BREAK":
            print("Loop is broken")
            break
        check_name=name.split("#")
        print("NAME: ",check_name)

        if check_name[0] == 'DATABASECHECK':
            print("Working!!")
            database_check_name_thread = threading.Thread(
                target=databaseNameCheck, args=(client, check_name,))
            database_check_name_thread.start()
            database_check_name_thread.join()

    client.send('username?'.encode('utf-8'))
    name = client.recv(1024).decode("utf-8")

    ip_list.append(address)
    # Sending ip_list to client
    users.append(name)
    client_conn.append(client)
    print(f'{name} is connected now!')

    broadcast(f"USERNAME#{users}", name)
    broadcast(f"IP_LIST#{ip_list}", name)

    s=""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print("\nLength",len(message))
            # print("Message: ",message)
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
            elif msg[0] == 'DATABASECHECK':
                database_check_name_thread = threading.Thread(target=databaseNameCheck, args=(client, msg,))
                database_check_name_thread.start()
                database_check_name_thread.join()
            elif msg[0] == 'SEARCHFILE':
                client.send(f"SEARCHFILE#{msg[1]}".encode('utf-8'))
            elif msg[0] == 'DATABASEINSERT':
                
                if msg[1] == 'START':
                    s=""
                if not (msg[1] == 'START' or msg[1] == 'END'):
                    s+=msg[1]

                if msg[1] == 'END':
                    database_insert_thread = threading.Thread(target=insertIntoDatabase, args=(client, name, s))
                    database_insert_thread.start()
                    database_insert_thread.join()
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
# def getName(client):


def Main():
    server = connect_method()
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        
        thread = threading.Thread(target=handle_client, args=(client,address,))
        thread.start()


if __name__ == "__main__":
    Main()

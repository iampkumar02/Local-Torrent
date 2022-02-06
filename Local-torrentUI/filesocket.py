from socket import *
import threading
import chatroom.chat_client as client
from tqdm import tqdm
import json

# socket for file transfer
def file_socket():
    while True:
        # hostname_file = gethostname()
        # ip_file = gethostbyname(hostname_file)
        ip_file="localhost"
        port_file = 14000
        server_file = socket(AF_INET, SOCK_STREAM)
        server_file.bind((ip_file, port_file))
        server_file.listen()
        
        file_conn, file_addr = server_file.accept()
        print("Connection established to download")
        # receiving data from other peer

        data = file_conn.recv(1024).decode('utf-8')
        print("Before Error Data: ",data)

        item = data.split("@")
        FILENAME = item[0]
        FILESIZE = int(item[1])

        data_size=file_conn.recv(1024).decode('utf-8')
        print("Data Size: ",data_size)

        """ Data transfer """
        bar = tqdm(range(
            FILESIZE), f"Receiving long.txt", unit="B", unit_scale=True, unit_divisor=1024)
        cnt_size = 0
        with open("E:\Computer Network\Local-torrent\client_data\\text.txt", "w") as f:
            g = open('E:\Computer Network\Local-Torrent\\temp_file.json')
            data = json.load(g)
            v = 0
            for i in data['users']:
                name = i['username']
                if name == "iam":
                    v = i['count']
                    f.seek(v)
                    break
            j = 0
            while j < v/1024:
                j += 1
                bar.update(1024)

            g.close()
            while True:
                cnt_size += 1
                data = file_conn.recv(1024).decode("utf-8")
                if not data:
                    break

                f.write(data)
                bar.update(len(data))
        file_conn.close()
        

file_thread= threading.Thread(target=file_socket,args=())
file_thread.start()

from socket import *
import threading
from tqdm import tqdm
import json


def multi_down(file_conn):
    # receiving data from other peer
    main_rec = file_conn.recv(1024).decode("utf-8")
    file_dir, down_dir = main_rec.split("@")
    file_name=file_dir.split("\\")[-1]
    print("First Received file_name and down_dir", file_name, down_dir)

    data = file_conn.recv(1024).decode('utf-8')
    print("Second Received Data: ", data)

    item = data.split("@")
    FILENAME = item[0]
    FILESIZE = float(item[1])
    FILESIZE = int(round(FILESIZE))

    data_size = file_conn.recv(1024).decode('utf-8')
    print("Third Received Data Size: ", data_size)

    """ Data transfer """
    bar = tqdm(range(FILESIZE), f"Receiving long.txt", unit="B", unit_scale=True, unit_divisor=1024)
    cnt_size = 0
    with open(f"E:\Computer Network\Local-torrent\client_data\\{file_name}", "w") as f:
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
            # if pause_click:
            #     return
            if not data:
                break

            f.write(data)
            bar.update(len(data))
    file_conn.close()

# socket for file transfer
def file_socket():
    ip_file = "localhost"
    port_file = 14000
    server_file = socket(AF_INET, SOCK_STREAM)
    server_file.bind((ip_file, port_file))
    server_file.listen()
    while True:
        # hostname_file = gethostname()
        # ip_file = gethostbyname(hostname_file)
        print("Waiting for new connection...")
        file_conn, file_addr = server_file.accept()
        print("Connection established to download")

        thread = threading.Thread(target=multi_down,args=(file_conn,))
        thread.start()
        

file_thread= threading.Thread(target=file_socket,args=())
file_thread.start()

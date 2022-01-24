import socket
import os
from tqdm import tqdm
import json
import sys

IP = "localhost"
PORT = 4444
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

FILENAME = "E:\Computer Network\Local-torrent\server_data\\share.txt"
FILESIZE = os.path.getsize(FILENAME)


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


def get():
    print("Server is listening...")
    s, addr = server.accept()
    print("Connection established!")
    user = s.recv(1024).decode("utf-8")
    print("Username received: " + user)

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
    s.send(data.encode(FORMAT))
    msg = s.recv(SIZE).decode(FORMAT)
    print(f"SERVER: {msg}")
    cnt = 0
    """ Data transfer. """
    bar = tqdm(range(FILESIZE), f"Sending long.txt",
               unit="B", unit_scale=True, unit_divisor=SIZE)

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
        cnt_size=0
        while True:
            data = f.read(SIZE)

            if not data:
                break
            cnt += 1
            try:
                cnt_size+=1
                s.send(data.encode(FORMAT))
                bar.update(len(data))
            except:
                print("\nClient stopped receiving!")
                cnt -= 1
                print(f"Total No. of Packets sended: {cnt}")
                print("Size of file sended now: ", cnt_size/1024)
                cnt1 = 1
                cnt = v+(cnt*SIZE)
                temp_file_fetch(user, cnt)
                sys.exit()
        if not cnt1:
            temp_file_fetch(user, 0)
        print("Size of file sended now: ", cnt_size/1024)

    s.close()
    # print(f"\nTotal No. of Packets sended: {cnt}")


get()

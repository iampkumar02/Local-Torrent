import socket
from tqdm import tqdm
import json
IP = "localhost"
PORT = 4444
ADDR = (IP, PORT)
SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
username = input("Enter username: ")
client.send(username.encode("utf-8"))


data = client.recv(1024).decode('utf-8')
item = data.split("@")
FILENAME = item[0]
FILESIZE = int(item[1])
client.send("Filename and filesize received".encode("ascii"))
""" Data transfer """
bar = tqdm(range(
    FILESIZE), f"Receiving long.txt", unit="B", unit_scale=True, unit_divisor=SIZE)

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
        data = client.recv(SIZE).decode("utf-8")
        # if cnt == 40000 or cnt == 60000:
        #     input("Press Enter to continue...")
        if not data:
            break

        f.write(data)
        bar.update(len(data))
client.close()

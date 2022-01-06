import socket
import os
from tqdm import tqdm

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


def get():
    print("Server is listening...")
    s, addr = server.accept()
    data = f"{FILENAME}@{FILESIZE}"
    # print(data)
    s.send(data.encode(FORMAT))
    msg = s.recv(SIZE).decode(FORMAT)
    print(f"SERVER: {msg}")

    """ Data transfer. """
    bar = tqdm(range(FILESIZE), f"Sending long.txt",
               unit="B", unit_scale=True, unit_divisor=SIZE)
    for i in range(1, 20):
        with open("E:\Computer Network\Local-torrent\server_data\share.txt", "r") as f:
            while True:
                data = f.read(SIZE)

                if not data:
                    break

                s.send(data.encode(FORMAT))

                bar.update(len(data))
    s.close()
    server.close()


get()

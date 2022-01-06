import socket
import os
from tqdm import tqdm

IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)
# server.listen()

FILENAME = "E:\Computer Network\Local-torrent\server_data\\share.txt"
FILESIZE = os.path.getsize(FILENAME)


def get():
    print("Server is listening...")
    # s, addr = server.accept()
    s, addr = server.recvfrom(1024)
    print(s.decode("utf-8"))

    data = f"{FILENAME}@{FILESIZE}"

    server.sendto(data.encode(FORMAT), addr)

    """ Data transfer. """
    bar = tqdm(range(FILESIZE), f"Sending long.txt",
               unit="B", unit_scale=True, unit_divisor=SIZE)
    for i in range(1, 20):
        with open("E:\Computer Network\Local-torrent\server_data\share.txt", "r") as f:
            while True:
                data = f.read(SIZE)

                if not data:
                    break

                server.sendto(data.encode(FORMAT), addr)

                bar.update(len(data))
    server.close()


get()

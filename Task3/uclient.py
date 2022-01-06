import socket
from tqdm import tqdm
IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client.connect(ADDR)

client.sendto("Sending to server...".encode("utf-8"), ADDR)

data, add = client.recvfrom(1024)
data = data.decode("utf-8")
item = data.split("@")
FILENAME = item[0]
FILESIZE = int(item[1])

""" Data transfer """
bar = tqdm(range(
    FILESIZE), f"Receiving long.txt", unit="B", unit_scale=True, unit_divisor=SIZE)
for i in range(1, 20):
    with open("E:\Computer Network\Local-torrent\client_data\\text_u.txt", "w") as f:
        while True:
            data, add = client.recvfrom(SIZE)
            data = data.decode("utf-8")

            if not data:
                break

            f.write(data)

            bar.update(len(data))

client.close()

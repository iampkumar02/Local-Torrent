import socket
from tqdm import tqdm
IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


data = client.recv(1024).decode('utf-8')
item = data.split("@")
FILENAME = item[0]
FILESIZE = int(item[1])
client.send("Filename and filesize received".encode("ascii"))

""" Data transfer """
bar = tqdm(range(
    FILESIZE), f"Receiving long.txt", unit="B", unit_scale=True, unit_divisor=SIZE)

with open("E:\Computer Network\Tasks\client_data\\text.txt", "w") as f:
    while True:
        data = client.recv(SIZE).decode("utf-8")

        if not data:
            break

        f.write(data)

        bar.update(len(data))
client.close()

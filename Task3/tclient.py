import socket
from tqdm import tqdm
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
    while True:
        data = client.recv(SIZE).decode("utf-8")
        # if cnt == 40000 or cnt == 60000:
        #     input("Press Enter to continue...")
        if not data:
            break

        f.write(data)
        bar.update(len(data))
client.close()

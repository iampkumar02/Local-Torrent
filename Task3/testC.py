from tqdm import tqdm
import os
import socket

host = "localhost"
port = 12345

IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# t = client.recv(1024).decode('utf-8')
# with open("E:\Computer Network\Tasks\client_data\\text.txt", "w") as f:
#     f.write(t)
FILENAME = "E:\Computer Network\Tasks\server_data\\text.txt"
FILESIZE = os.path.getsize(FILENAME)


def main():
    data = f"{FILENAME}@{FILESIZE}"
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"SERVER: {msg}")

    """ Data transfer. """
    bar = tqdm(range(FILESIZE), f"Sending {FILENAME}",
               unit="B", unit_scale=True, unit_divisor=SIZE)

    with open(FILENAME, "r") as f:
        while True:
            data = f.read(SIZE)

            if not data:
                break

            client.send(data.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)

            bar.update(len(data))

    """ Closing the connection """
    client.close()


if __name__ == "__main__":
    main()

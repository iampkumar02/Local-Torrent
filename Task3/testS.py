import socket
from tqdm import tqdm

IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
while True:
    print("Server is listening...")
    conn, addr = server.accept()
    print(f"[+] Client connected from {addr[0]}:{addr[1]}")
    # with open("E:\Computer Network\Tasks\server_data\share.txt", "r") as f:
    #     text = f.read()
    # s.send(text.encode(FORMAT))

    data = conn.recv(SIZE).decode(FORMAT)
    item = data.split("@")
    print(item)
    FILENAME = item[0]
    FILESIZE = int(item[1])

    print("[+] Filename and filesize received from the client.")
    conn.send("Filename and filesize received".encode(FORMAT))

    """ Data transfer """
    bar = tqdm(range(
        FILESIZE), f"Receiving {FILENAME}", unit="B", unit_scale=True, unit_divisor=SIZE)

    with open(f"{FILENAME}", "w") as f:
        while True:
            data = conn.recv(SIZE).decode(FORMAT)

            if not data:
                break

            f.write(data)
            conn.send("Data received.".encode(FORMAT))

            bar.update(len(data))

    """ Closing connection. """
    conn.close()
    server.close()

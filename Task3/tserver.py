import socket
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
    s, addr = server.accept()
    print("Server is listening...")
    with open("E:\Computer Network\Tasks\server_data\share.txt", "r") as f:
        text = f.read()
    s.send(text.encode(FORMAT))

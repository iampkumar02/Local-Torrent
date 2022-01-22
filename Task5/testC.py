import socket
IP = "localhost"
PORT = 4444
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)
# data = client.recv(SIZE).decode('utf-8')
# print(data)
client.close()

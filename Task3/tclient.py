import socket
IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

t = client.recv(1024).decode('utf-8')
with open("E:\Computer Network\Tasks\client_data\\text.txt", "w") as f:
    f.write(t)

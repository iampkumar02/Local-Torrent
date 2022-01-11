from socket import *
host = '192.168.1.7'
port = 2345

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen()

print("Server is running and listening...")
conn, addr = server.accept()
print(f"Client is connected with addr: {addr}")

while True:
    msg = conn.recv(1024)
    if not msg:
        break
    print("Received from client: "+msg.decode('utf-8'))
    conn.send(input("> ").encode("utf-8"))
conn.close()

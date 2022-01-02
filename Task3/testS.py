from socket import *
host = "localhost"
port = 12345
tcp_s = socket(AF_INET, SOCK_STREAM)


tcp_s.bind((host, port))

tcp_s.listen()

while True:
    print("Server is listening...")
    s, addr = tcp_s.accept()
    print("You are connected")
    while True:
        print("i am connected")
        message = s.recv(1024)

from socket import *
host = "localhost"
port = 12345
ADDR = (host, port)
tcp_s = socket(AF_INET, SOCK_STREAM)

tcp_s.connect((host, port))
while True:
    print("Now connected with server")
    p = input("> ")

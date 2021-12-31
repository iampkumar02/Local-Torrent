from socket import *
host = "localhost"
port = 12345

# create socket
sockfd = socket(AF_INET, SOCK_DGRAM)

addr = (host, port)
sockfd.sendto("this is from client".encode("utf-8"), addr)
msg, add = sockfd.recvfrom(1024)
print(msg.decode("utf-8"))
msg, add = sockfd.recvfrom(1024)
print(msg.decode("utf-8"))
msg, add = sockfd.recvfrom(1024)
print(msg.decode("utf-8"))
msg, add = sockfd.recvfrom(1024)
print(msg.decode("utf-8"))
sockfd.sendto("this is again from client".encode("utf-8"), addr)

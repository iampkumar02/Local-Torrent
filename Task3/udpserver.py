from socket import *
import time
start_time = time.time()
host = "localhost"
port = 12345
server = socket(AF_INET, SOCK_DGRAM)

server.bind((host, port))
print("server is listening")

s, addr = server.recvfrom(1024)
print(s.decode("utf-8"), addr)
msg = "I"
server.sendto(msg.encode("utf-8"), addr)
msg = "Am"
server.sendto(msg.encode("utf-8"), addr)
msg = "P"
server.sendto(msg.encode("utf-8"), addr)
msg = "K"
server.sendto(msg.encode("utf-8"), addr)
print(round(time.time()-start_time, 2))
time.sleep(10)
ss, addrr = server.recvfrom(1024)
print(ss, addrr)

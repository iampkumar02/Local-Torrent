from socket import *

ip = "192.168.1.7"
port = 44444
ADDR = (ip, port)
username = "iampkumar"

client=socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

client.send(username.encode("utf-8"))

from socket import *
import threading
import time
host = "localhost"
port = 12345


def th():
    while True:
        tcp_s = socket(AF_INET, SOCK_STREAM)
        tcp_s.connect((host, port))
        tcp_s.close()


th()

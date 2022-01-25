from socket import *
import threading

# socket for private messaging
def msg_socket():
    while True:
        hostname_msg = gethostname()
        ip_msg = gethostbyname(hostname_msg)
        port_msg=12000
        server_msg=socket(AF_INET, SOCK_STREAM)
        server_msg.bind((ip_msg, port_msg))
        server_msg.listen()

        msg_conn,msg_addr=server_msg.accept()

# socket for file transfer
def file_socket():
    while True:
        hostname_file = gethostname()
        ip_file = gethostbyname(hostname_file)
        port_file = 14000
        server_file = socket(AF_INET, SOCK_STREAM)
        server_file.bind((ip_file, port_file))
        server_file.listen()
        
        file_conn, file_addr = server_file.accept()


thread_msg = threading.Thread(target=msg_socket, args=())
thread_file = threading.Thread(target=file_socket, args=())

thread_msg.start()
thread_file.start()





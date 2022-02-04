from socket import *
import threading
import chatroom.chat_client as client

# socket for file transfer
def file_socket():
    while True:
        # hostname_file = gethostname()
        # ip_file = gethostbyname(hostname_file)
        ip_file="localhost"
        port_file = 14000
        server_file = socket(AF_INET, SOCK_STREAM)
        server_file.bind((ip_file, port_file))
        server_file.listen()
        
        file_conn, file_addr = server_file.accept()
        print("Connection established to download")
        

file_thread= threading.Thread(target=file_socket,args=())
file_thread.start()
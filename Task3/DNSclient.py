from socket import *
import threading
import os

host = "localhost"
port = 12345
ADDR = (host, port)
udp_s = socket(AF_INET, SOCK_DGRAM)
tcp_s = socket(AF_INET, SOCK_STREAM)

tcp_s.connect(ADDR)


alias = input('Enter the name: ')


def client_receive():
    while True:
        try:
            message = tcp_s.recv(1024).decode('utf-8')
            if message == "username?":
                tcp_s.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            tcp_s.close()
            break


def client_send():
    while True:
        data = input("")
        if data[0:2] == ">>":
            data = data[2:]
            info = data.split(" ")
            if info[0] == "GET":
                filename = info[1]
                # udp starts here
                udp_s.sendto(f"{info[0]}@{filename}".encode("utf-8"), ADDR)
                text = udp_s.recvfrom(1024)
                text = text[0].decode("utf-8")

                if text == "File not found.":
                    print(text)
                else:
                    dirname = "E:\Computer Network\Tasks/client_data"
                    filelist = os.listdir(dirname)
                    filepath = os.path.join(dirname, filename)
                    name = filename.split(".")
                    rename = name[0].split("_")

                    i = 0
                    if filename in filelist:
                        for file in filelist:
                            if not file.find(f"{rename[0]}_") == -1:
                                br = file.split(".")
                                i = max(i, int(br[0][-1]))

                        filename = rename[0]+"_"+str(i+1)+"."+name[1]
                        filepath = os.path.join(dirname, filename)
                        with open(filepath, "w") as f:
                            f.write(text)
                    else:
                        with open(filepath, "w") as f:
                            f.write(text)

                    print("File successfully downloaded.")

            elif info[0] == "UPLOAD":
                dirname = os.getcwd()
                path = f"E:/Computer Network/Tasks/client_data/{info[1]}"
                with open(f"{path}", "r") as f:
                    text = f.read()
                filename = path.split("/")[-1]
                send_data = f"{info[0]}@{filename}@{text}"
                udp_s.sendto(send_data.encode("ascii"), ADDR)

            else:
                print("Invalid entry!")

        elif data[0] == ">":
            data = data[1:]
            message = f'{alias}: {data}'
            tcp_s.send(message.encode('utf-8'))

        else:
            print("Invalid entry!")


receive_thread = threading.Thread(target=client_receive, args=())
receive_thread.start()

send_thread = threading.Thread(target=client_send, args=())
send_thread.start()

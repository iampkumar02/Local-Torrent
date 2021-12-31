import socket
import os

IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        elif cmd == "UPLOAD":
            # dirname = os.path.dirname(__file__)
            dirname = os.getcwd()
            path = f"E:/Computer Network/Tasks/client_data/{data[1]}"

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))

        elif cmd == "GET":
            filename = data[1]

            client.send(f"{cmd}@{filename}".encode(FORMAT))
            text = client.recv(1024).decode("utf-8")

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

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()

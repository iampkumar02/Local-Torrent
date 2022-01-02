import socket
import os

IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.sendto(cmd.encode(FORMAT), ADDR)

        elif cmd == "LOGOUT":
            client.sendto(cmd.encode(FORMAT), ADDR)
            break

        elif cmd == "LIST":
            client.sendto(cmd.encode(FORMAT), ADDR)

        elif cmd == "DELETE":
            client.sendto(f"{cmd}@{data[1]}".encode(FORMAT), ADDR)

        elif cmd == "UPLOAD":
            dirname = os.getcwd()
            path = f"E:/Computer Network/Tasks/client_data/{data[1]}"

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.sendto(send_data.encode(FORMAT))

        elif cmd == "GET":
            filename = data[1]

            client.sendto(f"{cmd}@{filename}".encode(FORMAT), ADDR)
            text = client.recvfrom(1024)
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

        data, addr = client.recvfrom(SIZE)
        cmd, msg = (data.decode("utf-8")).split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

    print("Disconnected from the server.")
    client.close()


if __name__ == "__main__":
    main()

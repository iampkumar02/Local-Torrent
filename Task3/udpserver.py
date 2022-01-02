
import os
import socket
import threading

IP = "localhost"
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)

    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        data, addr = server.recvfrom(1024)
        data = str(data.decode("utf-8")).split("@")
        cmd = data[0]

        if cmd == "LIST":
            dirname = os.getcwd()
            files = os.listdir(f"{dirname}/server_data")
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            server.sendto(send_data.encode(FORMAT), addr)

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            # dirname = os.path.dirname(__file__)
            dirname = os.getcwd()
            filepath = os.path.join(f"{dirname}/client_data", name)
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File uploaded successfully."
            server.sendto(send_data.encode(FORMAT), addr)

        elif cmd == "GET":
            # filename = server.recvfrom(1024).decode("ascii")
            dirname = os.getcwd()
            files = os.listdir(f"{dirname}/server_data")
            if data[1] in files:
                with open(f"{dirname}/server_data/{data[1]}", "r") as f:
                    text = f.read()
                server.sendto(text.encode(FORMAT), addr)
            else:
                server.sendto("File not found.".encode(FORMAT), addr)
            server.sendto("OK@Thank You".encode(FORMAT), addr)

        elif cmd == "DELETE":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    print(SERVER_DATA_PATH)
                    print(
                        f'del "E:/Computer Network/Tasks/server_data/{filename}"')
                    os.system(
                        f'del "E:/Computer Network/Tasks/server_data/{filename}"')
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            server.sendto(send_data.encode(FORMAT), addr)

        elif cmd == "LOGOUT":
            break
        elif cmd == "HELP":
            data = "OK@"
            data += "LIST: List all the files from the server.\n"
            data += "UPLOAD <path>: Upload a file to the server.\n"
            data += "GET <path>: Get a file from the server.\n"
            data += "DELETE <filename>: Delete a file from the server.\n"
            data += "LOGOUT: Disconnect from the server.\n"
            data += "HELP: List all the commands."
            server.sendto(data.encode(FORMAT), addr)


if __name__ == "__main__":
    main()

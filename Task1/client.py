import threading
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))
alias = input('Enter the name: ')


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "username?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive, args=())
receive_thread.start()

send_thread = threading.Thread(target=client_send, args=())
send_thread.start()

import threading
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 12345))


def input_name():
    user = input('Enter the name: ')
    return user



def client_receive(user):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "username?":
                client.send(user.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = input("")
        client.send(message.encode('utf-8'))

def main(name):
    receive_thread = threading.Thread(target=client_receive, args=(name,))
    receive_thread.start()

    send_thread = threading.Thread(target=client_send, args=())
    send_thread.start()

if __name__ == '__main__':
    name=input_name()
    main(name)

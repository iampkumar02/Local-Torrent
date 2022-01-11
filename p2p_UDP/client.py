import socket
import sys
import threading

rendezvous = ('localhost', 55555)

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50006))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recvfrom(1024)[0].decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recvfrom(1024)[0].decode("utf-8")
sock.close()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001


def listen():
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind(('192.168.1.7', sport))

    while True:
        data = sock.recvfrom(1024)
        print('\rpeer: {}\n> '.format(data[0].decode("utf-8")))


listener = threading.Thread(target=listen, daemon=True)
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('192.168.1.7', dport))

while True:
    msg = input('> ')
    sock.sendto(msg.encode("utf-8"), (ip, sport))

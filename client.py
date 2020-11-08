import socket

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print('Para sair digite quit\n')
msg = input()

def sendmsg(msg):
    tcp.send(msg.encode())

while msg != '\x18':
    tcp.send(msg.encode())
    data = tcp.recv(1024)
    print(data.decode())
    msg = input()

tcp.close()
# IRC-server
import socket
import time
import os

portaHost= 65001

# requisita API do SO uma conexão AF_INET (IPV4)
#   com protocolo de transporte SOCK_STREAM (TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Esperando para Conectar no Server...")
time.sleep(5)
sock.connect((socket.gethostname(), portaHost))
print("Pronto, falai =]")

while 1:
    mensagem = input()
    #se o usuário quiser sair sai
    if mensagem == '/quit':
       sock.close()
       break
    elif mensagem == '/clear':
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
             sock.send(mensagem.encode("utf-8"))
             time.sleep(5)
             answer = sock.recv(512)

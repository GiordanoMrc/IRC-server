# IRC-server
import socket
import time
import os

portaHost= 65015
# requisita API do SO uma conexão AF_INET (IPV4)
#   com protocolo de transporte SOCK_STREAM (TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Esperando para Conectar no Server...")
time.sleep(5)
sock.connect((socket.gethostname(), portaHost))

os.system('cls' if os.name == 'nt' else 'clear')
print ("!-----------------------------------!")
print ("!Comandos Suportados:               !")
print ("!   ?USUARIO (nick, host, nome)     !")
print ("!       ?SAIR                       !")
print ("!       ?ENTRAR (canal)             !")
print ("!       ?LISTAR                     !")
print ("!       ?SAIRC   (canal)            !")
print ("!       /quit                       !")
print ("!       /clear                      !")
print ("!+++++++++++++++++++++++++++++++++++!")
print ("!    Seja Bem vindo ao min-IRC      !")
print ("!-----------------------------------!")
print (">")

while 1:
    mensagem = input()
    #se o usuário quiser sair sai
    if mensagem == '/quit':
       break
    elif mensagem == '/clear':
        os.system('cls' if os.name == 'nt' else 'clear')
        print ("!-----------------------------------!")
        print ("!Comandos Suportados:               !")
        print ("!   ?USUARIO (nick, host, nome)     !")
        print ("!       ?SAIR                       !")
        print ("!       ?ENTRAR (canal)             !")
        print ("!       ?LISTAR                     !")
        print ("!       ?SAIRC   (canal)            !")
        print ("!       /quit                       !")
        print ("!       /clear                      !")
        print ("!+++++++++++++++++++++++++++++++++++!")
        print ("!    Seja Bem vindo ao min-IRC      !")
        print ("!-----------------------------------!")
        print (">")
    else:
             sock.send(mensagem.encode("utf-8"))
             answer = sock.recv(512)

# IRC-server
import socket
import time
import os
import sys
import rsa

portaHost= 65110

chaves = rsa.gera_chaves()
public_key = chaves[0]
private_key = chaves[1]

# requisita API do SO uma conexão AF_INET (IPV4)
#   com protocolo de transporte SOCK_STREAM (TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as c:
    print("Esperando para Conectar no Server...")
    time.sleep(5)
    c.connect((socket.gethostname(), portaHost))

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
           sys.exit()

        elif mensagem == '/clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            print ("!-----------------------------------!")
            print ("!Comandos Suportados:               !")
            print ("!   ?USUARIO (nick, host, nome)     !")
            print ("!       ?SAIR                       !")
            print ("!       ?ENTRAR (canal)             !")
            print ("!       ?LISTAR                     !")
            print ("!       ?SAIRC   (canal)            !")
            print ("!       ?FECHAR                     !")
            print ("!       /clear                      !")
            print ("!+++++++++++++++++++++++++++++++++++!")
            print ("!    Seja Bem vindo ao min-IRC      !")
            print ("!-----------------------------------!")
            print (">")
        else:
                 c.send(mensagem.encode("utf-8"))
                 answer = c.recv(512)
                 print(repr(answer.decode("utf-8")))

# IRC-server
import socket
import time
import os
import sys
import rsa

portaHost= 65046

chaves = rsa.gera_chaves()
c_public_key = chaves[0]
c_private_key = chaves[1]
receivekeys = 0

# requisita API do SO uma conexão AF_INET (IPV4)
#   com protocolo de transporte SOCK_STREAM (TCP)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as c:
    print("Esperando para Conectar no Server...")
    time.sleep(5)
    c.connect((socket.gethostname(), portaHost))

    while 1:
        if (receivekeys==0):
            print("ENVIANDO E RECEBENDO CHAVES")
            mensagem="?PUBK "+repr(c_public_key)
            receivekeys+=1
            c.sendall(mensagem.encode("utf-8"))
            s_public_key = c.recv(1024).decode("utf-8")

            print(s_public_key)
            time.sleep(5)

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
            mensagem = input()

            if mensagem == '/quit':
                c.close()
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
                print ("!       /quit                       !")
                print ("!       /clear                      !")
                print ("!+++++++++++++++++++++++++++++++++++!")
                print ("!    Seja Bem vindo ao min-IRC      !")
                print ("!-----------------------------------!")
                print (">")
            else:
                 c.sendall(mensagem.encode("utf-8"))
                 answer = c.recv(1024).decode("utf-8")
                 print(answer)

# IRC-server
import socket
import time
import os

#HOST = '192.168.1.107' #Endereco IP do Servidor - meu pc"""
#PORT = 65000       #Porta que o Servidor esta
#mensagem = "abobrinha"  # mensagem a ser enviada

portaHost= 65000

    # requisita API do SO uma conexão AF_INET (IPV4)
    #   com protocolo de transporte SOCK_STREAM (TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # processo dorme por 10 segundos para evitar
    #   se conectar com servidor antes desse estar rodando
#time.sleep(5)

    # requisita estabelecimento de conexão
sock.connect((socket.gethostname(), portaHost))
print("Esperando para nonectar no Server")

while 1:
    msg = input()

    mensagem = msg#.split(' ', 1)
    #se o usuário quiser sair sai
    if mensagem == '?SAIR':
       sock.close()
       break
    #se quiser limpar limpa
    elif mensagem == '/clear':
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        # transforma mensagem em bytes e transmite
             sock.send(mensagem.encode("utf-8"))
             print("Cliente enviou mensagem" ,mensagem)
             time.sleep(5)
             answer = sock.recv(512)
             print(answer.decode("utf-8"))

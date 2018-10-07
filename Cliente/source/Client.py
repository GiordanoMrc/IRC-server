# IRC-server
import socket
import time

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
print("fdp")
msg = input()
print(msg)

while 1:

    mensagem = msg.split(' ', 1)
    #se o usuário quiser sair sai
    if mensagem[0] == '?SAIR':
       sock.close()
       break
    #se quiser limpar limpa
    elif mensagem[0] == '/clear':
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        # transforma mensagem em bytes e transmite
        try:
             sock.send(bytes(mensagem, "utf-8"))
             print("Cliente id %d: enviou mensagem" % id)
             time.sleep(1)
             answer = sock.recv(10)
        except: pass


######
if __name__ == '__main__':
    main()

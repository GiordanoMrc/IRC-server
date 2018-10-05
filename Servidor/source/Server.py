# IRC-server
import time
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#definindo uma conexão TCP para a Origem
origem= (HOST,PORT)
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(origem)






def processo1():
    # requisita API do SO uma conexão AF_INET (IPV4)
    #   com protocolo de transporte SOCK_STREAM (TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # processo dorme por 10 segundos para evitar
    #   se conectar com servidor antes desse estar rodando
    time.sleep(10)

    # requisita estabelecimento de conexão
    sock.connect((socket.gethostname(),portaHost))

    while 1:
        # transforma mensagem em bytes e transmite
        sock.send(bytes(mensagem,"utf-8"))
        print("Cliente:", mensagem)
        time.sleep(5)
    return



def main():
    import multiprocessing as mp
    processes[]

    # cria 2 processos, um servidor (processo2) e um cliente (processo1)
    processes += [mp.Process(target=processo2)]
    processes += [mp.Process(target=processo1)]

    # inicia os dois processos (pode olhar no gerenciador de tarefas,
    #    que lá estarão
    for process in processes:
        process.start()

    # espera pela finalização dos processos filhos
    #   (em Sistemas operacionais verão o que isso significa)
    for process in processes:
        process.join()



    return

#end
if __name__ == '__main__':
    main()

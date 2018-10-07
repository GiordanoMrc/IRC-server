import socket
import time

portaHost = 65000 #porta do servidor (fica escutando esperando conexões)
mensagem = "?NICK ze" #mensagem a ser enviada


class ServerClient:
    numClients = 0

    def __init__(self, ipv4, sock, nickname="USR"+str(numClients),realname = "", hostname="", channel=""):
        self.ipv4     = ipv4
        self.sock     = sock
        self.nickname = nickname
        self.hostname = hostname
        self.realname = realname
        self.channel  = channel

        ServerClient.numClients += 1

    def sendMsg(self, msg):
        self.sock.send(msg.encode("utf-8"))
        print(msg)

    def alteraNick(self,msg):
        #input
        #self.nickname
        pass

class ServerChannel:
    def __init__(self, name):
        self.name = name
        self.clients = {}


class ServerApp:

    def __init__(self, portaHost):
        # Cria estruturas para segurar clients e canais
        self.clients = {}
        self.canais   = {}

        self.canais[""] = ServerChannel("")

        # registra handlers para comandos
        self.handlers = {"NICK"   : self.nickClientHandler,
                         "USUARIO": self.newClientHandler,
                         "SAIR"   : self.deleteClientHandler,
                         "ENTRAR" : self.subscribeChannelHandler,
                         "SAIRC"  : self.unsubscribeChannelHandler,
                         "LISTAR" : self.listChannelHandler,
                        }
        # requisita API do SO uma conexão AF_INET (IPV4)
        #   com protocolo de transporte SOCK_STREAM (TCP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # requisita ao SO a posse de uma porta associada a um IP
        self.sock.bind((socket.gethostname(), portaHost))

        # requisita ao SO que a porta indicada de um dado IP seja
        #   reservado para escuta
        self.sock.listen(5)

        # não blocante
        self.sock.setblocking(0)

        self.run()

    def run(self):
        while 1:
            # aceita requisição de conexão do processo 1,
            #   e recebe um socket para o cliente e o
            #   endereço de IP dele
            (clientsock, address) = self.sock.accept()

            while 1:
                # recebe do socket do cliente (processo 1) uma mensagem de 512 bytes
                mensagem_recebida = clientsock.recv(512).decode("utf-8")

                print(mensagem_recebida)

                # processa mensagem
                answer = self.parseCommands(clientsock, address, mensagem_recebida)
                if len(answer) > 0:
                    self.sendMessage(answer)
        pass

    def parseCommands(self, clientsock, clientAddr, mensagem_recebida):
        commands = mensagem_recebida.split('\n') # comandos separados por nova linha
        unrecognized_commands = []
        invalid_parameters = []


        if clientAddr not in self.clients.keys():
            self.clients[clientAddr] = ServerClient(clientAddr, clientsock)
            self.canais[""].clients[clientAddr] = self.clients[clientAddr]

        client = self.clients[clientAddr]


        for command in commands:
            comm_n_args = command.split(' ')
            if comm_n_args[0][0] is '?':
                if comm_n_args[0][1:] in self.handlers.keys():
                    ans = self.handlers[comm_n_args[0][1:]](clientAddr, comm_n_args[1:])
                    if len(ans) > 0:
                        invalid_parameters += ans
                else:
                    unrecognized_commands += comm_n_args[0]
            else:
                self.sendMsgChannel(command, client.channel)

        answer = ""
        if len(unrecognized_commands) > 0:
            answer += "Unrecognized commands: %s" % unrecognized_commands
        if len(invalid_parameters) > 0:
            answer += "Invalid parameters: %s\n" % invalid_parameters

        return answer

    def sendMsgChannel(self, msg, channel):
            for client in self.canais[channel].clients:
                self.clients[client].sendMsg(msg)

    def nickClientHandler(self, clientAddr, nick):
            for client in self.clients:
                if (nick == self.clients[client].nickname):
                    self.clients[client].alteraNick("Já existe esse nick")
                    return ("lixo")
                else:
                    self.clients[clientAddr].nickname= nick
                    return ("ok")


    def newClientHandler(self, clientAddr, args):
        pass

    def deleteClientHandler(self, clientAddr, args):
        pass

    def subscribeChannelHandler(self, clientAddr, args):
        pass

    def unsubscribeChannelHandler(self, clientAddr, args):

        pass

    def listChannelHandler(self, clientAddr, args):
        for canal in self.canais:
            nomeCanal = self.canais[canal].name
            self.clients[clientAddr].sendMsg(nomeCanal)
        return ("ok")

def processo1():
     #requisita API do SO uma conexão AF_INET (IPV4)
    #  com protocolo de transporte SOCK_STREAM (TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # processo dorme por 10 segundos para evitar
    #   se conectar com servidor antes desse estar rodando
    time.sleep(5)

    # requisita estabelecimento de conexão
    sock.connect((socket.gethostname(),portaHost))

    while 1:
        # transforma mensagem em bytes e transmite
        try:
            sock.send(mensagem.encode(encoding="utf-8"))
            #print("Cliente:", mensagem)
            time.sleep(5)
        except: pass
    return


def processo2():
    #Cria servidor e escuta clients
    serv = ServerApp(portaHost)
    pass

def main():
    import multiprocessing as mp
    processes = []

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

# Para evitar dar pau com multiprocessos em python,
#   sempre colocar essa guarda, que evita processos filhos
#   de executarem a o conteúdo da função
if __name__ == '__main__':
    main()

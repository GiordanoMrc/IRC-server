import ServerCliente
import socket
#import ServerCanais

portaHost= 65000

class ServerCanal:
    def __init__(self, name):
        self.name = name
        self.clients = {}


class ServerApp:

    def __init__(self):
        # Cria estruturas para segurar clients e canais
        self.clients = {}
        self.canais   = {}

        self.canais["canal"] = ServerCanal("canal")

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
        self.sock.listen(10)

        # não blocante
        self.sock.setblocking(0)

        self.run()

    def run(self):
        while 1:
            # aceita requisição de conexão do processo 1,
            #   e recebe um socket para o cliente e o
            #   endereço de IP dele
            try:(clientsock, address) = self.sock.accept()
            except: pass

            while 1:
                # recebe do socket do cliente (processo 1) uma mensagem de 512 bytes
                try:
                    mensagem_recebida = clientsock.recv(512).decode("utf-8")
                    print(mensagem_recebida)
                    if not mensagem_recebida:
                        break
                    answer = self.parseCommands(clientsock, address, mensagem_recebida)
                    if len(answer) > 0:
                        self.sendMessage(answer)
                except: pass
        pass

    def parseCommands(self, clientsock, clientAddr, msg):
        mensagem_recebida = msg.split('\n') # comandos separados por nova linha
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
                        invalid_parameters.append(ans)
                else:
                    unrecognized_commands += comm_n_args[0]
            else:
                self.sendMsgChannel(command, client.channel)

        answer = []
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

    def closeServer(self):
        self.sock.close()

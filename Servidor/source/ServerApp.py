import ServerCliente
import socket
#import ServerCanais

portaHost= 65001

class ServerCanal:
    def __init__(self, name):
        self.name = name
        self.clients = {}


class ServerApp:

    def __init__(self):
        # Cria estruturas para segurar clients e canais
        self.clients = {}
        self.canais   = {}

        self.canais["canal1"] = ServerCanal("canal1")

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


    def run(self):
        while 1:
            # aceita requisição de conexão do processo 1,
            #   e recebe um socket para o cliente e o
            #   endereço de IP dele
            clientsock, address = self.sock.accept()


            while 1:
                # recebe do socket do cliente (processo 1) uma mensagem de 512 bytes
                    mensagem_recebida = clientsock.recv(512).decode("utf-8")
                    answer = self.parseCommands(clientsock, address, mensagem_recebida)
                    if len(answer) > 0:
                        for Erro in answer:
                            for item in Erro:
                                self.sendMsgChannel((self.clients[address].nickname + ". %s" %(item)), self.clients[address].channel)
        pass


    def parseCommands(self, clientsock, clientAddr, msg):
        mensagem_recebida = msg.split('\n') # comandos separados por nova linha
        unrecognized_commands = []
        invalid_parameters = []


        if clientAddr not in self.clients.keys():
            self.clients[clientAddr] = ServerCliente.Cliente(clientAddr, clientsock, "","","","")
            self.canais["canal1"].clients[clientAddr] = self.clients[clientAddr]
            self.clients[clientAddr].channel = "canal1"

        for command in mensagem_recebida:
            comm_n_args = command.split(' ')
            if comm_n_args[0][0] is '?':
                if comm_n_args[0][1:] in self.handlers.keys():
                    ans = self.handlers[comm_n_args[0][1:]](clientAddr, comm_n_args[1:])
                    if len(ans) > 0:
                        invalid_parameters.append(ans)
                else:
                    unrecognized_commands.append("Unrecognized Command:" + comm_n_args[0][1:])
            else:
                if (self.clients[clientAddr].nickname == ""):
                    invalid_parameters.append('Você precisa de um nick')
                else:
                    self.sendMsgChannel((self.clients[clientAddr].nickname + ": %s" % (command)), self.clients[clientAddr].channel)

        answer = []
        if len(unrecognized_commands) > 0:
            answer.append(unrecognized_command)
        if len(invalid_parameters) > 0:
            answer.append(invalid_parameters)

        return answer

    def closeServer(self):
        self.sock.close()

    def sendMsgChannel(self, msg, channel):
            for client in self.canais[channel].clients:
                self.clients[client].sendMsg(channel + "~%s" %(msg))

    def nickClientHandler(self, clientAddr, args):
            for client in self.clients:
                if (args[0] == self.clients[client].nickname):
                    return "Já existe esse nick"
                else:
                    self.clients[clientAddr].nickname= args[0]

            self.sendMsgChannel("ok", self.clients[clientAddr].channel)
            return ""

    def newClientHandler(self, clientAddr, args):

        pass

    def deleteClientHandler(self, clientAddr, args):
        pass

    def subscribeChannelHandler(self, clientAddr, args):
        pass

    def unsubscribeChannelHandler(self, clientAddr, args):

        pass

    def listChannelHandler(self, clientAddr, channel):
        self.sendMsgChannel("listando canais:\n", self.clients[clientAddr].channel)
        for canal in self.canais:
            self.sendMsgChannel(channel + ": %d" (len(self.canais[channel].clients)), self.clients[clientAddr].channel)
        return ("ok")

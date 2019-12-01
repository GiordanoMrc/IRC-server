import socket
import os
import sys
import rsa


class Cliente:
    numClients = 0
    def __init__(self, ipv4, sock, nickname,realname, hostname, channel):
        self.ipv4     = ipv4
        self.sock     = sock
        self.nickname = nickname
        self.hostname = hostname
        self.realname = realname
        self.channel  = channel

        Cliente.numClients += 1

    def sendMsg(self, msg):
        self.sock.send(msg.encode("utf-8"))
        print(msg)


class ServerCanal:
    def __init__(self, name):
        self.name = name
        self.clients = {}


class ServerApp:

    def __init__(self, portaHost):
        self.clients = {}
        self.canais   = {}
        #self.handlers = {}
        self.canais["canal-default"] = ServerCanal("canal-default")

        # registra handlers para comandos
        self.handlers = {"NICK"   : self.nickClientHandler,
                         "USUARIO": self.newClientHandler,
                         "SAIR"   : self.deleteClientHandler,
                         "ENTRAR" : self.subscribeChannelHandler,
                         "SAIRC"  : self.unsubscribeChannelHandler,
                         "LISTAR" : self.listChannelHandler,
                         "FECHAR" : self.closeServer
                        } # Não mexer
        # requisita API do SO uma conexão AF_INET (IPV4)
        #   com protocolo de transporte SOCK_STREAM (TCP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), portaHost))
        self.sock.listen(10)

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print ("!-----------------------------------!")
        print ("!Bem Vindo ao min-IRC:              !")
        print ("!       Pode Falar!                 !")
        print ("!-----------------------------------!")

        while 1:
            clientsock, address = self.sock.accept()
            while 1:
                try:
                    mensagem_recebida = clientsock.recv(512).decode("utf-8")
                    if not mensagem_recebida:
                        break
                    answer = self.parseCommands(clientsock, address, mensagem_recebida)
                    if len(answer) > 0:
                        for Erro in answer:
                            for item in Erro:
                                self.sendMsgChannel((self.clients[address].nickname + ". %s" %(item)), self.clients[address].channel)
                except:
                    pass
        pass


    def parseCommands(self, clientsock, clientAddr, msg):
        commands = msg.split('\n') # comandos separados por nova linha
        unrecognized_commands = []
        invalid_parameters = []


        if clientAddr not in self.clients.keys():
            self.clients[clientAddr] = Cliente(clientAddr, clientsock,"","","","")  #mudei!
            self.canais["canal-default"].clients[clientAddr] = self.clients[clientAddr]
            self.clients[clientAddr].channel = "canal-default"


        client = self.clients[clientAddr]

        for command in commands:
            comm_n_args = command.split(' ')
            if comm_n_args[0][0] is '?':
                if comm_n_args[0][1:] in self.handlers.keys():
                    ans = self.handlers[comm_n_args[0][1:]](clientAddr, comm_n_args[1:])
                    if len(ans) > 0:
                        invalid_parameters.append(ans)
                else:
                        unrecognized_commands.append("Unrecognized Command:" + comm_n_args[0][1:]) # verifica se é comando ou não
            else:
                if (self.clients[clientAddr].nickname == ""):
                    invalid_parameters.append('Você precisa de um nick para enviar mensagens.')
                else:
                    self.sendMsgChannel((self.clients[clientAddr].nickname + ": %s" % (command)), self.clients[clientAddr].channel)

        answer = []
        if len(unrecognized_commands) > 0:
            answer.append(unrecognized_commands)
        if len(invalid_parameters) > 0:
            answer.append(invalid_parameters)

        return answer

    def closeServer(self):
        self.sock.close()
        sys.exit()

    def sendMsgChannel(self, msg, channel):
            for client in self.canais[channel].clients:
                self.clients[client].sendMsg(channel + "~%s" %(msg))

    def nickClientHandler(self, clientAddr, args):
            for client in self.clients:
                if (args[0] == self.clients[client].nickname):
                    return "Já existe esse nick"
                else:
                    self.clients[clientAddr].nickname= args[0]
            self.sendMsgChannel("Agora você tem um Nick!", self.clients[clientAddr].channel)
            pass

    def newClientHandler(self, clientAddr, usr):
        for client in self.clients:
            if usr[0] == self.clients[client].nickname:
                return "Usuario já cadastrado"
        self.clients[clientAddr].nickname = usr[0]
        self.clients[clientAddr].hostname = usr [1]
        self.clients[clientAddr].realname = usr [2]
        self.sendMsgChannel("Bem vindo:%s  a.k.a  " %(usr[2]) +"%s" %usr[0], self.clients[clientAddr].channel )
        return ""

    def deleteClientHandler(self, clientAddr, args):
        if clientAddr in self.clients.keys():
            self.sendMsgChannel("Usuario "+ self.clients[clientAddr].nickname +" saiu.", self.clients[clientAddr].channel)
            del(self.clients[clientAddr])
        else:
            return "Usuario não encontrado."

        return ""

    def subscribeChannelHandler(self, clientAddr, newChannel):
        if newChannel[0] not in self.canais.keys():
            self.canais[newChannel[0]] = ServerCanal(newChannel[0])

        self.canais[newChannel[0]].clients[clientAddr] = self.clients[clientAddr]
        self.clients[clientAddr].channel = newChannel[0]
        self.sendMsgChannel("Foi criado!", self.clients[clientAddr].channel)

        return ""

    def unsubscribeChannelHandler(self, clientAddr, leftChannel):
        for client in self.clients:
            if leftChannel[0] not in self.canais.keys():
                return "Esse canal não existe"
            if leftChannel[0] == self.clients[client].channel:
                del(self.canais[leftChannel[0]].clients[clientAddr])
                self.clients[client].channel = "canal-default"
            else:
                return "você Não está no Canal"

        self.sendMsgChannel("Você saiu.",self.clients[clientAddr].channel)
        return ""

    def listChannelHandler(self, clientAddr, arg):
        self.sendMsgChannel("listagem:", self.clients[clientAddr].channel)
        for channel in self.canais:
            self.sendMsgChannel("!  %d)" %(len(self.canais[channel].clients))+ channel, self.clients[clientAddr].channel)
        return ""

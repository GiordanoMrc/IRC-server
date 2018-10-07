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
        self.clients = {}
        self.canais   = {}
        self.handlers = {}
        self.canais["canal1"] = ServerCanal("canal1")

        # registra handlers para comandos
        self.handlers['baseHandlers'] = {"NICK"   : self.nickClientHandler,
                         "USUARIO": self.newClientHandler,
                         "SAIR"   : self.deleteClientHandler,
                         "ENTRAR" : self.subscribeChannelHandler,
                         "SAIRC"  : self.unsubscribeChannelHandler,
                         "LISTAR" : self.listChannelHandler,
                        }
        # requisita API do SO uma conexão AF_INET (IPV4)
        #   com protocolo de transporte SOCK_STREAM (TCP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((socket.gethostname(), portaHost))
        self.sock.listen(10)

    def run(self):
        print ("!--------------------!")
        print ("!Comandos Suportados:!")
        print ("!       ?USUARIO     !")
        print ("!       ?SAIR        !")
        print ("!       ?ENTRAR      !")
        print ("!       ?LISTAR      !")
        print ("!       ?SAIRC       !")
        print ("!--------------------!")
        while 1:
            clientsock, address = self.sock.accept()
            while 1:
                    mensagem_recebida = clientsock.recv(512).decode("utf-8")
                    #if not mensagem_recebida:
                        #break
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
                if comm_n_args[0][1:] in self.handlers['baseHandlers'].keys():
                    ans = self.handlers['baseHandlers'][comm_n_args[0][1:]](clientAddr, comm_n_args[1:])
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
            answer.append(unrecognized_commands)
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

    def newClientHandler(self, clientAddr, usr):
        for client in self.clients:
            if usr[0] == self.clients[client].nickname:
                return "Usuario já cadastrado"
        self.clients[clientAddr].nickname = usr[0]
        self.clients[clientAddr].hostname = usr [1]
        self.clients[clientAddr].realname = usr [2]
        self.sendMsgChannel("Bem vindo:%s  a.k.a  " %(usr[2]) +"%s" %usr[0], self.clients[clientAddr].channel )
        return("ok")

    def deleteClientHandler(self, clientAddr, args):
        if clientAddr in self.clients.keys():
            self.sendMsgChannel("Usuario "+ self.clients[clientAddr].nickname +" saiu.", self.clients[clientAddr].channel)
            del(self.clients[clientAddr])
        else:
            return "Usuario não encontrado."

        return("ok")

    def subscribeChannelHandler(self, clientAddr, newChannel):
        if newChannel[0] not in self.canais.key():
            self.canais[channel[0]] = ServerCanal(newChannel[0])

        self.canais[newChannel[0]].clients[clientAddr] = self.clients[clientAddr]
        self.clients[clientAddr].channel = newChannel[0]
        self.sendMsgChannel("Entrou", self.clients[clientAddr].channel)

        return("ok")

    def unsubscribeChannelHandler(self, clientAddr, leftChannel):
        for client in self.clients:
            if leftChannel[0] not in self.canais.keys():
                return "Esse canal não existe"
            if leftChannel[0] == self.clients[client].channel:
                del(self.canais[leftChannel[0]].clients[clientAddr])
                self.clients[client].channel = "canal1"
            else:
                return "você Não está no Canal"

        self.sendMsgChannel("Você saiu.",self.clients[clientAddr].channel)
        return("ok")

    def listChannelHandler(self, clientAddr, arg):
        self.sendMsgChannel("lista de canais:\n", self.clients[clientAddr].channel)
        for channel in self.canais:
            self.sendMsgChannel("!  %d)" %(len(self.canais[channel].clients))+ channel, self.clients[clientAddr].channel)
        return ("")

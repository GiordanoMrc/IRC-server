import ServerApp
import socket


class ServerCliente:
    def __init__(self, ipv4, sock, nickname,realname, hostname, canal):
        self.ipv4     = ipv4
        self.sock     = sock
        self.nickname = nickname
        self.hostname = hostname
        self.realname = realname
        self.channel  = channel

        #ServerClient.numClients += 1

    def sendMsg(self, msg):
        self.sock.send(msg.encode("utf-8"))
        print(msg)

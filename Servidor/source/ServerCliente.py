import ServerApp
import socket


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

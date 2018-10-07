import socket
import time

class ServerChannel:
    def __init__(self, name):
        self.name = name
        self.clients = {}

#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import *
from SocketServer import *

HOST = ''
PORT = 8009
userlist = []
namelist = []
addr = (HOST, PORT)

def now():
    return ctime(time())

def welcome():
    return '''Bem-Vindo ao CHAT-SERVER
    Hora Local: %s, %i usuário(s) online:%s
    ''' %(now(), len(userlist), repr(namelist))
    

class ClientHandler(BaseRequestHandler):
    def handle(self):
        userlist.append(self.request)
        self.setnick()
        sleep(3)
        print self.connection()
        self.request.send(welcome())
        self.broadcast(self.connection())
        
        print '[%i usuários online]\n' % len(userlist)
        
        while True:
            try:
                data = self.request.recv(1024)
                print '%s(%s): "%s"' % (self.nickname, self.client_address[0], data)
                outgoing = '%s: %s' % (self.nickname, data)
                self.broadcast(outgoing)
                
            except:
                print self.disconnection()
                userlist.remove(self.request)
                namelist.remove(self.nickname)
                self.broadcast(self.disconnection())
                self.request.close()
                print '[%i usuários(s) online]\n' % len(userlist)
                
                return
        
    def broadcast(self, data):
        for user in userlist:
            user.send(data)
    
    def disconnection(self):
        return '(%s)%s Desconectado de %s\n' % (self.nickname, self.client_address[0], now())
    
    def connection(self):
        return '(%s)%s Conectado em %s\n' % (self.client_address[0], self.nickname, now())
    
    def setnick(self):
        self.request.send('Informe ser nome!')
        self.nickname = self.request.recv(1024)
        self.request.send('Bem-Vindo, %s!\n' % self.nickname)
        namelist.append(self.nickname)

server = ThreadingTCPServer(addr, ClientHandler)

if __name__ == '__main__':
    print welcome()
    print 'Servidor Inicializado. Aguardando Conexões na Porta %i...\n' % PORT
    server.serve_forever()

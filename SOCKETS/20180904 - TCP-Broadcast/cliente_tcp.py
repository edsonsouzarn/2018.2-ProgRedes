#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
import thread, time

def recvMsg(sock):
    while True:
        recvmsg = sock.recv(1024)
        print '<Servidor>>> ' + recvmsg

if __name__ == '__main__':
    host = raw_input('HOST(default:localhost): ')
    port = raw_input('PORT(default:8008): ')
    
    host = host if (len(host) > 0) else 'localhost'
    port = int(port) if (len(port) > 0) else 8008
    
    try:
        s = socket(AF_INET, SOCK_STREAM) 
        s.connect((host, port))
        
        thread.start_new_thread(recvMsg, (s, )) 
        
        time.sleep(1)
        nickmsg = raw_input('Seu Nome: ')
        s.send(nickmsg)
        
        time.sleep(2)
        print 'Aguarde!...'
        
        while True:
            sendmsg = raw_input(' - Enviou: ')
            if sendmsg == 'sair()':
                break
            s.send(sendmsg)
        
        s.close()
    except:
        print 'IP Errado!'

    raw_input('Saindo do Cliente (Pressione uma Tecla!)')

#!/usr/bin/python3

import socket

HOST = ''
PORT = 5001

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind((HOST, PORT))
tcp_socket.listen(1)

print('Aguardando conexão')

while True:
   lista_msg_servidor = []
   con, cliente = tcp_socket.accept()
   print('Conectado por: ', cliente)
   while True:
      msg = con.recv(1024)
      if not msg: break
      msg_serv = 'O cliente {0} disse: {1}'.format(cliente, msg.decode('utf-8'))
      print(msg_serv)
      lista_msg_servidor.append(msg_serv)
      con.send(msg_serv.encode('utf-8'))

   print('Finalizando conexão do cliente ', cliente)


   print(' ')
   print('----------------------------------------------------------')
   print('Historico das Mensagens do Cliente ',cliente)
   for i in range(0, len(lista_msg_servidor)):
       print(lista_msg_servidor[i])
   print('----------------------------------------------------------')

   con.close()

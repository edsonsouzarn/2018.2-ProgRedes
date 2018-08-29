#!/usr/bin/python3

import socket

HOST = '10.20.1.6'
PORT = 5001

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT))

print('Para sair use CTRL+X\n')

msg_received = ''
msg_input = input('Digite a mensagem: ')

while msg_input != '\x18':
   msg_sended = msg_input.encode('utf-8')
   tcp_socket.send(msg_sended)
   msg_received = tcp_socket.recv(1024)
   print(msg_received.decode('utf-8'))
   msg_input = input('Digite a mensagem: ')

tcp_socket.close()

#!/usr/bin/env python3
#!C:\Users\pains\AppData\Local\Programs\Python\Python311\

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address      #Cliente servidor en la misma maquina
PORT = 65432  # The port used by the server,para poder usar un puerto restringido es necesario ejecutar como admin
buffer_size = 1024
#socket.socket(Family, type, proto)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket: # Un socket debe ser abierto y cerrado, con "with" se hace amnbas (open y close)
    TCPClientSocket.connect((HOST, PORT)) #.conect(adress) /El cliente espera a que reciba, pero si lo sobrepasa en tiempo puede generar error, recomendable poner trycatch
    print("Enviando mensaje...")
    TCPClientSocket.sendall(b"Hello TCP server") #Parametro en bits
    print("Esperando una respuesta...")
    data = TCPClientSocket.recv(buffer_size) #recv detiene el proceso hasta que reciba algun dato
    print("Recibido,", repr(data), " de", TCPClientSocket.getpeername()) #Saber que llega y de quien llega
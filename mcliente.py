import socket
import os
from time import time

HOST = input("IP destino: ")
PORT = int(input("Puerto: "))
buffer_size = 1024
casilla1 = ''       #Variables para asignar
casilla2 = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    tiempo_inicial= time()
    print("Conectando con el servidor...")
    clientSocket.connect((HOST,PORT))           #Conexion con el servidor
    print("-Servidor conectado-")
    #Escogiendo dificultad
    dificultad = input("--MENU--\n1.- Facil\n2.- Dificil\nRespuesta: ")  #Se guarda la dificultad en la variable
    clientSocket.send(dificultad.encode('utf8'))                         #Envia el valor de dificultad codificado a bytes usando utf8 Los sockets solo transmiten bytes y
    os.system("cls")
    if dificultad == '1':
        limite = 3
    else:                                               #Establece limites de tamaño de nxn de las cartas del tablero
        limite = 5
    
    while True:
        data = clientSocket.recv(buffer_size).decode('utf8')                #r1 recibimos la opcion que manda el servidor
        if data == '1' or data == '2':                                      #Valor que determina quien gana
            break
        elif data == '3':                                                   #Turno del pc
            clientSocket.send('hola4'.encode('utf8'))                    #envio de cualquier cosa para continuar turno
            data = clientSocket.recv(buffer_size).decode('utf8')            #R2 recibe el tablero decodifica la informacion con el tamaño de buffer y la imprime
            print(data)
            input('Presione enter...')
            os.system('cls')
            clientSocket.send('hola3'.encode('utf8'))                    #Envio 3

        elif data=='4':                                                     #Turno del jugador
            print('-Tu turno-')
            clientSocket.send('hola4'.encode('utf8'))                    #envio de cualquier cosa para continuar turno
            print('Turno del jugador\n')
            data = clientSocket.recv(buffer_size).decode('utf8')            #R2 recibe el tablero actual
            print(data)
            while True:
                casilla1 = input('Seleccione la casilla 1 (Y,X): ')
                aux = casilla1.split(',')
                if (int(aux[0]) <= limite) and (int(aux[1]) <= limite):     #if para salir del while para seleccionar la casilla
                    break
                
            clientSocket.send(casilla1.encode('utf8'))                      #Enviar la primer tirada E3
            data = clientSocket.recv(buffer_size).decode('utf8')            #R4 recibe el tablero destapado de la primer tirada
            os.system('cls')
            print(data)
            while True:
                casilla2 = input('Seleccione la casilla 2 (Y,X): ')
                aux = casilla2.split(',')
                if (int(aux[0]) <= limite) and (int(aux[1]) <= limite):     #if para salir del while para seleccionar la casilla
                    break

            clientSocket.send(casilla2.encode('utf8'))                      #Envia la segunda tirada E5
            data = clientSocket.recv(buffer_size).decode('utf8')            #R6 recibe el tablero de la segnuda tirada
            os.system('cls')
            print(data)
            input('Presiona enter..')
            clientSocket.send('siuu'.encode('utf8'))                        #E7 Envia cualquier cosa para recibir resultado
            os.system('cls')
            data = clientSocket.recv(buffer_size).decode('utf8')            #R8 Recibe el tablero con el resultado
            print(data)
            input("Enter para continuar..")
            clientSocket.send("hola".encode('utf8'))                        #E9 Envia cualquier cosa para continuar con el turno
            os.system("cls")

    tiempo_final= time()
    tiempo_partida= tiempo_final-tiempo_inicial
    if data == '1':
        print("!!EL JUGADOR GANA!!")                                      #Valor de data que manda el servidor determinando el ganador
        print("Tiempo de partida: ",tiempo_partida)
    else:
        print("LA PC GANA")
        print("Tiempo de partida: ", tiempo_partida)
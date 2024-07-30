import socket
import os

HOST = input("Ingrese una direccion IP destino: ")
PORT = int(input("Ingrese un numero de puerto valido: "))
buffer_size = 1024
casilla1 = ''
casilla2 = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    print("Conectando con el servidor...")
    clientSocket.connect((HOST,PORT))
    print("-Servidor conectado-")

    dificultad = input("--MENU--\n1.- Facil\n2.- Dificil\nRespuesta: ")
    clientSocket.send(dificultad.encode('utf8'))
    os.system("cls")
    if dificultad == '1':
        limite = 3
    else:
        limite = 5
    
    while True:
        data = clientSocket.recv(buffer_size).decode('utf8')
        if data == '1' or data == '2':
            break
        elif data == '3':
            clientSocket.send('hola4'.encode('utf8'))
            data = clientSocket.recv(buffer_size).decode('utf8')
            print(data)
            input('Presione enter...')
            os.system('cls')
            clientSocket.send('hola3'.encode('utf8'))

        elif data=='4':
            print('---Tu turno---')
            clientSocket.send('hola4'.encode('utf8'))
            print('Turno del jugador\n\n')
            data = clientSocket.recv(buffer_size).decode('utf8')
            print(data)
            while True:
                casilla1 = input('Seleccione la casilla 1(Y,X): ')
                aux = casilla1.split()
                if (int(aux[0]) <= limite) and (int(aux[1]) <= limite):
                    break
                
            clientSocket.send(casilla1.encode('utf8'))
            data = clientSocket.recv(buffer_size).decode('utf8')
            os.system('cls')
            print(data)
            while True:
                casilla2 = input('Seleccione la casilla 2(Y,X): ')
                aux = casilla2.split(',')
                if (int(aux[0]) <= limite) and (int(aux[1]) <= limite):
                    break

            clientSocket.send(casilla2.encode('utf8'))
            data = clientSocket.recv(buffer_size).decode('utf8')
            os.system('cls')
            print(data)
            input('Presione enter..')
            clientSocket.send('siuu'.encode('utf8'))
            os.system('cls')
            data = clientSocket.recv(buffer_size).decode('utf8')
            print(data)
            input("Enter para continuar TURNO..")
            clientSocket.send("hola".encode('utf8'))
            os.system("cls")


    if data == '1':
        print("!!EL JUGADOR GANA!!")                                    
    else:
        print("LA PC GANA")
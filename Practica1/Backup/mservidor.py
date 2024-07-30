import socket
import random
import os
import time
import struct

class jugador:
    puntos = 0                                        #self para acceder a los atributos
    def __init__(self,pancho):                        #requiere init para una clase
        self.pancho = pancho

class memorama:
    def __init__(self, dificultad):
        self.dificultad = dificultad
        if dificultad == "1":
            self.tablero = [['gato','cabra','niños','vaca'],
            ['viento','niños','pasto','viento'],
            ['silbato','vaca','gato','perro'],
            ['perro','pasto','cabra','silbato']]
            self.tablero_oculto = [['*','*','*','*'],
            ['*','*','*','*'],
            ['*','*','*','*'],
            ['*','*','*','*']]
            self.cont = 8                                              #Contador de parejas posibles
            print("Dificultad principiante")
        elif dificultad == "2":
            self.tablero = [['molino','tarea','fuego','uva','lapiz','zapatos'],
            ['tabaco','rollo','flor','grupo','fuego','cazar'],
            ['cargador','cerillo','planta','cazar','torre','uva'],
            ['arco','zapatos','molino','arbol','tarea','lapiz'],
            ['arbol','alien','rollo','cargador','cerillo','torre'],
            ['tabaco','grupo','flor','planta','alien','arco']]
            self.tablero_oculto = [['*','*','*','*','*','*'],
            ['*','*','*','*','*','*'],
            ['*','*','*','*','*','*'],
            ['*','*','*','*','*','*'],
            ['*','*','*','*','*','*'],
            ['*','*','*','*','*','*']]
            self.cont = 18                                              #Contador de parejas posibles
            print("Dificultad avanzada")
        else:
            print("Es otra cosa rara: ",dificultad)
    def mostrar_tablero(self):
        for i in self.tablero_oculto:                                   #mostrar tablero
            print(i)

    def turno_jugador(self,socket,jugador):
        socket.send('4'.encode('utf8'))                                 #E1 Envia el valor de turno del jugador    4 TURNO DEL JUGADOR
        socket.recv(1024).decode('utf8')
        game.enviar_tablero(Client_conn)                                #E2 Envia el tablero actual
        tirada1 = socket.recv(1024).decode('utf8').split(',')           #R3 Recibe la primer tirada
        print("Tirada 1")
        x1 = int(tirada1[0])
        y1 = int(tirada1[1])
        self.tablero_oculto[x1][y1] = self.tablero[x1][y1]
        self.enviar_tablero(socket)                                     #E4 Envia el tablero con la primer casilla destapada
        tirada2 = socket.recv(1024).decode('utf8').split(',')           #R5 Recibe la segunda tirada
        print("Tirada 2")
        x2 = int(tirada2[0])
        y2 = int(tirada2[1])
        self.tablero_oculto[x2][y2] = self.tablero[x2][y2]              #asigna del tablero no oculto al oculto las casiilas para mostrar
        self.enviar_tablero(socket)                                     #E6 Envia el tablero destapando la segunda casilla

        if self.tablero[x1][y1] != self.tablero[x2][y2]:
            self.tablero_oculto[x1][y1] = '*'
            self.tablero_oculto[x2][y2] = '*'
        else:
            self.cont -= 1                                              #Reduce el contador de parejas
            jugador.puntos += 1
        socket.recv(1024).decode('utf8')                                #R7 recive cualquier cosa para enviar el resultado
        self.enviar_tablero(socket)                                     #E8 Envia el tablero con el resultado destapado si son iguales o tapando si son diferentes
        socket.recv(1024).decode('utf8')                                #R9 Recibe cualquier cosa para terminar el turno
        print("Termina el turno")
        

    def tirada_pc(self, jugador, conn):
        while True and self.cont != 0:                                  #mientras existan parejas
            while True:
                try:
                    if self.dificultad == "1":
                        x1 = x2 = random.randrange(0,4)
                        y1 = y2 = random.randrange(0,4)
                    else:
                        x1 = x2 = random.randrange(0,5)
                        y1 = y2 = random.randrange(0,5)
                    if self.tablero_oculto[x1][y1] != '*':
                        x1 = int("/")
                    self.tablero_oculto[x1][y1] = self.tablero[x1][y1]  #Asignacion del tablero actual al oculto
                    break
                except ValueError:
                    pass
                except IndexError:
                    pass

            while ((x1 == x2) and (y1 == y2)):
                while True:
                    try:
                        if self.dificultad == "1":
                            x2 = random.randrange(0,4)
                            y2 = random.randrange(0,4)
                        else:
                            x2 = random.randrange(0,6)
                            y2 = random.randrange(0,6)
                        if self.tablero_oculto[x2][y2] != '*':
                            x2 = int("/")
                        self.tablero_oculto[x2][y2] = self.tablero[x2][y2]
                        break
                    except ValueError:
                        pass
                    except IndexError:
                        pass
            conn.send('3'.encode('utf8'))                                   #E1 envia que es turno del pc      3
            conn.recv(1024).decode('utf8')
            self.enviar_tablero(conn)                                       #E2  Envia el tablero despues de la tirada del pc
            conn.recv(1024)                                                 #Espera a recibir cualquier cosa para enviar el resultado R3
            if self.tablero[x1][y1] != self.tablero[x2][y2]:                #oculta dos posiciones en un tablero si sus valores son diferentes (No atino al par)
                self.tablero_oculto[x1][y1] = '*'
                self.tablero_oculto[x2][y2] = '*'
                break
            else:
                self.cont -= 1                                              #Reduce el numero de parejas
                jugador.puntos += 1
            self.enviar_tablero(conn)                                       #Envia el tablero con el resultado E4
            print('tirada pc')


    def enviar_tablero(self,socket_oirgen):
        text = self.tablero_oculto.__str__().replace('], [','\n').replace('[[','').replace(']]','')
        socket_oirgen.send(text.encode('utf8'))



if __name__ == "__main__":
    HOST = input("IP servidor: ")
    PORT = int(input("Puerto: "))
    buffer_size = 8
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((HOST, PORT))
        while True:
            serverSocket.listen()           #Escuchando cliente
            print("El servidor está disponible y en espera de solicitudes")

            Client_conn, Client_addr = serverSocket.accept()               #Esperando a una conexion para establecer, conn establece un objeto tipo socket recien conectado
            with Client_conn:
                pc = jugador("pc")
                player = jugador("player")
                print("Conectado a", Client_addr)
                                            #definiendo dificultad
                data = Client_conn.recv(1024).decode('utf8') 
                                            #Creando juego con la dificultad como parametro
                game = memorama(data)
                                            #game.mostrar_tablero()
                i = 1
                while game.cont:            #mientras exista valor, si es 0 se toma como false y sale
                    i = 1 - i                   
                    if i == 0:
                                            #turno del jugador
                        print('jugador: {}'.format(player.puntos))
                        game.turno_jugador(Client_conn,player)
                    else:
                                            #turno de la pc
                        print('pc: {}'.format(pc.puntos))
                        game.tirada_pc(pc, Client_conn)
                if player.puntos > pc.puntos:
                    Client_conn.send('1'.encode('utf8'))
                    
                else:
                    Client_conn.send('2'.encode('utf8'))
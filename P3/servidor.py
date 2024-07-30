import socket
import threading
import memorama
import logging


logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)  #configura el registro login para mostrar mensajes de depuracion
MAIN_THREAD = threading.current_thread()                                            #metodo para obtener el objeto del hilo donde se ejecuta el programa(referenciar)

lista_conexiones = []
IP_SERV = input("Direccion del servidor: ")
PORT_SERV = int(input("Puerto: "))
address_server = (IP_SERV, PORT_SERV)

LIMITE_JUGADORES = int(input("Introduzca el numero total de jugadores: "))      #Obtencion de dificultad y numero de jugadores
dificultad = input("---DIFICULTAD--\n1.-Facil\n2.-Dificil\nEnter: ")
game = memorama.memorama(dificultad)


def cerrar_servidor(lista_conexiones):          #mensaje de cerrar servior a todos los jugadores
    msg_to_all(lista_conexiones, 'exit')
    msg_to_all(lista_conexiones, 'exit')
    msg_to_all(lista_conexiones, 'exit')


def msg_to_all(lista_conexiones, msg):              #envia un mensaje a todos los jugadores.
    for conexion in lista_conexiones:
        try:
            conexion.send('\n'.encode('utf-8'))
            conexion.send(msg.encode('utf-8'))
        except:
            lista_conexiones.remove(conexion)


def aceptar_jugadores(socket, lista_conexiones, LIMITE_JUGADORES, jugadores):  # Acepta todas las conexiones necesarias
    id = 1
    nombre_jugador = 'JUGADOR '
    while len(lista_conexiones) < LIMITE_JUGADORES:
        try:
            conn, addr = socket.accept()
            print('Conectado a ', addr)
            jugador = memorama.memorama_jugador(nombre_jugador + str(id) + '->' + str(addr[0]))
            id += 1
            jugadores.append(jugador)  # Se agrega a la lista jugadores el id ip

            msg = 'Bienvenido: ' + jugador.nombre + '\n'
            conn.send(msg.encode('utf-8'))

            lista_conexiones.append(conn)
            text = 'Jugadores conectados: ' + str(len(lista_conexiones)) + '/' + str(LIMITE_JUGADORES)
            msg_to_all(lista_conexiones=lista_conexiones, msg=text)             #Envio de mensaje del numero de jugadores
        except:
            pass


def manejo_jugadores(conn, jugador, lista_conexiones, game, condition):
    conn.send('---El JUEGO EMPEZO---'.encode('utf-8'))
    while True:
        logging.debug('Al empezar TURNO contador: ' + str(game.contador))
        with condition:                     #acquire implicito

            if game.contador <= 0:          #cuando no haya mas movimientos CONDICION PARA SALIR DE ESTE DEF
                condition.notify_all()      #notifica a los demas hilos que pueden continuar
                break

            msg = game.get_hiddenBoard()
            conn.send(msg.encode('utf-8'))

            # Parte 1(Avisar que es turno del jugador activo)
            logging.debug('Comenzo su TURNO: ' + jugador.nombre)
            msg = 'Tu turno: '
            conn.send(msg.encode('utf-8'))

            # Parte 2(Recibe y evalua la respuesta del jugador)
            msg = conn.recv(1024).decode('utf-8')
            if msg == 'exit':
                msg = 'El jugador: ' + jugador.nombre + ' abandono el juego'
                msg_to_all(lista_conexiones, msg)
                cerrar_servidor(lista_conexiones)
                condition.notify_all()  #notifica a los demas hilos que pueden continuar
                break
            msg = game.tirada(msg, jugador)

            # Parte 3(Enviar el tablero actualizado)
            conn.send(msg.encode('utf-8'))
            logging.debug('El tablero queda: \n' + game.get_hiddenBoard())
            logging.debug('Al terminar TURNO contador: ' + str(game.contador))
            logging.debug('Termino su TURNO')
            condition.notify_all()      #notifica a los demas hilos que pueden continuar
            condition.wait()            #bloquea la ejecucion del hilo hasta que un condition notify all aparezca


if __name__ == "__main__":
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(address_server)
    socket_server.listen(LIMITE_JUGADORES)

    jugadores = []  # Lista de objetos tipo memorama.memorama_jugador

    condition = threading.Condition() #Creacion para coordinacion de hilos
    threads_jugadores = []              #Lista para almacenar los hilos

    print('Esperando conexiones')
    aceptar_jugadores(socket_server, lista_conexiones, LIMITE_JUGADORES, jugadores)
    try:
        id = 0
        for conn in lista_conexiones:                           #Recorre lista de conexiones
            threads_jugadores.append(threading.Thread(target=manejo_jugadores, args=(conn, jugadores[id], lista_conexiones, game, condition)).start()) #Creacion del hilo, argumentos para interactuar con el jugador
            id += 1                                                                                                                                    #y donde se hara el juego segun la lista

        for t in threading.enumerate():     #devuelve una lista de los hilos en ejecucion
            if t is not MAIN_THREAD:        #                       segmento espera aque todos los hilos (el principal no) termine su ejecucion para continuar conel programa
                t.join()                    #tjoin bloquea cualquier proceso hasta que termine su ejecucion que se le ha dicho que haga
    except:
        print('Hubo un error al crear hilos')
    print('El juego TERMINO')

    # Ordenamiento de los jugadores
    marcador = sorted(jugadores, key=lambda objeto: objeto.puntuacion, reverse=True)        #Ordena segun puntuacion
    msg = '\n----PUNTUACION FINAL----\n'
    posicion = 1
    for jugador in marcador:
        msg = msg + str(posicion) + ')' + jugador.nombre + ' con ' + str(jugador.puntuacion) + '\n'
        posicion += 1

    msg_to_all(lista_conexiones, msg)
    print(msg)
    cerrar_servidor(lista_conexiones)
    socket_server.close()
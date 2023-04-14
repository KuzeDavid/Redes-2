import socket
import selectors

# Tamaño del búfer de transferencia
buffer_size=32768

# Crear un nuevo selector
sel = selectors.DefaultSelector()

# Función para aceptar conexiones entrantes
def accept(sock):
    conn, addr = sock.accept()
    print(f"Conexión aceptada desde {addr}")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

# Función para leer datos del cliente
# Función para leer datos del cliente
def read(conn):
    data = conn.recv(buffer_size)
    if data:
        # Obtener el puerto del cliente
        client_port = conn.getpeername()[1]
        # Generar el nombre de archivo con el identificador del puerto
        file_name = f'audio_{client_port}.wav'
        # Guardar los datos en el archivo
        with open(file_name, 'ab') as f:
            f.write(data)
        print(f"Recibidos {len(data)} bytes y guardados en {file_name}")
    else:
        print("Cliente desconectado")
        sel.unregister(conn)
        conn.close()


# Crear un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 12345))
sock.listen(5)
print("Servidor escuchando en localhost:12345")
sock.setblocking(False)

# Registrar el socket en el selector para eventos de lectura
sel.register(sock, selectors.EVENT_READ, accept)

# Bucle principal del servidor
while True:
    # Esperar a que haya eventos de entrada/salida en los sockets registrados
    events = sel.select()
    for key, _ in events:
        # Obtener la función de callback asociada al evento
        callback = key.data
        # Llamar a la función de callback con el socket como argumento
        callback(key.fileobj)

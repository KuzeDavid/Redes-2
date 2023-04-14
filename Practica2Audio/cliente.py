import socket
import time

buffer_size=32768
# Crear un socket de cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Enviar archivo de audio al servidor
filename = 'audiobeat.wav'
with open(filename, 'rb') as file:
    while True:
        data = file.read(buffer_size)
        if not data:
            break
        try:
            # Enviar datos al servidor
            client_socket.sendall(data)
            time.sleep(0.1)  # Pequeña pausa para evitar saturación del socket
        except socket.error:
            pass  # Ignorar errores de no bloqueo

print("Archivo de audio enviado con éxito")

# Cerrar el socket del cliente
client_socket.close()

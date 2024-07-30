import socket
import threading


def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request: {request}")

    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, client!"
    client_socket.send(response.encode('utf-8'))

    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Server listening on port 8080")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from: {addr[0]}:{addr[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


start_server()

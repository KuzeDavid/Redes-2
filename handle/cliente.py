import socket


def send_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(request.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {response}")

    client_socket.close()


send_request()

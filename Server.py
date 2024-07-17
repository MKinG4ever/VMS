import socket


def create_proxy_server(host: str, port: int):
    """
    Create a simple proxy server.

    Version: 0.0
    Timestamp: R

    :param host: Host address
    :param port: Port number
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(5)
        print(f"Proxy server running on {host}:{port}")

        while True:
            client_socket, client_address = server.accept()
            with client_socket:
                print(f"Connection from {client_address}")
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)


if __name__ == "__main__":
    create_proxy_server('0.0.0.0', 3128)

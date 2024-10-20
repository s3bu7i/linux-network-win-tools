import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    print(f"Server is running on {HOST}:{PORT}")

    # Listen for incoming connections (allowing up to 5 simultaneous clients)
    server_socket.listen(5)

    while True:
        client_socket, client_address = server_socket.accept()
        with client_socket:
            print(f"Connected by {client_address}")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break 

                print(f"Received: {data.decode()}")
                client_socket.sendall(b"Message received!")

            print(f"Disconnected from {client_address}")

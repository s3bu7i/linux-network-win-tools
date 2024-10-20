import socket

HOST = '127.0.0.1'
PORT = 65432        

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")

    while True:
        message = input(
            "Enter message to send to server (or 'exit' to quit): ")

        if message.lower() == 'exit':
            print("Closing connection...")
            break

        # Send the message to the server
        client_socket.sendall(message.encode())

        # Receive the server's response
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

    print("Connection closed.")

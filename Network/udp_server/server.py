import socket

server_address = ('localhost', 6789)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(server_address)

print(f"Server listening on {server_address[0]}:{server_address[1]}")

while True:
    print("\nWaiting for a connection...")

    data, address = sock.recvfrom(1024)

    print(f"Received {len(data)} bytes from {address}")
    print(f"Message: {data.decode()}")

    if data:
        sent = sock.sendto(b"Message received", address)
        print(f"Sent confirmation back to {address}")

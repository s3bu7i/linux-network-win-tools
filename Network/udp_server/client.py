import socket

server_address = ('localhost', 6789)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send data
    message = input("Enter message: ").encode()
    print(f"Sending: {message.decode()}")
    sent = sock.sendto(message, server_address)

    # Receive response
    data, server = sock.recvfrom(1024)
    print(f"Received reply: {data.decode()}")

finally:
    print("Closing the connection")
    sock.close()

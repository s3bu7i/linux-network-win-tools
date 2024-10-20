import socket
import threading

HOST = 'localhost'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                print("Disconnected from server.")
                break
            print(message)
        except Exception:
            print("An error occurred.")
            sock.close()
            break

def send_messages(sock):
    while True:
        message = input()
        sock.send(message.encode())


def main():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the chat server
        client_socket.connect((HOST, PORT))
    except Exception:
        print("Failed to connect to the server.")
        return

    print("Connected to the chat server.")

    receive_thread = threading.Thread(
        target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


if __name__ == "__main__":
    main()

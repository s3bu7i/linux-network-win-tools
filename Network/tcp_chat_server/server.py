import socket
import threading

HOST = 'localhost'
PORT = 12345

clients = {}

def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except Exception:
                remove_client(client_socket)

def handle_client(client_socket, address):
    print(f"New connection from {address}")

    nickname = get_unique_nickname(client_socket)
    clients[client_socket] = nickname
    print(f"Nickname of {address} is {nickname}")

    broadcast(f"{nickname} has joined the chat!")
    client_socket.send(f"Welcome to the chat, {nickname}!\n".encode())

    listen_for_messages(client_socket, nickname)

def get_unique_nickname(client_socket):
    client_socket.send("Enter your nickname: ".encode())
    nickname = client_socket.recv(1024).decode()
    while nickname in clients.values():
        client_socket.send("Nickname already taken, choose another: ".encode())
        nickname = client_socket.recv(1024).decode()
    return nickname

def listen_for_messages(client_socket, nickname):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith("/"):
                handle_command(client_socket, message)
            else:
                broadcast(f"{nickname}: {message}", client_socket)
        except Exception:
            remove_client(client_socket)
            break

def handle_command(client_socket, message):
    if message == "/list":
        client_socket.send(f"Connected users: {', '.join(clients.values())}\n".encode())
    elif message == "/quit":
        remove_client(client_socket)
    elif message.startswith("/msg"):
        try:
            target_nickname, private_msg = message.split(" ", 2)[1:]
            private_message(client_socket, target_nickname, private_msg)
        except ValueError:
            client_socket.send("Usage: /msg <nickname> <message>\n".encode())
    else:
        client_socket.send("Unknown command.\n".encode())

def private_message(sender_socket, target_nickname, message):
    sender_nickname = clients[sender_socket]
    for client_socket, nickname in clients.items():
        if nickname == target_nickname:
            try:
                client_socket.send(f"[Private from {sender_nickname}]: {
                                   message}\n".encode())
                sender_socket.send(f"[Private to {target_nickname}]: {
                                   message}\n".encode())
                return
            except Exception:
                remove_client(client_socket)
                return
    sender_socket.send(f"User {target_nickname} not found.\n".encode())

def remove_client(client_socket):
    if client_socket in clients:
        nickname = clients[client_socket]
        del clients[client_socket]
        client_socket.close()
        print(f"{nickname} has disconnected")
        broadcast(f"{nickname} has left the chat.")

def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, address = server_socket.accept()

        thread = threading.Thread(
            target=handle_client, args=(client_socket, address))
        thread.start()


if __name__ == "__main__":
    main()

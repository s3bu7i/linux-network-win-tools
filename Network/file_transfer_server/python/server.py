import socket
import os
import threading

BUFFER_SIZE = 4096
HOST = '127.0.0.1'
PORT = 5001


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data:
            break

        command, filename = data.split()  # 'upload' or 'download'

        if command == "upload":
            handle_upload(conn, filename)
        elif command == "download":
            handle_download(conn, filename)
        else:
            conn.send("ERROR: Invalid command.".encode())

    conn.close()


def handle_upload(conn, filename):
    file_size = int(conn.recv(BUFFER_SIZE).decode())
    with open(f'server_files/{filename}', 'wb') as f:
        received_bytes = 0
        while received_bytes < file_size:
            bytes_read = conn.recv(BUFFER_SIZE)
            f.write(bytes_read)
            received_bytes += len(bytes_read)
            print(f"Received {received_bytes}/{file_size} bytes.")
    conn.send(f"File {filename} uploaded successfully.".encode())


def handle_download(conn, filename):
    if os.path.exists(f'server_files/{filename}'):
        file_size = os.path.getsize(f'server_files/{filename}')
        conn.send(f"{file_size}".encode())
        with open(f'server_files/{filename}', 'rb') as f:
            sent_bytes = 0
            while sent_bytes < file_size:
                bytes_read = f.read(BUFFER_SIZE)
                conn.sendall(bytes_read)
                sent_bytes += len(bytes_read)
                print(f"Sent {sent_bytes}/{file_size} bytes.")
        conn.send(f"File {filename} sent successfully.".encode())
    else:
        conn.send("ERROR: File not found.".encode())


def start_server():
    if not os.path.exists('server_files'):
        os.makedirs('server_files')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()

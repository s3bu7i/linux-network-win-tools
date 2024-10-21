import socket
import ssl
import os
import threading

# Server address
HOST = '0.0.0.0'
PORT = 9000

# Path where files will be saved
FILE_DIR = './server_files/'

# SSL context for secure transmission
def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')  # Use your own certificate
    return context

# Function to handle each client
def handle_client(conn, addr):
    print(f'[+] Connection from {addr}')
    
    try:
        # Receive the file name
        filename = conn.recv(1024).decode().strip()
        if not filename:
            print('[-] No file received')
            return

        # Send confirmation
        conn.send(b'Filename received')

        # Receive the file size
        filesize = int(conn.recv(1024).decode().strip())
        conn.send(b'Filesize received')

        print(f'[+] Receiving file: {filename} ({filesize} bytes)')
        
        # Receive the file data
        with open(os.path.join(FILE_DIR, filename), 'wb') as f:
            remaining = filesize
            while remaining > 0:
                chunk_size = 4096
                if remaining < chunk_size:
                    chunk_size = remaining
                chunk = conn.recv(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                remaining -= len(chunk)
        
        print(f'[+] File {filename} received successfully.')
    
    except Exception as e:
        print(f'[-] Error: {e}')
    
    finally:
        conn.close()

def start_server():
    # Ensure the file directory exists
    if not os.path.exists(FILE_DIR):
        os.makedirs(FILE_DIR)

    # Create SSL context
    ssl_context = create_ssl_context()

    # Setup socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f'[*] Server listening on {HOST}:{PORT}')
    
    while True:
        client_socket, client_address = server.accept()
        # Wrap the socket with SSL
        conn = ssl_context.wrap_socket(client_socket, server_side=True)
        
        # Handle client in a new thread
        client_thread = threading.Thread(target=handle_client, args=(conn, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()

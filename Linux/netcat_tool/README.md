
# Python Netcat Tool

This is an advanced Python implementation of the Netcat tool, a versatile networking utility. This tool allows for port scanning, file transfers, chat communication, and remote shell execution over TCP connections.

## Features
- **Port Scanning**: Scan a range of ports on a target host.
- **File Transfer**: Send and receive files between two machines.
- **Chat Functionality**: Enable communication between two machines over TCP.
- **Remote Shell Access**: Execute commands remotely on a machine over a network.

## Requirements
- Python 3.x

## Usage

You can use the script by specifying the mode of operation and required arguments.

### Port Scanning

Scan open ports on a target IP within a specified range of ports.

```bash
python netcat.py --mode scan --target <target_ip> --start_port <start_port> --end_port <end_port>
```
Example:
```bash
python netcat.py --mode scan --target 192.168.1.10 --start_port 1 --end_port 100
```

### File Transfer

#### Send a file:
```bash
python netcat.py --mode send --target <target_ip> --port <port> --file <file_path>
```
Example:
```bash
python netcat.py --mode send --target 192.168.1.10 --port 4444 --file myfile.txt
```

#### Receive a file:
```bash
python netcat.py --mode receive --port <port> --save <save_path>
```
Example:
```bash
python netcat.py --mode receive --port 4444 --save received_file.txt
```

### Chat Functionality

Set up a chat between two machines over TCP.

#### Server (Listen for chat):
```bash
python netcat.py --mode chat --port <port>
```
Example:
```bash
python netcat.py --mode chat --port 4444
```

#### Client (Connect to chat server):
```bash
python netcat.py --mode chat --target <server_ip> --port <port>
```
Example:
```bash
python netcat.py --mode chat --target 192.168.1.10 --port 4444
```

### Remote Shell Access

Execute commands remotely on a target machine.

#### Server (Start remote shell):
```bash
python netcat.py --mode shell --port <port>
```
Example:
```bash
python netcat.py --mode shell --port 4444
```

#### Client (Connect to remote shell server):
```bash
python netcat.py --mode shell --target <server_ip> --port <port>
```
Example:
```bash
python netcat.py --mode shell --target 192.168.1.10 --port 4444
```

## Security Notice

This tool allows for remote shell access and file transfers, which could be misused if used improperly. Only use this tool in controlled environments where you have permission to do so.

## License

This project is licensed under the MIT License.


# Python Network Scanner Tool

## Overview

This is an advanced Python-based network scanner tool designed to discover devices on a local network, perform port scanning, and retrieve service banners from open ports. It combines the capabilities of **ARP scanning**, **port scanning** (using `nmap`), and **banner grabbing** to provide detailed information about connected devices and the services they are running.

## Features

- **ARP Scan**: Discover all devices connected to your network.
- **Port Scanning**: Scan common ports (1-1024) to identify open ports on discovered devices.
- **Banner Grabbing**: Retrieve information about services running on open ports.
- **Easy-to-use**: Enter the IP range, and the tool will automatically perform all scanning tasks.

## Requirements

### Python Libraries:
- `scapy`
- `nmap`
- `socket`

Install the required libraries using pip:
```bash
pip install scapy python-nmap
```

### System Requirements:
- **Nmap**: This tool requires the **Nmap** executable installed on your system, as the `python-nmap` library is a wrapper for Nmap.
  - Download and install Nmap from the official site: [Nmap Download](https://nmap.org/download.html)
  - Ensure Nmap is added to your system's `PATH`.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/network-scanner-tool.git
   cd network-scanner-tool
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install **Nmap** on your system:
   - [Download and Install Nmap](https://nmap.org/download.html) (ensure it is added to your `PATH`).
   - Verify installation by running `nmap --version`.

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Enter the IP range to scan (e.g., `192.168.1.0/24`):
   ```
   Enter IP range to scan (e.g., 192.168.1.0/24): 192.168.1.0/24
   ```

3. The tool will:
   - Discover devices on the network.
   - Perform port scanning on each discovered device.
   - Retrieve banners from the open ports.

### Example Output

```
Found 3 devices on the network:
IP: 192.168.1.10 - MAC: aa:bb:cc:dd:ee:ff
  Open ports: [22, 80]
    Port 22 banner: SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
    Port 80 banner: HTTP/1.1 200 OK

IP: 192.168.1.12 - MAC: ff:ee:dd:cc:bb:aa
  Open ports: [443]
    Port 443 banner: HTTP/1.1 200 OK
```

## Troubleshooting

- **Nmap not found**: Ensure that Nmap is installed and correctly added to your system's `PATH`. Verify by running `nmap --version` from the terminal.
- **Permission errors**: On some systems, you may need to run the script with elevated privileges (e.g., as an administrator on Windows or with `sudo` on Linux).

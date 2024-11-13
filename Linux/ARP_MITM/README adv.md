
# ARP Spoofing and HTTP Packet Sniffer

This script performs **ARP Spoofing** (Man-in-the-Middle) attacks using the `scapy` library to intercept and display HTTP traffic between a target machine and a gateway. It also enables **packet sniffing** to monitor HTTP requests and responses in real-time.

## Features:
- **ARP Spoofing**: Redirects network traffic to the attacker's machine by manipulating ARP tables.
- **HTTP Packet Sniffing**: Captures and displays HTTP requests and responses, including URLs, methods, and raw data.
- **Restoration**: Restores network settings to their original state once the attack is stopped.

## Requirements:
- **Python 3**
- **Scapy library**: Used for network packet manipulation.

### Installation
1. Install Python 3 on your system if it's not already installed.
2. Install `scapy`:
   ```bash
   sudo apt-get install python3-pip
   sudo pip3 install scapy
   ```

## Usage:

### Running the Script:

```bash
sudo python3 advanced_mitm.py -t <target_ip> -g <gateway_ip>
```

### Arguments:
- `-t <target_ip>`: The IP address of the target machine.
- `-g <gateway_ip>`: The IP address of the gateway (router).

### Example:
```bash
sudo python3 advanced_mitm.py -t 192.168.1.10 -g 192.168.1.1
```

### Output:
- The script will continuously send ARP spoofing packets to poison the ARP cache of the target and the gateway.
- It will also print out any intercepted HTTP requests and responses, including URLs, methods, and raw data (if available).

### Stopping the Attack:
To stop the script, press `Ctrl+C`. The script will then restore the network settings to their original state.

## Important Notes:
- **Legal Disclaimer**: **ARP Spoofing** is illegal in many countries when done without explicit permission. Only use this script on networks you own or have permission to test.
- **Sudo Privileges**: This script requires root/sudo access to manipulate network settings and send ARP packets.

## Troubleshooting:
- **"Permission Denied"**: Ensure you run the script with `sudo`.
- **Interface Not Found**: If you encounter an error about the network interface, change the `interface` variable in the script to the correct one for your system (e.g., `wlan0`, `eth0`, etc.).



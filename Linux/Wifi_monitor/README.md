
# README for Advanced WiFi Monitoring Tool

## Overview

This project provides an **Advanced WiFi Monitoring Tool** for detecting nearby WiFi networks, extracting network details, and saving the data in CSV format. The tool enables users to set the network interface in monitor mode, perform channel hopping for comprehensive network coverage, and analyze network packets in real time.

---

## Features

1. **Channel Hopping**: Continuously switches between specified channels for better coverage.
2. **Network Details Extraction**: Captures details like SSID, BSSID, signal strength, channel, and encryption type.
3. **Real-Time Monitoring**: Displays detected networks and updates packet capture statistics dynamically.
4. **CSV Export**: Saves network data into a CSV file for offline analysis.
5. **Customizable Band and Channels**: Allows users to specify channels and band for monitoring.

---

## Requirements

- **Python 3.7+**
- **Dependencies**:
  - `scapy`
  - `tabulate`
- **System Requirements**:
  - A compatible WiFi adapter that supports monitor mode.
  - Root privileges for setting monitor mode and channel hopping.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/wifi-monitoring-tool.git
   cd wifi-monitoring-tool
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Basic Usage
Run the script with the following command:
```bash
sudo python3 wifi_monitoring.py -i <interface>
```

### Additional Options
- **Specify Channels**:
  ```bash
  sudo python3 wifi_monitoring.py -i <interface> --channels 1 6 11
  ```
- **Specify Network Band**:
  ```bash
  sudo python3 wifi_monitoring.py -i <interface> --band 2.4
  ```

### Help
For a detailed list of options, use:
```bash
python3 wifi_monitoring.py -h
```

---

## Output

### Real-Time Monitoring
Detected networks are displayed in the terminal in a tabular format:
```
+----------------+-------------------+------------------+----------+-------------+
| SSID           | BSSID            | Signal Strength  | Channel  | Encryption  |
+----------------+-------------------+------------------+----------+-------------+
| MyNetwork      | AA:BB:CC:DD:EE:FF| -45 dBm          | 6        | WPA/WPA2    |
+----------------+-------------------+------------------+----------+-------------+
```

### CSV File
All detected networks are saved to `output.csv` in the current directory:
```csv
SSID,BSSID,Signal Strength,Channel,Encryption
MyNetwork,AA:BB:CC:DD:EE:FF,-45,6,WPA/WPA2
```

---

## Key Functions

### `channel_hopper()`
Switches between the specified WiFi channels to maximize coverage.

### `get_network_details()`
Extracts SSID, BSSID, signal strength, channel, and encryption type from packets.

### `set_monitor_mode()`
Configures the specified interface to monitor mode.

### `write_to_csv()`
Saves the detected network information to a CSV file.

### `wifi_monitor()`
Handles packet sniffing and real-time display of network information.

---

## Notes

- **Root Privileges**: The tool requires root privileges to set monitor mode and perform channel hopping.
- **Legal Disclaimer**: This tool is intended for educational and lawful purposes only. Unauthorized use of this tool to monitor networks without permission may violate local laws.

---

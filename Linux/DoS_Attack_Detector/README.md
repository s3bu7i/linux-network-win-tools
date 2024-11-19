
# Advanced DoS Attack Detector

An advanced Python-based program to monitor network traffic and detect potential Denial of Service (DoS) attacks. The program uses packet analysis and threshold-based detection, providing real-time alerts through a command-line interface.

## Features

- Real-time Traffic Monitoring: Analyze packets on the specified network interface.
- DoS Detection: Detect suspicious activity based on packet rate thresholds.
- Logging: Save detection alerts to a log file (`dos_detector.log`).
- Customizable: Configure packet thresholds and time windows using CLI arguments.
- User-Friendly CLI: Clear and interactive command-line interface.

## Requirements

- Python 3.7 or higher
- Libraries:
  - `scapy`

Install required libraries using:
```bash
pip install scapy
```

## Usage

### 1. Run the Program
```bash
python dos_detector.py -i <interface> -t <threshold> -w <time_window> -l
```

### 2. CLI Arguments
| Argument        | Description                              | Default |
|------------------|------------------------------------------|---------|
| `-i, --interface` | Network interface to monitor (e.g., eth0, wlan0) | **Required** |
| `-t, --threshold` | Packet threshold per time window        | 100     |
| `-w, --time_window` | Time window for threshold in seconds  | 10      |
| `-l, --log`       | Enable logging to file (`dos_detector.log`) | Disabled |

Example:
```bash
python dos_detector.py -i eth0 -t 200 -w 15 -l
```

### 3. Stopping the Program
Press `Ctrl+C` to stop monitoring traffic.

## Example Output

```plaintext
Monitoring traffic on interface: eth0
Detection threshold: 100 packets/10 seconds
Press Ctrl+C to stop...

ALERT: DoS attack detected from IP: 192.168.1.100
ALERT: DoS attack detected from IP: 192.168.1.105
Stopped monitoring.
```

## Logging

- Alerts are saved to `dos_detector.log` if the `-l` flag is used.
- Log format:
  ```
  YYYY-MM-DD HH:MM:SS - Potential DoS attack detected from IP: <IP>
  ```

## How It Works

1. Captures network packets using `scapy`.
2. Tracks packet counts for each IP within a specified time window.
3. Flags and alerts when an IP exceeds the defined packet threshold.
4. Periodically resets counters to maintain real-time accuracy.

## Limitations

- This program is designed for educational and small-scale use.
- For large-scale environments, consider:
  - Machine learning-based detection.
  - Integration with tools like Snort, Suricata, or Splunk.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built using the amazing [scapy](https://scapy.net/) library.
- Inspired by the need for practical cybersecurity tools.

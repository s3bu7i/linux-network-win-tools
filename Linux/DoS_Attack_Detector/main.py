import argparse
import logging
from scapy.all import sniff, IP
from collections import defaultdict
from datetime import datetime, timedelta
import os
import sys

# Setting up logging
logging.basicConfig(
    filename="/dos_detector.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Global variables
packet_count = defaultdict(int)
alerted_ips = set()
start_time = datetime.now()


def detect_dos(packet, threshold, time_window):
    """
    Detect potential DoS attacks by monitoring packet rates.
    """
    global packet_count, alerted_ips, start_time
    current_time = datetime.now()

    # Reset packet counts periodically
    if current_time - start_time > timedelta(seconds=time_window):
        packet_count.clear()
        alerted_ips.clear()
        start_time = current_time

    # Check if the packet has an IP layer
    if IP in packet:
        src_ip = packet[IP].src
        packet_count[src_ip] += 1

        # Trigger alert if threshold exceeded
        if packet_count[src_ip] > threshold and src_ip not in alerted_ips:
            logging.warning(f"Potential DoS attack detected from IP: {src_ip}")
            print(f"⚠️ ALERT: DoS attack detected from IP: {src_ip}")
            alerted_ips.add(src_ip)


def monitor_traffic(interface, threshold, time_window):
    """
    Monitor network traffic on a specified interface.
    """
    print(f"🌐 Monitoring traffic on interface: {interface}")
    print(f"🚀 Detection threshold: {threshold} packets/{time_window} seconds")
    print("Press Ctrl+C to stop...\n")

    try:
        sniff(
            iface=interface,
            prn=lambda packet: detect_dos(packet, threshold, time_window),
            store=False,
        )
    except KeyboardInterrupt:
        print("\n🛑 Stopped monitoring.")
        sys.exit(0)


def main():
    """
    Command-line interface for the DoS detector.
    """
    parser = argparse.ArgumentParser(
        description="🚀 Advanced DoS Attack Detector using Python"
    )
    parser.add_argument(
        "-i", "--interface", required=True, help="Network interface to monitor (e.g., eth0, wlan0)"
    )
    parser.add_argument(
        "-t", "--threshold", type=int, default=100, help="Packet threshold per time window"
    )
    parser.add_argument(
        "-w", "--time_window", type=int, default=10, help="Time window for threshold in seconds"
    )
    parser.add_argument(
        "-l", "--log", action="store_true", help="Enable logging to file"
    )

    args = parser.parse_args()

    # Enable logging if specified
    if args.log:
        print(f"📁 Logs will be saved to: {
              os.path.abspath('dos_detector.log')}")

    # Run the traffic monitor
    monitor_traffic(args.interface, args.threshold, args.time_window)


if __name__ == "__main__":
    main()

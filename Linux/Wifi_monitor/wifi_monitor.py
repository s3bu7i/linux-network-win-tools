import os
import time
import argparse
import csv
from scapy.all import sniff
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
from tabulate import tabulate
import threading

# Channel hopping function


def channel_hopper(interface, channels=[1, 6, 11]):
    print("Channel hopping is active...")
    while True:
        for channel in channels:
            os.system(f"sudo iwconfig {interface} channel {channel}")
            time.sleep(1)

# Function to extract network details


def get_network_details(packet):
    ssid = packet[Dot11Elt].info.decode(errors="ignore")
    bssid = packet[Dot11].addr3
    signal_strength = getattr(packet, "dBm_AntSignal", "N/A")
    channel = ord(packet[Dot11Elt:3].info)
    encryption = "Open" if "privacy" not in packet.sprintf(
        "{Dot11Beacon:%Dot11Beacon.cap%}") else "WPA/WPA2"
    return ssid, bssid, signal_strength, channel, encryption

# Function to set monitor mode


def set_monitor_mode(interface):
    os.system(f"sudo ip link set {interface} down")
    os.system(f"sudo iw {interface} set type monitor")
    os.system(f"sudo ip link set {interface} up")

# Function to write data to CSV


def write_to_csv(networks, filename="output.csv"):
    headers = ["SSID", "BSSID", "Signal Strength", "Channel", "Encryption"]
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(networks.values())

# WiFi monitoring function


def wifi_monitor(interface):
    networks = {}
    unique_bssids = set()
    total_packets = 0

    def packet_handler(packet):
        nonlocal total_packets
        total_packets += 1

        if packet.haslayer(Dot11Beacon):
            ssid, bssid, signal, channel, encryption = get_network_details(
                packet)
            if bssid not in unique_bssids:
                unique_bssids.add(bssid)
                networks[bssid] = [ssid, bssid, signal, channel, encryption]
                print(tabulate([networks[bssid]], headers=[
                      "SSID", "BSSID", "Signal", "Channel", "Encryption"], tablefmt="grid"))

        # Real-time statistics
        print(f"\rPackets Captured: {total_packets}, Unique Networks: {
              len(unique_bssids)}", end="")

    print("WiFi Monitoring Started. Press Ctrl+C to stop.")
    try:
        sniff(iface=interface, prn=packet_handler)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        write_to_csv(networks)
        print(f"Collected data saved to {os.path.abspath('output.csv')}.")


def main():
    parser = argparse.ArgumentParser(
        description="Advanced WiFi Monitoring Tool")
    parser.add_argument("-i", "--interface", required=True,
                        help="Network interface to use")
    parser.add_argument("--channels", nargs="+", type=int,
                        default=[1, 6, 11], help="Channels to monitor")
    parser.add_argument(
        "--band", choices=["2.4", "5"], default="2.4", help="Network band (2.4GHz or 5GHz)")
    args = parser.parse_args()

    interface = args.interface
    channels = args.channels

    # Set monitor mode
    set_monitor_mode(interface)

    # Start channel hopping
    hopper_thread = threading.Thread(
        target=channel_hopper, args=(interface, channels), daemon=True)
    hopper_thread.start()

    # Start monitoring
    wifi_monitor(interface)


if __name__ == "__main__":
    main()

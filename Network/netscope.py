#!/usr/bin/env python3
"""
NetScope - Advanced Network Analysis Tool
A comprehensive network analyzer with interactive menu system
"""

import subprocess
import socket
import json
import time
import os
import sys
import platform
from datetime import datetime
import re
import ipaddress
import threading
from concurrent.futures import ThreadPoolExecutor


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class NetworkAnalyzer:
    def __init__(self):
        self.system = platform.system()
        self.local_ip = None
        self.gateway_ip = None
        self.public_ip = None
        self.network_info = {}
        self.scan_results = {}

    def print_banner(self):
        """Display the program banner"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  {Colors.BOLD}███╗   ██╗███████╗████████╗███████╗ ██████╗ ██████╗ ███████╗{Colors.ENDC}{Colors.CYAN}  ║
║  {Colors.BOLD}████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔═══██╗██╔════╝{Colors.ENDC}{Colors.CYAN}  ║
║  {Colors.BOLD}██╔██╗ ██║█████╗     ██║   ███████╗██║     ██║   ██║██████╗ {Colors.ENDC}{Colors.CYAN}  ║
║  {Colors.BOLD}██║╚██╗██║██╔══╝     ██║   ╚════██║██║     ██║   ██║██╔═══╝ {Colors.ENDC}{Colors.CYAN}  ║
║  {Colors.BOLD}██║ ╚████║███████╗   ██║   ███████║╚██████╗╚██████╔╝███████╗{Colors.ENDC}{Colors.CYAN}  ║
║  {Colors.BOLD}╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝{Colors.ENDC}{Colors.CYAN}  ║
║                                                              ║
║           {Colors.BOLD}Advanced Network Analysis & Discovery Tool{Colors.ENDC}{Colors.CYAN}         ║
║                   {Colors.YELLOW}Created for Network Engineers{Colors.ENDC}{Colors.CYAN}              ║
╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(banner)

    def execute_command(self, command):
        """Execute system command and return output"""
        try:
            if isinstance(command, str):
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=30)
            else:
                result = subprocess.run(
                    command, capture_output=True, text=True, timeout=30)
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1

    def get_local_ip(self):
        """Get local IP address"""
        try:
            # Connect to a remote address (doesn't actually send data)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                self.local_ip = s.getsockname()[0]
                return self.local_ip
        except:
            return "Unable to determine"

    def get_gateway_ip(self):
        """Get default gateway IP"""
        try:
            if self.system == "Windows":
                output, _, _ = self.execute_command("ipconfig /all")
                for line in output.split('\n'):
                    if 'Default Gateway' in line:
                        gateway = line.split(':')[-1].strip()
                        if gateway and gateway != "":
                            self.gateway_ip = gateway
                            return gateway
            else:
                output, _, _ = self.execute_command("ip route | grep default")
                if output:
                    self.gateway_ip = output.split()[2]
                    return self.gateway_ip
                else:
                    output, _, _ = self.execute_command(
                        "route -n | grep '^0.0.0.0'")
                    if output:
                        self.gateway_ip = output.split()[1]
                        return self.gateway_ip
        except:
            pass
        return "Unable to determine"

    def get_public_ip(self):
        """Get public IP address"""
        services = [
            "curl -s ifconfig.me",
            "curl -s ipinfo.io/ip",
            "curl -s icanhazip.com",
            "curl -s ident.me"
        ]

        for service in services:
            try:
                output, _, code = self.execute_command(service)
                if code == 0 and output:
                    self.public_ip = output.strip()
                    return self.public_ip
            except:
                continue
        return "Unable to determine"

    def get_interface_info(self):
        """Get detailed network interface information"""
        interfaces = {}
        try:
            if self.system == "Windows":
                output, _, _ = self.execute_command("ipconfig /all")
                current_interface = None
                for line in output.split('\n'):
                    line = line.strip()
                    if 'adapter' in line.lower() and ':' in line:
                        current_interface = line.split(':')[0].strip()
                        interfaces[current_interface] = {}
                    elif current_interface and line:
                        if 'Physical Address' in line or 'MAC' in line:
                            interfaces[current_interface]['MAC'] = line.split(
                                ':')[-1].strip()
                        elif 'IPv4 Address' in line:
                            ip = line.split(
                                ':')[-1].strip().replace('(Preferred)', '').strip()
                            interfaces[current_interface]['IP'] = ip
                        elif 'Subnet Mask' in line:
                            interfaces[current_interface]['Subnet'] = line.split(
                                ':')[-1].strip()
            else:
                # Linux/Unix systems
                output, _, _ = self.execute_command("ip addr show")
                current_interface = None
                for line in output.split('\n'):
                    if re.match(r'^\d+:', line):
                        current_interface = line.split(':')[1].strip()
                        interfaces[current_interface] = {}
                    elif current_interface and 'link/ether' in line:
                        interfaces[current_interface]['MAC'] = line.split()[1]
                    elif current_interface and 'inet ' in line and 'scope global' in line:
                        ip_info = line.split()[1]
                        interfaces[current_interface]['IP'] = ip_info.split(
                            '/')[0]
                        interfaces[current_interface]['CIDR'] = ip_info
        except:
            pass
        return interfaces

    def get_dns_servers(self):
        """Get DNS server information"""
        dns_servers = []
        try:
            if self.system == "Windows":
                output, _, _ = self.execute_command('nslookup google.com')
                lines = output.split('\n')
                for line in lines:
                    if 'Server:' in line:
                        dns_ip = line.split(':')[-1].strip()
                        if dns_ip:
                            dns_servers.append(dns_ip)
            else:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns_servers.append(line.split()[1])
        except:
            pass
        return dns_servers

    def scan_network_ports(self, target_ip, ports=None):
        """Scan common ports on target IP"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110,
                     143, 443, 993, 995, 3389, 5432, 3306]

        open_ports = []

        def scan_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((target_ip, port))
                    if result == 0:
                        return port
            except:
                pass
            return None

        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(scan_port, ports)
            open_ports = [port for port in results if port is not None]

        return sorted(open_ports)

    def discover_network_devices(self):
        """Discover devices on the local network"""
        if not self.local_ip:
            self.get_local_ip()

        if not self.local_ip or self.local_ip == "Unable to determine":
            return {}

        # Get network range
        try:
            network = ipaddress.IPv4Network(
                f"{self.local_ip}/24", strict=False)
        except:
            return {}

        devices = {}

        def ping_host(ip):
            if self.system == "Windows":
                cmd = f"ping -n 1 -w 1000 {ip}"
            else:
                cmd = f"ping -c 1 -W 1 {ip}"

            _, _, code = self.execute_command(cmd)
            if code == 0:
                hostname = "Unknown"
                try:
                    hostname = socket.gethostbyaddr(str(ip))[0]
                except:
                    pass
                return str(ip), hostname
            return None, None

        print(f"\n{Colors.YELLOW}🔍 Scanning network {network}...{Colors.ENDC}")

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(ping_host, ip)
                       for ip in network.hosts()]
            for i, future in enumerate(futures):
                ip, hostname = future.result()
                if ip:
                    devices[ip] = {'hostname': hostname}
                # Progress indicator
                if i % 10 == 0:
                    print(
                        f"\r{Colors.CYAN}Progress: {i+1}/{len(futures)}{Colors.ENDC}", end="")

        print(f"\r{Colors.GREEN}✅ Network scan complete!{Colors.ENDC}\n")
        return devices

    def get_routing_table(self):
        """Get routing table information"""
        routes = []
        try:
            if self.system == "Windows":
                output, _, _ = self.execute_command("route print")
            else:
                output, _, _ = self.execute_command("ip route")
            routes = output.split('\n')
        except:
            pass
        return routes

    def trace_route(self, destination="8.8.8.8"):
        """Perform traceroute to destination"""
        try:
            if self.system == "Windows":
                output, _, _ = self.execute_command(f"tracert {destination}")
            else:
                output, _, _ = self.execute_command(
                    f"traceroute {destination}")
            return output.split('\n')
        except:
            return ["Traceroute failed"]

    def get_arp_table(self):
        """Get ARP table"""
        arp_entries = {}
        try:
            if self.system == "Windows":
                output, _, _ = self.execute_command("arp -a")
            else:
                output, _, _ = self.execute_command("arp -a")

            for line in output.split('\n'):
                if '.' in line and ':' in line or '-' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        ip = parts[0].replace('(', '').replace(')', '')
                        mac = parts[1] if len(parts) > 1 else "Unknown"
                        arp_entries[ip] = mac
        except:
            pass
        return arp_entries

    def display_basic_info(self):
        """Display basic network information"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"🌐  BASIC NETWORK INFORMATION")
        print(f"{'='*60}{Colors.ENDC}")

        local_ip = self.get_local_ip()
        gateway_ip = self.get_gateway_ip()
        public_ip = self.get_public_ip()

        print(
            f"{Colors.CYAN}📍 Local IP Address:{Colors.ENDC}    {Colors.GREEN}{local_ip}{Colors.ENDC}")
        print(
            f"{Colors.CYAN}🚪 Gateway IP:{Colors.ENDC}          {Colors.GREEN}{gateway_ip}{Colors.ENDC}")
        print(
            f"{Colors.CYAN}🌍 Public IP Address:{Colors.ENDC}   {Colors.GREEN}{public_ip}{Colors.ENDC}")
        print(
            f"{Colors.CYAN}💻 System:{Colors.ENDC}              {Colors.GREEN}{self.system}{Colors.ENDC}")
        print(f"{Colors.CYAN}⏰ Timestamp:{Colors.ENDC}           {Colors.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")

    def display_interface_details(self):
        """Display detailed interface information"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"🔌  NETWORK INTERFACE DETAILS")
        print(f"{'='*60}{Colors.ENDC}")

        interfaces = self.get_interface_info()
        dns_servers = self.get_dns_servers()

        for interface, info in interfaces.items():
            if info:  # Only show interfaces with information
                print(f"\n{Colors.YELLOW}Interface: {interface}{Colors.ENDC}")
                for key, value in info.items():
                    print(
                        f"  {Colors.CYAN}{key}:{Colors.ENDC} {Colors.GREEN}{value}{Colors.ENDC}")

        if dns_servers:
            print(f"\n{Colors.YELLOW}DNS Servers:{Colors.ENDC}")
            for dns in dns_servers:
                print(f"  {Colors.GREEN}{dns}{Colors.ENDC}")

    def display_network_scan(self):
        """Display network device discovery"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"🔍  NETWORK DEVICE DISCOVERY")
        print(f"{'='*60}{Colors.ENDC}")

        devices = self.discover_network_devices()

        if devices:
            print(
                f"\n{Colors.GREEN}Found {len(devices)} active devices:{Colors.ENDC}\n")
            for ip, info in devices.items():
                hostname = info.get('hostname', 'Unknown')
                print(
                    f"  {Colors.CYAN}📱 {ip:<15}{Colors.ENDC} → {Colors.YELLOW}{hostname}{Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ No devices found or scan failed{Colors.ENDC}")

    def display_port_scan(self):
        """Display port scanning results"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"🔐  PORT SCANNING")
        print(f"{'='*60}{Colors.ENDC}")

        target = input(
            f"\n{Colors.CYAN}Enter target IP (or press Enter for gateway): {Colors.ENDC}").strip()
        if not target:
            target = self.gateway_ip if self.gateway_ip else "127.0.0.1"

        print(f"\n{Colors.YELLOW}🔍 Scanning ports on {target}...{Colors.ENDC}")
        open_ports = self.scan_network_ports(target)

        if open_ports:
            print(f"\n{Colors.GREEN}Open ports found:{Colors.ENDC}")
            port_services = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
                80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
                995: "POP3S", 3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL"
            }
            for port in open_ports:
                service = port_services.get(port, "Unknown")
                print(
                    f"  {Colors.CYAN}Port {port:<6}{Colors.ENDC} → {Colors.GREEN}{service}{Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ No open ports found{Colors.ENDC}")

    def display_routing_info(self):
        """Display routing table and traceroute"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"🗺️   ROUTING INFORMATION")
        print(f"{'='*60}{Colors.ENDC}")

        print(f"\n{Colors.YELLOW}Routing Table:{Colors.ENDC}")
        routes = self.get_routing_table()
        for route in routes[:10]:  # Show first 10 routes
            if route.strip():
                print(f"  {Colors.GREEN}{route}{Colors.ENDC}")

        print(f"\n{Colors.YELLOW}Traceroute to 8.8.8.8:{Colors.ENDC}")
        trace_result = self.trace_route()
        for hop in trace_result[:8]:  # Show first 8 hops
            if hop.strip():
                print(f"  {Colors.GREEN}{hop}{Colors.ENDC}")

    def display_arp_table(self):
        """Display ARP table"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"📋  ARP TABLE (IP-MAC MAPPINGS)")
        print(f"{'='*60}{Colors.ENDC}")

        arp_entries = self.get_arp_table()
        if arp_entries:
            for ip, mac in arp_entries.items():
                print(
                    f"  {Colors.CYAN}{ip:<18}{Colors.ENDC} → {Colors.GREEN}{mac}{Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ Unable to retrieve ARP table{Colors.ENDC}")

    def display_menu(self):
        """Display main menu"""
        menu = f"""
{Colors.HEADER}╔══════════════════════════════════════════════════════════════╗
║                         NETSCOPE MENU                       ║
╠══════════════════════════════════════════════════════════════╣{Colors.ENDC}
{Colors.CYAN}║  1. 🌐  Basic Network Information                            ║
║  2. 🔌  Network Interface Details                           ║
║  3. 🔍  Network Device Discovery                            ║
║  4. 🔐  Port Scanner                                         ║
║  5. 🗺️   Routing & Traceroute                               ║
║  6. 📋  ARP Table                                            ║
║  7. 🔄  Complete Network Analysis                           ║
║  8. ❓  Help & Information                                   ║
║  9. 🚪  Exit                                                 ║{Colors.ENDC}
{Colors.HEADER}╚══════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(menu)

    def show_help(self):
        """Display help information"""
        help_text = f"""
{Colors.HEADER}{'='*60}
❓  HELP & INFORMATION
{'='*60}{Colors.ENDC}

{Colors.YELLOW}What does each option do?{Colors.ENDC}

{Colors.CYAN}1. Basic Network Information:{Colors.ENDC}
   Shows your local IP, gateway IP, public IP, and system info

{Colors.CYAN}2. Network Interface Details:{Colors.ENDC}
   Displays detailed info about network adapters, MAC addresses, DNS servers

{Colors.CYAN}3. Network Device Discovery:{Colors.ENDC}
   Scans your local network to find active devices and their hostnames

{Colors.CYAN}4. Port Scanner:{Colors.ENDC}
   Scans common ports on a target IP to identify running services

{Colors.CYAN}5. Routing & Traceroute:{Colors.ENDC}
   Shows routing table and traces the path to external servers

{Colors.CYAN}6. ARP Table:{Colors.ENDC}
   Displays IP to MAC address mappings from the ARP cache

{Colors.CYAN}7. Complete Network Analysis:{Colors.ENDC}
   Runs all analysis tools in sequence for comprehensive overview

{Colors.GREEN}💡 Tips:{Colors.ENDC}
• Run with administrator/root privileges for best results
• Some features may take time to complete (network scanning)
• Press Ctrl+C to interrupt long-running operations
"""
        print(help_text)

    def run_complete_analysis(self):
        """Run complete network analysis"""
        print(f"\n{Colors.HEADER}{'='*60}")
        print(f"🔄  COMPLETE NETWORK ANALYSIS")
        print(f"{'='*60}{Colors.ENDC}")
        print(
            f"{Colors.YELLOW}Running comprehensive network analysis...{Colors.ENDC}\n")

        self.display_basic_info()
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")

        self.display_interface_details()
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")

        self.display_network_scan()
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")

        self.display_routing_info()
        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")

        self.display_arp_table()

    def run(self):
        """Main program loop"""
        self.print_banner()

        while True:
            try:
                self.display_menu()
                choice = input(
                    f"\n{Colors.CYAN}Select an option (1-9): {Colors.ENDC}").strip()

                if choice == '1':
                    self.display_basic_info()
                elif choice == '2':
                    self.display_interface_details()
                elif choice == '3':
                    self.display_network_scan()
                elif choice == '4':
                    self.display_port_scan()
                elif choice == '5':
                    self.display_routing_info()
                elif choice == '6':
                    self.display_arp_table()
                elif choice == '7':
                    self.run_complete_analysis()
                elif choice == '8':
                    self.show_help()
                elif choice == '9':
                    print(
                        f"\n{Colors.GREEN}👋 Thank you for using NetScope! Goodbye!{Colors.ENDC}")
                    break
                else:
                    print(
                        f"\n{Colors.RED}❌ Invalid option. Please select 1-9.{Colors.ENDC}")

                if choice != '9':
                    input(
                        f"\n{Colors.CYAN}Press Enter to return to main menu...{Colors.ENDC}")
                    # Clear screen
                    os.system('cls' if self.system == 'Windows' else 'clear')

            except KeyboardInterrupt:
                print(
                    f"\n\n{Colors.YELLOW}⚠️  Operation interrupted by user{Colors.ENDC}")
                input(
                    f"{Colors.CYAN}Press Enter to return to main menu...{Colors.ENDC}")
            except Exception as e:
                print(f"\n{Colors.RED}❌ An error occurred: {str(e)}{Colors.ENDC}")
                input(f"{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")


def main():
    """Main function"""
    try:
        analyzer = NetworkAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Program terminated by user. Goodbye!{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {str(e)}{Colors.ENDC}")


if __name__ == "__main__":
    main()

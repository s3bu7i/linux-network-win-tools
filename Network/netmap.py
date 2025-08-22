#!/usr/bin/env python3
"""
NetScope Pro - Advanced Network Analysis Tool
A comprehensive network diagnostics and monitoring suite
"""

import os
import sys
import socket
import subprocess
import platform
import time
import threading
import json
import re
from datetime import datetime
from collections import defaultdict
import ipaddress

try:
    import psutil
    import requests
except ImportError:
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip",
                          "install", "psutil", "requests"])
    import psutil
    import requests


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
        self.system_info = self.get_system_info()
        self.network_interfaces = {}
        self.traffic_stats = {}
        self.monitoring = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                          NetScope Pro v2.0                      ║
║                 Advanced Network Analysis Suite                  ║
║                                                                  ║
║  Comprehensive LAN diagnostics, traffic monitoring & analysis   ║
╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.YELLOW}System: {Colors.ENDC}{self.system_info['system']} | {Colors.YELLOW}Host: {Colors.ENDC}{self.system_info['hostname']}
{Colors.YELLOW}Time: {Colors.ENDC}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        print(banner)

    def get_system_info(self):
        return {
            'system': platform.system(),
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'architecture': platform.architecture()[0]
        }

    def get_network_interfaces(self):
        """Get detailed network interface information"""
        interfaces = {}

        # Get network interfaces with psutil
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()

        for interface_name, addresses in net_if_addrs.items():
            if interface_name in net_if_stats:
                stats = net_if_stats[interface_name]
                interfaces[interface_name] = {
                    'addresses': [],
                    'is_up': stats.isup,
                    'duplex': stats.duplex,
                    'speed': stats.speed,
                    'mtu': stats.mtu
                }

                for addr in addresses:
                    addr_info = {
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast,
                        'ptp': addr.ptp
                    }
                    interfaces[interface_name]['addresses'].append(addr_info)

        self.network_interfaces = interfaces
        return interfaces

    def get_gateway_info(self):
        """Get default gateway information"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['ipconfig'], capture_output=True, text=True)
                output = result.stdout
                gateway_match = re.search(
                    r'Default Gateway[.\s]*:\s*([0-9.]+)', output)
                if gateway_match:
                    return gateway_match.group(1)
            else:
                result = subprocess.run(
                    ['ip', 'route', 'show', 'default'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if 'default via' in line:
                            return line.split('via')[1].split()[0]
        except:
            pass
        return "Unknown"

    def get_dns_servers(self):
        """Get DNS server information"""
        dns_servers = []
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['nslookup', 'google.com'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Server:' in line:
                        server = line.split(':')[-1].strip()
                        if server and server != '127.0.0.1':
                            dns_servers.append(server)
            else:
                with open('/etc/resolv.conf', 'r') as f:
                    for line in f:
                        if line.startswith('nameserver'):
                            dns_servers.append(line.split()[1])
        except:
            pass
        return dns_servers if dns_servers else ["Unknown"]

    def get_public_ip(self):
        """Get public IP address and ISP info"""
        try:
            response = requests.get('http://ipinfo.io/json', timeout=5)
            return response.json()
        except:
            try:
                response = requests.get(
                    'https://api.ipify.org?format=json', timeout=5)
                return {'ip': response.json()['ip']}
            except:
                return {'ip': 'Unable to fetch'}

    def scan_network(self, network):
        """Scan network for active devices"""
        active_devices = []
        network_obj = ipaddress.IPv4Network(network, strict=False)

        def ping_host(ip):
            try:
                if platform.system() == "Windows":
                    result = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)],
                                            capture_output=True, text=True)
                else:
                    result = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)],
                                            capture_output=True, text=True)

                if result.returncode == 0:
                    hostname = self.get_hostname(str(ip))
                    active_devices.append({
                        'ip': str(ip),
                        'hostname': hostname,
                        'response_time': self.extract_ping_time(result.stdout)
                    })
            except:
                pass

        print(f"{Colors.YELLOW}Scanning network {network}...{Colors.ENDC}")
        threads = []

        for ip in list(network_obj.hosts())[:50]:  # Limit to first 50 IPs
            thread = threading.Thread(target=ping_host, args=(ip,))
            thread.daemon = True
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join(timeout=2)

        return active_devices

    def get_hostname(self, ip):
        """Get hostname for IP address"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def extract_ping_time(self, ping_output):
        """Extract ping response time from output"""
        try:
            if platform.system() == "Windows":
                match = re.search(r'time=(\d+)ms', ping_output)
            else:
                match = re.search(r'time=(\d+\.?\d*) ms', ping_output)

            if match:
                return f"{match.group(1)}ms"
        except:
            pass
        return "N/A"

    def get_port_info(self, interface):
        """Get port and connection information"""
        connections = psutil.net_connections(kind='inet')
        interface_connections = []

        for conn in connections:
            if conn.status == 'ESTABLISHED':
                interface_connections.append({
                    'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                    'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                    'status': conn.status,
                    'pid': conn.pid
                })

        return interface_connections[:20]  # Limit to 20 connections

    def get_traffic_stats(self):
        """Get network traffic statistics"""
        net_io = psutil.net_io_counters(pernic=True)
        stats = {}

        for interface, io_stats in net_io.items():
            stats[interface] = {
                'bytes_sent': io_stats.bytes_sent,
                'bytes_recv': io_stats.bytes_recv,
                'packets_sent': io_stats.packets_sent,
                'packets_recv': io_stats.packets_recv,
                'errin': io_stats.errin,
                'errout': io_stats.errout,
                'dropin': io_stats.dropin,
                'dropout': io_stats.dropout
            }

        return stats

    def format_bytes(self, bytes_val):
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f} PB"

    def monitor_traffic(self, duration=10):
        """Monitor network traffic in real-time"""
        print(
            f"{Colors.GREEN}Monitoring network traffic for {duration} seconds...{Colors.ENDC}\n")

        initial_stats = self.get_traffic_stats()
        time.sleep(duration)
        final_stats = self.get_traffic_stats()

        print(
            f"{Colors.CYAN}{'Interface':<15} {'Sent':<12} {'Received':<12} {'Total':<12}{Colors.ENDC}")
        print("-" * 55)

        for interface in initial_stats:
            if interface in final_stats:
                sent_diff = final_stats[interface]['bytes_sent'] - \
                    initial_stats[interface]['bytes_sent']
                recv_diff = final_stats[interface]['bytes_recv'] - \
                    initial_stats[interface]['bytes_recv']
                total_diff = sent_diff + recv_diff

                if total_diff > 0:
                    print(f"{interface:<15} {self.format_bytes(sent_diff):<12} "
                          f"{self.format_bytes(recv_diff):<12} {self.format_bytes(total_diff):<12}")

    def display_network_overview(self):
        """Display comprehensive network overview"""
        self.clear_screen()
        self.print_banner()

        print(f"{Colors.HEADER}📊 NETWORK OVERVIEW{Colors.ENDC}")
        print("=" * 60)

        # Get all network information
        interfaces = self.get_network_interfaces()
        gateway = self.get_gateway_info()
        dns_servers = self.get_dns_servers()
        public_info = self.get_public_ip()

        # Display gateway information
        print(f"\n{Colors.CYAN}🌐 Gateway & Internet Connection:{Colors.ENDC}")
        print(f"   Default Gateway: {Colors.GREEN}{gateway}{Colors.ENDC}")
        print(
            f"   Public IP: {Colors.GREEN}{public_info.get('ip', 'Unknown')}{Colors.ENDC}")
        if 'org' in public_info:
            print(f"   ISP: {Colors.GREEN}{public_info['org']}{Colors.ENDC}")
        if 'city' in public_info:
            print(
                f"   Location: {Colors.GREEN}{public_info['city']}, {public_info.get('region', '')}{Colors.ENDC}")

        # Display DNS information
        print(f"\n{Colors.CYAN}🔍 DNS Configuration:{Colors.ENDC}")
        for i, dns in enumerate(dns_servers[:3], 1):
            print(f"   DNS Server {i}: {Colors.GREEN}{dns}{Colors.ENDC}")

        # Display active interfaces
        print(f"\n{Colors.CYAN}🔌 Network Interfaces:{Colors.ENDC}")
        for name, info in interfaces.items():
            if info['is_up']:
                print(f"\n   {Colors.YELLOW}Interface: {name}{Colors.ENDC}")
                print(f"   Status: {Colors.GREEN}UP{Colors.ENDC}")
                if info['speed'] > 0:
                    print(
                        f"   Speed: {Colors.GREEN}{info['speed']} Mbps{Colors.ENDC}")
                print(f"   MTU: {Colors.GREEN}{info['mtu']}{Colors.ENDC}")

                for addr in info['addresses']:
                    if addr['family'] == 'AddressFamily.AF_INET':
                        print(
                            f"   IP Address: {Colors.GREEN}{addr['address']}{Colors.ENDC}")
                        print(
                            f"   Subnet Mask: {Colors.GREEN}{addr['netmask']}{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def display_device_discovery(self):
        """Discover and display network devices"""
        self.clear_screen()
        self.print_banner()

        print(f"{Colors.HEADER}🔍 NETWORK DEVICE DISCOVERY{Colors.ENDC}")
        print("=" * 60)

        # Get local network range
        interfaces = self.get_network_interfaces()
        local_networks = []

        for name, info in interfaces.items():
            if info['is_up']:
                for addr in info['addresses']:
                    if addr['family'] == 'AddressFamily.AF_INET' and addr['address'] != '127.0.0.1':
                        try:
                            network = ipaddress.IPv4Network(
                                f"{addr['address']}/{addr['netmask']}", strict=False)
                            local_networks.append(str(network))
                        except:
                            pass

        if local_networks:
            network = local_networks[0]
            print(f"Scanning network: {Colors.CYAN}{network}{Colors.ENDC}\n")

            devices = self.scan_network(network)

            if devices:
                print(
                    f"{Colors.CYAN}{'IP Address':<15} {'Hostname':<25} {'Response Time':<12}{Colors.ENDC}")
                print("-" * 55)

                for device in devices:
                    print(
                        f"{device['ip']:<15} {device['hostname']:<25} {device['response_time']:<12}")
            else:
                print(f"{Colors.RED}No devices found on the network.{Colors.ENDC}")
        else:
            print(
                f"{Colors.RED}No suitable network interface found for scanning.{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def display_traffic_analysis(self):
        """Display traffic analysis menu"""
        while True:
            self.clear_screen()
            self.print_banner()

            print(f"{Colors.HEADER}📈 TRAFFIC ANALYSIS{Colors.ENDC}")
            print("=" * 60)

            print(f"{Colors.CYAN}1.{Colors.ENDC} Current Traffic Statistics")
            print(f"{Colors.CYAN}2.{Colors.ENDC} Real-time Traffic Monitor (10s)")
            print(f"{Colors.CYAN}3.{Colors.ENDC} Real-time Traffic Monitor (30s)")
            print(f"{Colors.CYAN}4.{Colors.ENDC} Interface-specific Analysis")
            print(f"{Colors.CYAN}5.{Colors.ENDC} Active Connections")
            print(f"{Colors.CYAN}0.{Colors.ENDC} Back to Main Menu")

            choice = input(f"\n{Colors.YELLOW}Select option: {Colors.ENDC}")

            if choice == '1':
                self.show_current_stats()
            elif choice == '2':
                self.monitor_traffic(10)
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
            elif choice == '3':
                self.monitor_traffic(30)
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
            elif choice == '4':
                self.interface_analysis()
            elif choice == '5':
                self.show_active_connections()
            elif choice == '0':
                break

    def show_current_stats(self):
        """Show current traffic statistics"""
        self.clear_screen()
        self.print_banner()

        print(f"{Colors.HEADER}📊 CURRENT TRAFFIC STATISTICS{Colors.ENDC}")
        print("=" * 60)

        stats = self.get_traffic_stats()

        print(f"{Colors.CYAN}{'Interface':<12} {'Sent':<12} {'Received':<12} {'Packets Out':<12} {'Packets In':<12}{Colors.ENDC}")
        print("-" * 70)

        for interface, data in stats.items():
            if data['bytes_sent'] > 0 or data['bytes_recv'] > 0:
                print(f"{interface:<12} {self.format_bytes(data['bytes_sent']):<12} "
                      f"{self.format_bytes(data['bytes_recv']):<12} "
                      f"{data['packets_sent']:<12} {data['packets_recv']:<12}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def interface_analysis(self):
        """Analyze specific interface"""
        interfaces = list(self.get_network_interfaces().keys())

        print(f"\n{Colors.CYAN}Available Interfaces:{Colors.ENDC}")
        for i, interface in enumerate(interfaces, 1):
            print(f"{i}. {interface}")

        try:
            choice = int(
                input(f"\n{Colors.YELLOW}Select interface number: {Colors.ENDC}"))
            if 1 <= choice <= len(interfaces):
                interface = interfaces[choice - 1]

                print(f"\n{Colors.HEADER}Analysis for {interface}:{Colors.ENDC}")

                # Show connections for this interface
                connections = self.get_port_info(interface)
                if connections:
                    print(f"\n{Colors.CYAN}Active Connections:{Colors.ENDC}")
                    print(
                        f"{'Local Address':<20} {'Remote Address':<20} {'Status':<12}")
                    print("-" * 55)

                    for conn in connections[:10]:
                        print(
                            f"{conn['local_addr']:<20} {conn['remote_addr']:<20} {conn['status']:<12}")
                else:
                    print(
                        f"{Colors.RED}No active connections found for this interface.{Colors.ENDC}")

        except (ValueError, IndexError):
            print(f"{Colors.RED}Invalid selection.{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def show_active_connections(self):
        """Show all active network connections"""
        self.clear_screen()
        self.print_banner()

        print(f"{Colors.HEADER}🔗 ACTIVE NETWORK CONNECTIONS{Colors.ENDC}")
        print("=" * 60)

        connections = psutil.net_connections(kind='inet')
        active_connections = [
            conn for conn in connections if conn.status == 'ESTABLISHED']

        if active_connections:
            print(
                f"{Colors.CYAN}{'Local Address':<22} {'Remote Address':<22} {'Status':<12} {'PID':<8}{Colors.ENDC}")
            print("-" * 70)

            for conn in active_connections[:25]:  # Show first 25 connections
                local_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
                remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"

                print(
                    f"{local_addr:<22} {remote_addr:<22} {conn.status:<12} {conn.pid or 'N/A':<8}")
        else:
            print(f"{Colors.RED}No active connections found.{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def display_diagnostics(self):
        """Display network diagnostics tools"""
        while True:
            self.clear_screen()
            self.print_banner()

            print(f"{Colors.HEADER}🔧 NETWORK DIAGNOSTICS{Colors.ENDC}")
            print("=" * 60)

            print(f"{Colors.CYAN}1.{Colors.ENDC} Ping Test")
            print(f"{Colors.CYAN}2.{Colors.ENDC} Traceroute")
            print(f"{Colors.CYAN}3.{Colors.ENDC} Port Scanner")
            print(f"{Colors.CYAN}4.{Colors.ENDC} DNS Lookup")
            print(f"{Colors.CYAN}5.{Colors.ENDC} Speed Test (Basic)")
            print(f"{Colors.CYAN}0.{Colors.ENDC} Back to Main Menu")

            choice = input(f"\n{Colors.YELLOW}Select option: {Colors.ENDC}")

            if choice == '1':
                self.ping_test()
            elif choice == '2':
                self.traceroute_test()
            elif choice == '3':
                self.port_scan()
            elif choice == '4':
                self.dns_lookup()
            elif choice == '5':
                self.speed_test()
            elif choice == '0':
                break

    def ping_test(self):
        """Perform ping test"""
        target = input(
            f"\n{Colors.YELLOW}Enter target IP/hostname: {Colors.ENDC}")
        if not target:
            return

        print(f"\n{Colors.GREEN}Pinging {target}...{Colors.ENDC}\n")

        try:
            if platform.system() == "Windows":
                result = subprocess.run(['ping', '-n', '4', target], text=True)
            else:
                result = subprocess.run(['ping', '-c', '4', target], text=True)
        except:
            print(f"{Colors.RED}Ping failed.{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def traceroute_test(self):
        """Perform traceroute test"""
        target = input(
            f"\n{Colors.YELLOW}Enter target IP/hostname: {Colors.ENDC}")
        if not target:
            return

        print(f"\n{Colors.GREEN}Tracing route to {target}...{Colors.ENDC}\n")

        try:
            if platform.system() == "Windows":
                result = subprocess.run(['tracert', target], text=True)
            else:
                result = subprocess.run(['traceroute', target], text=True)
        except:
            print(f"{Colors.RED}Traceroute failed.{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def port_scan(self):
        """Basic port scanner"""
        target = input(f"\n{Colors.YELLOW}Enter target IP: {Colors.ENDC}")
        if not target:
            return

        common_ports = [21, 22, 23, 25, 53, 80, 110,
                        143, 443, 993, 995, 3389, 5432, 3306]

        print(f"\n{Colors.GREEN}Scanning common ports on {target}...{Colors.ENDC}\n")
        print(f"{Colors.CYAN}{'Port':<6} {'Status':<8} {'Service':<12}{Colors.ENDC}")
        print("-" * 30)

        services = {21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
                    80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
                    993: 'IMAPS', 995: 'POP3S', 3389: 'RDP', 5432: 'PostgreSQL',
                    3306: 'MySQL'}

        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))

                if result == 0:
                    status = f"{Colors.GREEN}OPEN{Colors.ENDC}"
                else:
                    status = f"{Colors.RED}CLOSED{Colors.ENDC}"

                service = services.get(port, 'Unknown')
                print(f"{port:<6} {status:<15} {service:<12}")
                sock.close()
            except:
                print(f"{port:<6} {Colors.RED}ERROR{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def dns_lookup(self):
        """Perform DNS lookup"""
        target = input(f"\n{Colors.YELLOW}Enter hostname: {Colors.ENDC}")
        if not target:
            return

        try:
            ip = socket.gethostbyname(target)
            print(f"\n{Colors.GREEN}{target} resolves to: {ip}{Colors.ENDC}")

            # Reverse lookup
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"{Colors.GREEN}Reverse lookup: {hostname}{Colors.ENDC}")
            except:
                print(f"{Colors.YELLOW}Reverse lookup failed{Colors.ENDC}")

        except socket.gaierror:
            print(f"{Colors.RED}DNS lookup failed for {target}{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def speed_test(self):
        """Basic speed test"""
        print(f"\n{Colors.GREEN}Running basic connectivity test...{Colors.ENDC}")

        test_urls = [
            'http://www.google.com',
            'http://www.github.com',
            'http://www.stackoverflow.com'
        ]

        for url in test_urls:
            try:
                start_time = time.time()
                response = requests.get(url, timeout=5)
                end_time = time.time()

                response_time = (end_time - start_time) * 1000
                print(f"{url}: {Colors.GREEN}{response_time:.2f}ms{Colors.ENDC}")
            except:
                print(f"{url}: {Colors.RED}Failed{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

    def main_menu(self):
        """Display main menu"""
        while True:
            self.clear_screen()
            self.print_banner()

            print(f"{Colors.HEADER}🚀 MAIN MENU{Colors.ENDC}")
            print("=" * 60)
            print(f"{Colors.CYAN}1.{Colors.ENDC} 📊 Network Overview")
            print(f"{Colors.CYAN}2.{Colors.ENDC} 🔍 Device Discovery")
            print(f"{Colors.CYAN}3.{Colors.ENDC} 📈 Traffic Analysis")
            print(f"{Colors.CYAN}4.{Colors.ENDC} 🔧 Network Diagnostics")
            print(f"{Colors.CYAN}5.{Colors.ENDC} ⚙️  System Information")
            print(f"{Colors.CYAN}0.{Colors.ENDC} ❌ Exit")

            choice = input(
                f"\n{Colors.YELLOW}Select option [0-5]: {Colors.ENDC}")

            if choice == '1':
                self.display_network_overview()
            elif choice == '2':
                self.display_device_discovery()
            elif choice == '3':
                self.display_traffic_analysis()
            elif choice == '4':
                self.display_diagnostics()
            elif choice == '5':
                self.show_system_info()
            elif choice == '0':
                print(
                    f"\n{Colors.GREEN}Thank you for using NetScope Pro!{Colors.ENDC}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Invalid option. Please try again.{Colors.ENDC}")
                time.sleep(1)

    def show_system_info(self):
        """Show detailed system information"""
        self.clear_screen()
        self.print_banner()

        print(f"{Colors.HEADER}💻 SYSTEM INFORMATION{Colors.ENDC}")
        print("=" * 60)

        # System info
        print(f"\n{Colors.CYAN}System Details:{Colors.ENDC}")
        print(
            f"   OS: {Colors.GREEN}{self.system_info['system']}{Colors.ENDC}")
        print(
            f"   Platform: {Colors.GREEN}{self.system_info['platform']}{Colors.ENDC}")
        print(
            f"   Hostname: {Colors.GREEN}{self.system_info['hostname']}{Colors.ENDC}")
        print(
            f"   Architecture: {Colors.GREEN}{self.system_info['architecture']}{Colors.ENDC}")

        # Memory info
        memory = psutil.virtual_memory()
        print(f"\n{Colors.CYAN}Memory Information:{Colors.ENDC}")
        print(
            f"   Total: {Colors.GREEN}{self.format_bytes(memory.total)}{Colors.ENDC}")
        print(
            f"   Available: {Colors.GREEN}{self.format_bytes(memory.available)}{Colors.ENDC}")
        print(
            f"   Used: {Colors.GREEN}{self.format_bytes(memory.used)}{Colors.ENDC}")
        print(f"   Percentage: {Colors.GREEN}{memory.percent}%{Colors.ENDC}")

        # CPU info
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"\n{Colors.CYAN}CPU Information:{Colors.ENDC}")
        print(f"   Cores: {Colors.GREEN}{cpu_count}{Colors.ENDC}")
        print(f"   Usage: {Colors.GREEN}{cpu_percent}%{Colors.ENDC}")
        print(
            f"   Processor: {Colors.GREEN}{self.system_info['processor'] or 'Unknown'}{Colors.ENDC}")

        # Disk info
        disk = psutil.disk_usage('/')
        print(f"\n{Colors.CYAN}Disk Information:{Colors.ENDC}")
        print(
            f"   Total: {Colors.GREEN}{self.format_bytes(disk.total)}{Colors.ENDC}")
        print(
            f"   Used: {Colors.GREEN}{self.format_bytes(disk.used)}{Colors.ENDC}")
        print(
            f"   Free: {Colors.GREEN}{self.format_bytes(disk.free)}{Colors.ENDC}")
        print(
            f"   Percentage: {Colors.GREEN}{(disk.used/disk.total)*100:.1f}%{Colors.ENDC}")

        # Network summary
        net_stats = self.get_traffic_stats()
        total_sent = sum(stats['bytes_sent'] for stats in net_stats.values())
        total_recv = sum(stats['bytes_recv'] for stats in net_stats.values())

        print(f"\n{Colors.CYAN}Network Summary:{Colors.ENDC}")
        print(
            f"   Total Sent: {Colors.GREEN}{self.format_bytes(total_sent)}{Colors.ENDC}")
        print(
            f"   Total Received: {Colors.GREEN}{self.format_bytes(total_recv)}{Colors.ENDC}")
        print(
            f"   Active Interfaces: {Colors.GREEN}{len([i for i in self.get_network_interfaces().values() if i['is_up']])}{Colors.ENDC}")

        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")


def main():
    """Main function to run the network analyzer"""
    try:
        analyzer = NetworkAnalyzer()
        analyzer.main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program interrupted by user.{Colors.ENDC}")
        print(f"{Colors.GREEN}Thank you for using NetScope Pro!{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}An error occurred: {e}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Please report this issue if it persists.{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()

import socket
import concurrent.futures
import argparse
import re
import logging

# Setup logging
logging.basicConfig(filename="port_scanner.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Common ports and their services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-ALT"
}

# Validate IP address


def is_valid_ip(ip):
    regex = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(regex, ip) is not None

# Scan a single port


def scan_port(ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            try:
                # Attempt to grab the banner
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(1024).decode().strip()
            except:
                banner = "Unknown"
            service = COMMON_PORTS.get(port, "Unknown Service")
            logging.info(f"Port {port}: OPEN ({service}) - Banner: {banner}")
            return port, service, banner
    except:
        return None

# Main scanning function


def scan_ports(ip, ports, timeout, threads):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_port = {executor.submit(
            scan_port, ip, port, timeout): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                open_ports.append(result)
    return open_ports


# Main entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("--start-port", type=int, default=1,
                        help="Start of port range (default: 1)")
    parser.add_argument("--end-port", type=int, default=65535,
                        help="End of port range (default: 65535)")
    parser.add_argument("--timeout", type=float, default=0.5,
                        help="Timeout for each connection (default: 0.5s)")
    parser.add_argument("--threads", type=int, default=100,
                        help="Number of threads to use (default: 100)")
    parser.add_argument("--output", type=str, default="scan_results.txt",
                        help="File to save results (default: scan_results.txt)")
    args = parser.parse_args()

    # Validate IP
    if not is_valid_ip(args.ip):
        print("Invalid IP address. Please provide a valid IPv4 address.")
        exit(1)

    # Generate port range
    ports = range(args.start_port, args.end_port + 1)
    print(f"Scanning {args.ip} from port {
          args.start_port} to {args.end_port}...")

    # Perform scan
    open_ports = scan_ports(args.ip, ports, args.timeout, args.threads)

    # Output results
    with open(args.output, "w") as f:
        for port, service, banner in open_ports:
            result = f"Port {port}: OPEN ({service}) - Banner: {banner}"
            print(result)
            f.write(result + "\n")

    print(f"Scan complete. Results saved to {args.output}.")

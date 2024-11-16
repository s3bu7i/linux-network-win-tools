import time
import sys
import requests
import socket
import argparse
import threading
from queue import Queue
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

# Lock for printing thread-safe messages
print_lock = threading.Lock()

# Save results globally
found_subdomains = set()
stop_program = False


def timeout_handler():
    """Handle timeout to stop the program."""
    global stop_program
    stop_program = True  # Signal threads to stop
    print("\n[INFO] Timeout reached! Exiting...")
    sys.exit(0)  # Terminate the program


def dns_resolver(subdomain):
    """Attempt to resolve DNS for the subdomain."""
    if stop_program:
        return
    try:
        ip = socket.gethostbyname(subdomain)
        with print_lock:
            print(f"[FOUND] {subdomain} -> {ip}")
        found_subdomains.add(subdomain)
    except socket.gaierror:
        pass


def scrape_html(domain, sources):
    """Scrape HTML pages for potential subdomains."""
    if stop_program:
        return
    headers = {'User-Agent': 'Mozilla/5.0'}
    for source in sources:
        try:
            url = f"https://{domain}.{source}"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    parsed_url = urlparse(link['href'])
                    if parsed_url.netloc and domain in parsed_url.netloc:
                        subdomain = parsed_url.netloc
                        dns_resolver(subdomain)
        except requests.RequestException:
            continue


def brute_force_subdomains(domain, wordlist, threads=10):
    """Brute force subdomains using a wordlist."""
    if stop_program:
        return

    def worker():
        while not q.empty() and not stop_program:
            sub = q.get()
            subdomain = f"{sub}.{domain}"
            dns_resolver(subdomain)
            q.task_done()

    q = Queue()
    for sub in wordlist:
        q.put(sub.strip())

    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()

    q.join()


def passive_discovery(domain):
    """Use APIs for passive subdomain enumeration."""
    if stop_program:
        return
    apis = {
        "crt.sh": f"https://crt.sh/?q=%25.{domain}&output=json",
        "virustotal": f"https://www.virustotal.com/vtapi/v2/domain/report?apikey=YOUR_API_KEY&domain={domain}",
    }

    for api_name, api_url in apis.items():
        handle_api_response(api_name, api_url)


def handle_api_response(api_name, api_url):
    """Handle the API response for passive discovery."""
    if stop_program:
        return
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            if api_name == "crt.sh":
                process_crtsh_response(response)
            elif api_name == "virustotal":
                process_virustotal_response(response)
    except Exception as e:
        print(f"[ERROR] {api_name} API failed: {e}")


def process_crtsh_response(response):
    """Process the response from crt.sh API."""
    results = response.json()
    for entry in results:
        subdomain = entry['name_value']
        dns_resolver(subdomain)


def process_virustotal_response(response):
    """Process the response from VirusTotal API."""
    results = response.json()
    for subdomain in results.get('subdomains', []):
        dns_resolver(subdomain)


def save_results(filename):
    """Save discovered subdomains to a file."""
    with open(filename, "w") as f:
        for subdomain in sorted(found_subdomains):
            f.write(subdomain + "\n")
    print(f"[SAVED] Results saved to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Subdomain Enumerator with Timeout")
    parser.add_argument("-d", "--domain", required=True,
                        help="Target domain (e.g., example.com)")
    parser.add_argument(
        "-w", "--wordlist", help="Wordlist for brute force (default: subdomains.txt)")
    parser.add_argument("-t", "--threads", type=int, default=10,
                        help="Number of threads (default: 10)")
    parser.add_argument(
        "-o", "--output", help="Output file to save results (default: results.txt)")
    parser.add_argument("--scrape", action="store_true",
                        help="Scrape HTML sources for subdomains")
    parser.add_argument("--passive", action="store_true",
                        help="Use passive enumeration (API integrations)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Maximum runtime in seconds (default: 300)")
    args = parser.parse_args()

    domain = args.domain
    wordlist_file = args.wordlist or "subdomains.txt"
    output_file = args.output or "results.txt"
    timeout = args.timeout

    try:
        with open(wordlist_file, "r") as f:
            wordlist = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Wordlist file not found: {wordlist_file}")
        return

    # Set up timeout
    timer = threading.Timer(timeout, timeout_handler)
    timer.start()

    print(f"[INFO] Starting enumeration for domain: {domain}")
    print(f"[INFO] Timeout set to {timeout} seconds.")

    try:
        if args.passive:
            print("[INFO] Performing passive enumeration...")
            passive_discovery(domain)

        print("[INFO] Performing brute force enumeration...")
        brute_force_subdomains(domain, wordlist, args.threads)

        if args.scrape:
            print("[INFO] Scraping HTML for additional subdomains...")
            scrape_html(domain, ["com", "org", "net"])

    except KeyboardInterrupt:
        print("\n[INFO] Detected Ctrl+C. Stopping the program...")

    finally:
        timer.cancel()  # Cancel the timer if the program finishes early
        save_results(output_file)
        print("[INFO] Program completed successfully.")


if __name__ == "__main__":
    main()

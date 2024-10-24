import requests
import threading
import argparse
from queue import Queue
import os

# Disable SSL warnings for simplicity
requests.packages.urllib3.disable_warnings()

# Global variables
FOUND_DIRECTORIES = []
q = Queue()
lock = threading.Lock()


def send_request(url):
    """
    Sends a GET request to the given URL and returns the status code and response length.
    """
    try:
        response = requests.get(
            url, allow_redirects=False, timeout=5, verify=True)
        return response.status_code, len(response.content)
    except requests.exceptions.RequestException:
        return None, None


def scan_directory(url, wordlist):
    """
    Scans the given URL for directories/files listed in the wordlist.
    """
    global FOUND_DIRECTORIES
    with open(wordlist, 'r') as f:
        for line in f:
            directory = line.strip()
            if directory:
                full_url = f"{url}/{directory}"
                status_code, content_length = send_request(full_url)

                if status_code and status_code in [200, 301, 302]:
                    with lock:
                        FOUND_DIRECTORIES.append(full_url)
                        print(
                            f"[+] Found: {full_url} (Status: {status_code}, Length: {content_length})")

                    # Recursively scan the discovered directory if it's not a file
                    if status_code == 200:
                        q.put(full_url)


def worker(wordlist):
    """
    Thread worker function to process URLs from the queue.
    """
    while not q.empty():
        current_url = q.get()
        scan_directory(current_url, wordlist)
        q.task_done()


def start_bruteforce(base_url, wordlist, threads):
    """
    Starts the brute force process with a base URL, wordlist, and number of threads.
    """
    # Add the base URL to the queue for recursive scanning
    q.put(base_url)

    # Create and start worker threads
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(wordlist,))
        t.daemon = True
        t.start()

    # Wait for all threads to complete
    q.join()


def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Recursive Web Directory Brute Force Tool")
    parser.add_argument(
        "url", help="The base URL to start the scan (e.g., http://example.com)")
    parser.add_argument("-w", "--wordlist",
                        help="Path to the wordlist file", required=True)
    parser.add_argument("-t", "--threads", type=int, default=10,
                        help="Number of threads (default: 10)")

    args = parser.parse_args()

    # Validate the wordlist file
    if not os.path.exists(args.wordlist):
        print("Error: Wordlist file does not exist.")
        return

    # Start the brute force scan
    print(f"Starting recursive brute force on {
          args.url} with {args.threads} threads...")
    start_bruteforce(args.url, args.wordlist, args.threads)


if __name__ == "__main__":
    main()


# Subdomain Enumerator

This project is a Python-based subdomain enumeration tool that uses multiple techniques to find subdomains for a given domain. It incorporates brute-forcing, passive discovery via APIs, and HTML scraping to find subdomains.

## Features
- **Brute-force Subdomain Enumeration**: Uses a wordlist to try common subdomains.
- **Passive Enumeration**: Leverages APIs like crt.sh and VirusTotal to gather known subdomains.
- **HTML Scraping**: Scrapes known sources to discover subdomains.
- **Timeout Support**: The program can be configured to stop after a specified timeout.
- **Threading**: Implements threading for faster enumeration by utilizing multiple threads.
- **Graceful Shutdown**: Handles `Ctrl+C` interrupts gracefully and saves progress.

## Requirements
- Python 3.x
- `requests` (for API calls and HTTP requests)
- `bs4` (for HTML parsing)
- `socket` (for DNS resolution)

You can install the required libraries using `pip`:
```
pip install requests beautifulsoup4
```

## Usage

Run the program with the following syntax:
```bash
python sub_enum.py -d <domain> -w <wordlist> -o <output_file> --timeout <timeout> [--scrape] [--passive]
```

### Arguments:
- `-d`, `--domain`: Target domain to enumerate subdomains (e.g., `example.com`).
- `-w`, `--wordlist`: Path to a wordlist file for brute-force enumeration (default: `subdomains.txt`).
- `-o`, `--output`: Output file to save discovered subdomains (default: `results.txt`).
- `--timeout`: Timeout in seconds (default: 300 seconds).
- `--scrape`: Enable HTML scraping for additional subdomains.
- `--passive`: Use passive enumeration via APIs (e.g., crt.sh, VirusTotal).

### Example:

To run the tool with a timeout of 15 seconds, brute-force subdomains using a wordlist, and save results to `output.txt`, use the following command:
```bash
python sub_enum.py -d hackthissite.org -w subdomains.txt -o output.txt --timeout 15
```

### Timeout:
You can specify a timeout for the program using the `--timeout` argument. The program will automatically stop once the timeout is reached.

### Output:
Discovered subdomains are saved in the specified output file, which will contain one subdomain per line.


# Recursive Web Directory Brute Force Tool

## Overview

This Python-based tool is designed to brute force web directories and files using a recursive scanning method. It attempts to discover hidden directories on a web server by testing URL paths from a given wordlist. When a directory is found, it recursively searches within that directory for more files or subdirectories.

## Features

- **Multithreaded Scanning**: Supports concurrent directory scanning using threading for faster performance.
- **Recursive Scanning**: Once a directory is found, the tool recursively scans it for subdirectories or files.
- **Wordlist-based Brute Force**: Utilizes a wordlist to test for potential directory and file names.
- **Handles HTTP Status Codes**: Checks for common status codes like 200 (OK), 301, 302 (redirects) to determine if a resource exists.

## Usage

Run the tool using the following command:
```bash
python bruteforce.py <base-url> -w <wordlist-file> -t <threads>
```
i add some wordlist file, big, med and small size
### Command-Line Arguments

- `url`: The base URL to start the scan (e.g., `http://example.com`).
- `-w` or `--wordlist`: Path to the wordlist file (required).
- `-t` or `--threads`: Number of threads to use for scanning (optional, default is 10).

### Example

```bash
python bruteforce.py http://example.com -w /path/to/wordlist.txt -t 20
```

### Sample Output
```
Starting recursive brute force on http://example.com with 10 threads...
[+] Found: http://example.com/admin (Status: 200, Length: 1489)
[+] Found: http://example.com/config (Status: 301, Length: 0)
[+] Found: http://example.com/uploads (Status: 200, Length: 5823)
[+] Found: http://example.com/admin/login (Status: 200, Length: 947)
```

### Wordlist

Use any wordlist to test for directories. A popular choice is the [SecLists](https://github.com/danielmiessler/SecLists) wordlist:
```bash
git clone https://github.com/danielmiessler/SecLists.git
python bruteforce.py http://example.com -w SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 10
```

## Notes

- Ensure that you have permission to run directory brute force scans on the target website.
- The tool disables SSL verification for simplicity, but you can modify the script to enable verification if needed.


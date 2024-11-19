
# Advanced Hash Buster

An advanced command-line tool to crack various types of hashes (MD5, SHA1, SHA256, etc.) using APIs and wordlist-based cracking.

## Features

- **Crack Hashes**: Supports cracking hashes from a single hash, file, or directory.
- **Multi-threading**: Improves cracking performance using threads.
- **API Integration**: Utilizes multiple external APIs to find plaintext values for hashes.
- **Wordlist Cracking**: Allows custom wordlist-based cracking for faster results.
- **Caching**: Caches previous results for faster repeated lookups.
- **Directory Search**: Scans files within a directory for potential hashes and attempts to crack them.

## Requirements

- Python 3.x
- Required Python libraries:
  - `requests` (for API requests)
  - `tqdm` (for progress bars)
  - `hashlib` (for wordlist-based cracking)

You can install the required libraries with the following command:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/advanced-hash-buster.git
   cd advanced-hash-buster
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. **Crack a Single Hash**

To crack a single hash, use the following command:
```bash
python3 main.py single <hash>
```

**Example:**
```bash
python3 main.py single 5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
```
This will attempt to crack the hash `5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8` (which is the MD5 hash for "password").

### 2. **Crack Hashes from a File**

To crack hashes stored in a file, use the following command:
```bash
python3 main.py file <file_path> -o <output_file> -t <threads>
```

**Example:**
```bash
python3 main.py file hashes.txt -o cracked_hashes.txt -t 8
```
- This will read the hashes from `hashes.txt`, crack them using 8 threads, and save the results to `cracked_hashes.txt`.

### 3. **Crack Hashes from a Directory**

To scan files in a directory for hashes and crack them, use the following command:
```bash
python3 main.py dir <directory_path> -o <output_file> -t <threads>
```

**Example:**
```bash
python3 main.py dir ./hash_files -o directory_cracked_hashes.txt -t 8
```
- This will scan all files in the `./hash_files` directory, extract hashes, crack them using 8 threads, and save the results to `directory_cracked_hashes.txt`.

## Example Hash File Format

If you are providing a file with hashes, the file should contain one hash per line. Here’s an example `hashes.txt` file:

```txt
5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8  # md5: password
2c6ee24b09816a6f14f95d1698b24ead  # md5: 123456
d8578edf8c3cec6f1d8a7f5d2f9e9e27  # md5: qwerty
```

### Example Output (cracked_hashes.txt)

After cracking the hashes, the output file (`cracked_hashes.txt`) will contain the cracked hash values:

```txt
5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8:password
2c6ee24b09816a6f14f95d1698b24ead:123456
d8578edf8c3cec6f1d8a7f5d2f9e9e27:qwerty
```

## Advanced Usage

- **Specify the Number of Threads**: By default, the program uses 4 threads for cracking. You can specify a different number of threads using the `-t` option.
  ```bash
  python3 main.py file hashes.txt -o cracked_hashes.txt -t 8
  ```

- **Output File**: You can specify the name of the output file using the `-o` option.
  ```bash
  python3 main.py file hashes.txt -o custom_output.txt
  ```

- **Caching**: The program caches previously cracked results to avoid repeated API requests and speed up the process. The cache is stored in `hash_cache.json`.

## FAQ

### 1. **What hash types are supported?**
Currently, the program supports the following hash types:
- MD5
- SHA1
- SHA256
- SHA384
- SHA512

### 2. **What if the hash is not cracked?**
If the program cannot crack a hash using APIs or the wordlist, it will return `[-] Hash was not found in any database.`

### 3. **How do I update the wordlist?**
To improve cracking speed, you can replace the default wordlist (`common_wordlist.txt`) with your custom wordlist. Just make sure it's in the same directory as the program, or specify the path in the `wordlist_crack` function.

### 4. **Can I use my own APIs?**
Yes, you can integrate your own APIs for cracking hashes by modifying the `crackers.py` file. Simply add the API logic inside the corresponding functions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


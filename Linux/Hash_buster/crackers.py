import os
import re
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from hash_utils import detect_hash_type, load_cache, save_cache, wordlist_crack

CACHE_FILE = "hash_cache.json"
cache = load_cache(CACHE_FILE)

# API-based cracking functions


def gamma(hashvalue, hashtype):
    try:
        response = requests.get(
            f'https://www.nitrxgen.net/md5db/{hashvalue}', timeout=10)
        return response.text if response.text else None
    except requests.exceptions.RequestException:
        return None


def beta(hashvalue, hashtype):
    try:
        response = requests.get(
            f'https://hashtoolkit.com/reverse-hash/?hash={hashvalue}', timeout=10).text
        match = re.search(r'/generate-hash/\?text=(.*?)"', response)
        return match.group(1) if match else None
    except requests.exceptions.RequestException:
        return None

# Master cracking function


def crack_hash(hashvalue):
    if hashvalue in cache:
        return cache[hashvalue]

    hash_type = detect_hash_type(hashvalue)
    if hash_type == "unknown":
        return None

    # Attempt wordlist cracking first
    result = wordlist_crack(hashvalue, hash_type, "common_wordlist.txt")
    if result:
        cache[hashvalue] = result
        save_cache(CACHE_FILE, cache)
        return result

    # Attempt API cracking
    for api_func in [gamma, beta]:
        result = api_func(hashvalue, hash_type)
        if result:
            cache[hashvalue] = result
            save_cache(CACHE_FILE, cache)
            return result

    return None


def process_single_hash(hashvalue):
    result = crack_hash(hashvalue)
    if result:
        print(f"[+] Cracked {hashvalue}: {result}")
    else:
        print(f"[-] Could not crack {hashvalue}")


def process_file_hashes(filepath, output_file, threads):
    with open(filepath, "r") as f:
        hashes = [line.strip() for line in f]

    results = {}
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for hashvalue in tqdm(hashes, desc="Processing hashes"):
            result = executor.submit(crack_hash, hashvalue).result()
            if result:
                results[hashvalue] = result

    with open(output_file, "w") as f:
        for hashvalue, result in results.items():
            f.write(f"{hashvalue}:{result}\n")

    print(f"[+] Results saved to {output_file}")


def process_directory_hashes(directory, output_file, threads):
    found_hashes = set()
    for root, _, files in os.walk(directory):
        for filename in files:
            with open(os.path.join(root, filename), "r") as f:
                content = f.read()
                matches = re.findall(r"[a-f0-9]{32,128}", content)
                found_hashes.update(matches)

    print(f"[+] Found {len(found_hashes)} hashes in directory")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = {
            hashvalue: executor.submit(crack_hash, hashvalue).result()
            for hashvalue in tqdm(found_hashes, desc="Processing hashes")
        }

    with open(output_file, "w") as f:
        for hashvalue, result in results.items():
            if result:
                f.write(f"{hashvalue}:{result}\n")

    print(f"[+] Results saved to {output_file}")

import hashlib
import json
import os


def detect_hash_type(hashvalue):
    length_map = {
        32: "md5",
        40: "sha1",
        64: "sha256",
        96: "sha384",
        128: "sha512"
    }
    return length_map.get(len(hashvalue), "unknown")


def wordlist_crack(hashvalue, hash_type, wordlist):
    hash_func = getattr(hashlib, hash_type, None)
    if not hash_func:
        return None

    try:
        with open(wordlist, "r") as wl:
            for word in wl:
                word = word.strip()
                if hash_func(word.encode()).hexdigest() == hashvalue:
                    return word
    except FileNotFoundError:
        pass
    return None


def load_cache(cache_file):
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache_file, cache):
    with open(cache_file, "w") as f:
        json.dump(cache, f)

#!/usr/bin/python3

import os
import sys
import argparse
from tqdm import tqdm
from collections import Counter
from datetime import datetime

LOG_FILE = "input_log.txt"


def log_input(file_path, formats, analyze):
    """Logs the user input and selected options to a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] FILE: {
        file_path}, FORMATS: {formats}, ANALYZE: {analyze}\n"
    try:
        with open(LOG_FILE, "a") as log:
            log.write(log_entry)
    except Exception as e:
        print(f"Warning: Could not write to log file: {e}", file=sys.stderr)


def format_byte(byte, fmt):
    """Converts a byte into the specified format."""
    if fmt == "hex":
        return f"{byte:02x}"
    elif fmt == "binary":
        return f"{byte:08b}"
    elif fmt == "octal":
        return f"{byte:03o}"
    elif fmt == "decimal":
        return f"{byte:03d}"
    else:
        raise ValueError(f"Unsupported format: {fmt}")


def analyze_file(file_path):
    """Analyzes the file's byte statistics."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        byte_count = Counter(data)
        total_bytes = sum(byte_count.values())
        most_common = byte_count.most_common(5)

        print("\n=== File Analysis ===")
        print(f"Total Bytes: {total_bytes}")
        print(f"Unique Bytes: {len(byte_count)}")
        print("Most Common Bytes (Top 5):")
        for byte, count in most_common:
            print(f"  Byte {byte:02x} ({chr(byte) if 32 <=
                  byte <= 127 else '.'}): {count} times")
        print("=====================\n")
    except Exception as e:
        print(f"Error in file analysis: {e}", file=sys.stderr)


def dump_file(file_path, formats):
    """Reads and displays file content in the specified formats."""
    try:
        with open(file_path, "rb") as f:
            filesize = os.path.getsize(file_path)
            print(f"Size of {file_path}: {filesize} bytes - 0x{filesize:08x}")

            # Reading file in chunks and displaying progress
            n = 0
            with tqdm(total=filesize, unit="B", unit_scale=True, desc="Reading File") as progress:
                while chunk := f.read(16):
                    line_output = []
                    for fmt in formats:
                        line = " ".join([format_byte(byte, fmt)
                                        for byte in chunk])
                        line_output.append(line)

                    # ASCII interpretation
                    ascii_line = "".join(
                        [chr(byte) if 32 <= byte <= 127 else "." for byte in chunk])
                    print(f"{n * 16:08x}  {'  '.join(line_output)}  |{ascii_line}|")
                    n += 1
                    progress.update(len(chunk))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Advanced File Dump Utility with Multi-Format Support, Analysis, and Logging.")
    parser.add_argument("FILE", help="Path to the file to be dumped", type=str)
    parser.add_argument("-f", "--formats", nargs="+", choices=["hex", "binary", "octal", "decimal"], default=["hex"],
                        help="Specify one or more formats: hex, binary, octal, decimal")
    parser.add_argument(
        "-a", "--analyze", help="Analyze the file and display byte statistics", action="store_true")
    args = parser.parse_args()

    # Log the user input and selected options
    log_input(args.FILE, args.formats, args.analyze)

    # Check if the file exists
    if not os.path.isfile(args.FILE):
        print(f"Error: File '{args.FILE}' does not exist!", file=sys.stderr)
        sys.exit(1)

    # Perform file analysis if requested
    if args.analyze:
        analyze_file(args.FILE)

    # Perform file dump in the selected formats
    dump_file(args.FILE, args.formats)


if __name__ == "__main__":
    main()

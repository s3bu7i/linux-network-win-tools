import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Advanced Hash Buster")

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    # Single hash cracking
    single_parser = subparsers.add_parser("single", help="Crack a single hash")
    single_parser.add_argument("hash", help="The hash to crack")

    # File-based cracking
    file_parser = subparsers.add_parser(
        "file", help="Crack hashes from a file")
    file_parser.add_argument(
        "filepath", help="Path to the file containing hashes")
    file_parser.add_argument(
        "-o", "--output", help="Output file for results", default="cracked_hashes.txt")
    file_parser.add_argument("-t", "--threads", type=int,
                             help="Number of threads to use", default=4)

    # Directory-based hash extraction
    dir_parser = subparsers.add_parser(
        "dir", help="Extract and crack hashes from a directory")
    dir_parser.add_argument(
        "directory", help="Directory containing files with hashes")
    dir_parser.add_argument(
        "-o", "--output", help="Output file for results", default="cracked_directory_hashes.txt")
    dir_parser.add_argument("-t", "--threads", type=int,
                            help="Number of threads to use", default=4)

    return parser.parse_args()

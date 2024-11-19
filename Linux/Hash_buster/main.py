#!/usr/bin/env python3

from cli import parse_args
from crackers import process_single_hash, process_file_hashes, process_directory_hashes


def main():
    args = parse_args()

    if args.command == "single":
        process_single_hash(args.hash)
    elif args.command == "file":
        process_file_hashes(args.filepath, args.output, args.threads)
    elif args.command == "dir":
        process_directory_hashes(args.directory, args.output, args.threads)
    else:
        print("Invalid command. Use -h or --help for usage instructions.")


if __name__ == "__main__":
    main()

import psutil
import json
import platform
from datetime import datetime


def fetch_process_details():
    """
    Fetch details of all running processes on the system.
    Returns:
        List of dictionaries with process information.
    """
    process_list = []

    # Attributes to gather for each process
    # Platform-specific adjustments
    base_attributes = [
        'pid', 'name', 'status', 'cpu_percent', 'memory_percent', 'create_time',
        'exe', 'cwd', 'cmdline', 'username', 'num_threads', 'open_files',
        'threads', 'memory_info', 'cpu_times'
    ]

    # Add Linux/UNIX-specific attributes
    if platform.system() != "Windows":
        base_attributes.extend(
            ['num_fds', 'cpu_num', 'terminal', 'gids', 'uids'])

    for proc in psutil.process_iter(attrs=base_attributes):
        try:
            process_info = proc.info

            # Convert inaccessible or complex objects to strings for JSON compatibility
            for key, value in process_info.items():
                if isinstance(value, (bytes, list, dict, set, tuple)):
                    process_info[key] = str(value)

            process_list.append(process_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # Ignore inaccessible processes

    return process_list


def save_to_json(data, filename="processes.json"):
    """
    Save the process details to a JSON file.
    Args:
        data: The data to save.
        filename: Name of the file to save the data.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"[INFO] Process details saved to {filename}")


def main(output_file):
    """
    Main function to fetch and save process details.
    Args:
        output_file: File to save the process details.
    """
    print("[INFO] Fetching process details...")
    processes = fetch_process_details()

    # Print process details in the console
    for process in processes[:5]:  # Limit to first 5 processes for readability
        print("\n" + "=" * 80)
        for key, value in process.items():
            print(f"{key}: {value}")
        print("=" * 80)

    # Save details to JSON file
    if output_file:
        save_to_json(processes, output_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch and save system process details.")
    parser.add_argument(
        "-o", "--output", help="Output JSON file name (e.g., processes.json)", default="processes.json")
    args = parser.parse_args()

    main(output_file=args.output)

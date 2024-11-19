import os
import hashlib
import json

BASELINE_FILE = 'baseline.json'

def hash_file(file_path):
    """Generate SHA-256 hash of the given file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(4096), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def create_baseline(directory):
    """Create a baseline of file hashes for the given directory."""
    baseline = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_hash:
                baseline[file_path] = file_hash
    with open(BASELINE_FILE, 'w') as f:
        json.dump(baseline, f, indent=4)
    print(f"Baseline created and saved to {BASELINE_FILE}")

def load_baseline():
    """Load the baseline file."""
    try:
        with open(BASELINE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Baseline file {BASELINE_FILE} not found. Please create a baseline first.")
        return None

def check_file_discrepancies(directory, baseline):
    """Check for discrepancies between current files and the baseline."""
    discrepancies = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            current_hash = hash_file(file_path)
            if file_path in baseline:
                if current_hash != baseline[file_path]:
                    discrepancies.append((file_path, 'modified'))
                del baseline[file_path]
            else:
                discrepancies.append((file_path, 'new'))
    return discrepancies

def verify_integrity(directory):
    """Verify the integrity of files in the given directory against the baseline."""
    baseline = load_baseline()
    if baseline is None:
        return

    discrepancies = check_file_discrepancies(directory, baseline)

    for file_path in baseline:
        discrepancies.append((file_path, 'deleted'))

    if discrepancies:
        print("Discrepancies found:")
        for file_path, status in discrepancies:
            print(f"{file_path}: {status}")
    else:
        print("No discrepancies found. All files are intact.")

def generate_report(directory):
    """Generate a report of the current file hashes in the given directory."""
    report = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_hash:
                report[file_path] = file_hash
    report_file = './report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=4)
    print(f"Report generated and saved to {report_file}")

def main_menu():
    """Main menu for user interaction."""
    while True:
        print("---------------------------------------")
        print("Welcome to the File System Integrity Checker")
        print("---------------------------------------")
        print("1. Create Baseline")
        print("2. Verify Integrity")
        print("3. Generate Report")
        print("4. Quit")
        choice = input("Select an option (1-4): ")

        if choice == '1':
            dir_path = input("Enter the directory to create a baseline: ")
            create_baseline(dir_path)
        elif choice == '2':
            dir_path = input("Enter the directory to verify integrity: ")
            verify_integrity(dir_path)
        elif choice == '3':
            dir_path = input("Enter the directory to generate a report: ")
            generate_report(dir_path)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main_menu()
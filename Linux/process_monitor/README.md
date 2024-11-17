
# Process Details Fetcher

This Python script retrieves information about all running processes on the system and saves them in a JSON file.

## Features:
- Fetches details of all active processes, including process IDs, memory usage, CPU usage, open files, threads, and more.
- Platform-specific details are adjusted for different operating systems (Linux/Unix vs. Windows).
- Saves the process details to a JSON file for further analysis.
- Displays a limited preview of the first few processes in the console for quick inspection.

## Requirements:
- Python 3.x
- `psutil` library for process information.

### Install Required Libraries:
If you don't have the `psutil` library installed, you can install it via `pip`:

```bash
pip install psutil
```

## Usage:

### Command-Line Interface (CLI):
Run the script from the terminal with the following command:

```bash
python process_monitor.py --output <output_file.json>
```

Where:
- `<output_file.json>` is the name of the JSON file where process details will be saved (default is `processes.json` if not provided).

### Example:

```bash
python process_monitor.py --output my_processes.json
```

This will fetch the process details and save them to `my_processes.json`.

## Output:
The JSON file will contain an array of process details, where each entry includes attributes such as:
- `pid`: Process ID
- `name`: Name of the process
- `status`: Current status of the process (e.g., running, sleeping)
- `cpu_percent`: CPU usage percentage
- `memory_percent`: Memory usage percentage
- `create_time`: Time the process was created
- `exe`: Path to the executable
- `cwd`: Current working directory
- `cmdline`: Command line used to start the process
- `username`: The user running the process
- `num_threads`: Number of threads
- `open_files`: List of open files by the process
- `cpu_times`: CPU times of the process

## Example Output in JSON:

```json
[
    {
        "pid": 1234,
        "name": "python",
        "status": "running",
        "cpu_percent": 5.4,
        "memory_percent": 2.3,
        "create_time": "2024-11-17 12:30:00",
        "exe": "/usr/bin/python3",
        "cwd": "/home/user/project",
        "cmdline": ["python3", "script.py"],
        "username": "user",
        "num_threads": 4,
        "open_files": ["file1.txt", "file2.txt"],
        "cpu_times": {"user": 2.4, "system": 1.2}
    },
]
```

## Notes:
- Some processes may not be accessible depending on the user permissions. These processes are skipped.
- Only the first 5 processes are printed to the console for readability.
- I encrypt output file, because that informations is my own computer :D
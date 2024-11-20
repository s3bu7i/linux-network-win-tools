
# File Type Identification Tool

This is a Python-based CLI application for identifying file types using the `libmagic` library, with an enhanced user interface powered by `rich`.

# Features

- Identify the file type and detailed metadata of a single file.
- Analyze all files in a directory with batch processing.
- Save the analysis results to a `.csv` file.
- Interactive and visually appealing CLI using the `rich` library.

# Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/s3bu7i/linux-and-network-tools/edit/main/Linux/File_type_identification
   cd File-type-identification
   ```

2. Create and activate a virtual environment:
   ```bash
   python - m venv venv
   source venv/bin/activate    # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the tool:
   ```bash
   python main.py
   ```

2. Follow the on-screen prompts to:
   - Analyze a single file.
   - Analyze all files in a directory.
   - Save results to a file (optional).

## Dependencies

- Python 3.8 or higher
- `python-magic-bin`
- `rich`

## File Structure

```
.
├── main.py           # Main script
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make changes and commit: `git commit -m 'Added a new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.






# OSINT Tool

## Overview
The OSINT Tool is a command-line application designed to perform various Open Source Intelligence (OSINT) tasks, such as gathering domain information, IP geolocation, email validation, social media username lookups, and Google search results. It stores the results in a SQLite database and saves them as text files for easy access.

## Features
- **Domain Information**: Fetch WHOIS data for a given domain.
- **IP Geolocation**: Retrieve geolocation information for a specified IP address using an external API.
- **Email Validation**: Check the validity of an email address and verify if its domain exists.
- **Social Media Username Lookup**: Check the existence of a username across popular social media platforms.
- **Google Search**: Perform a Google search and display the top results.
- **View Previous Results**: Access previously saved results from the database.

## Requirements
To run the OSINT Tool, ensure you have the following Python libraries installed:

- `requests`
- `whois`
- `socket`
- `sqlite3` (built-in)
- `json` (built-in)
- `beautifulsoup4`
- `re` (built-in)
- `os` (built-in)
- `datetime` (built-in)

You can install the required libraries using pip:

```bash
pip install -r requirements.txt

```

## Usage
1. Clone or download the repository.
2. Navigate to the directory containing the script.
3. Run the script using Python:

```bash
python main.py
```

4. Follow the prompts to perform various OSINT tasks.

## Data Storage
The tool creates a folder named `data` to store:
- A SQLite database named `osint_results.db` where results are saved.
- Text files for each query result, named in the format: `<osint_type>_<query>.txt`.


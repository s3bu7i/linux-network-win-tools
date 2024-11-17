
# Keylogger and Server Communication Project

This project consists of two Python scripts: a **keylogger client** and a **server**. The keylogger captures keystrokes and clipboard data, encrypts them using the `cryptography` library, and sends them to a remote server. The server receives the encrypted data, decrypts it, and logs the information.

---

## Features

### Keylogger (`keylogger.py`)
- Captures keystrokes and clipboard data using `pynput` and `pandas`.
- Encrypts captured data with a symmetric key (Fernet encryption).
- Sends encrypted data to a configured remote server.

### Server (`server.py`)
- Listens for incoming connections from the keylogger client.
- Receives and decrypts the data using the same encryption key.
- Logs the decrypted data into a file for analysis.

---

## Requirements

1. **Python 3.6+**
2. Required libraries:
   - `cryptography`
   - `pynput`
   - `pandas`

Install dependencies using:
```bash
pip install cryptography pynput pandas
```

---

## Setup

### 1. Generate an Encryption Key
Run the following script to generate a Fernet encryption key:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

Save the generated key securely.

---

### 2. Configuration
Create a `config.json` file with the following structure:
```json
{
    "server_address": "192.168.100.28:53",
    "encryption_key": "YOUR_GENERATED_KEY_HERE"
}
```

Replace `"YOUR_GENERATED_KEY_HERE"` with the key generated in step 1.

---

### 3. Run the Server
Run the `server.py` script to start listening for incoming connections:
```bash
python server.py
```

### 4. Run the Keylogger
Run the `keylogger.py` script on the client machine:
```bash
python keylogger.py
```

---

## Notes

- Ensure the encryption key matches on both the keylogger and server.
- Use this project **ethically** and only in environments where you have explicit authorization.

---

## Security Recommendations

- Avoid hardcoding sensitive information in scripts.
- Store the encryption key securely, such as in environment variables or a secure file.
- Use non-standard ports to avoid conflicts with existing services.
- Enable logging to monitor script activity.

---

## Disclaimer

This project is for **educational purposes only**. Unauthorized use of keylogging or data interception tools is **illegal** and unethical. Always obtain proper consent before deployment.

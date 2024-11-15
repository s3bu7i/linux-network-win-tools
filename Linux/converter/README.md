
# **Advanced File Dump Utility**

## **Overview**
This Python script is a versatile file dump utility designed to read and display the contents of a file in multiple formats, such as hexadecimal, binary, octal, and decimal. It includes features such as byte-level analysis, ASCII interpretation, logging, and progress tracking for an enhanced user experience.

---

## **Features**
1. **Multi-Format Support**:
   - Display file content in formats: `hex`, `binary`, `octal`, and `decimal`.
2. **File Analysis**:
   - Provides byte-level statistics, including the most common bytes and their frequencies.
3. **ASCII Interpretation**:
   - Shows the ASCII representation of bytes when possible.
4. **Logging**:
   - Records user inputs (file path, selected formats, and analysis option) into a log file (`input_log.txt`).
5. **Progress Tracking**:
   - Displays progress while reading large files using a progress bar.

---

## **Requirements**
- Python 3.7 or later
- Dependencies:
  - `tqdm` (for progress bar)

Install dependencies using:
```bash
pip install tqdm
```

---

## **Usage**
Run the script with the required arguments as follows:

```bash
python3 advanced_dump.py FILE [OPTIONS]
```

### **Arguments**
- **`FILE`**: Path to the file you want to process.

### **Options**
| Option         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `-f`, `--formats` | Specify one or more formats: `hex`, `binary`, `octal`, `decimal`. Defaults to `hex`. |
| `-a`, `--analyze` | Perform byte-level analysis of the file.                                 |

---

## **Examples**

### 1. **Dump File in Hexadecimal Format** (default):
```bash
python3 advanced_dump.py example.bin
```

### 2. **Dump File in Binary and Octal Formats**:
```bash
python3 advanced_dump.py example.bin -f binary octal
```

### 3. **Analyze File Content**:
```bash
python3 advanced_dump.py example.bin -a
```

### 4. **Dump File in All Formats and Analyze**:
```bash
python3 advanced_dump.py example.bin -f hex binary octal decimal -a
```

---

## **Features in Detail**

### **File Dump**
- Displays file content in user-specified formats.
- Displays the ASCII equivalent of bytes where possible.
- Prints output in an organized and readable format.

### **File Analysis**
- Provides the total number of bytes in the file.
- Shows the number of unique bytes.
- Lists the 5 most common bytes and their frequencies.

### **Logging**
- Logs all user inputs (file path, selected formats, and analysis flag) with a timestamp in the `input_log.txt` file.

### **Error Handling**
- Checks for file existence and handles exceptions during file operations gracefully.

---

## **Output Example**

### **Hex Dump Example**:
```plaintext
Size of example.bin: 1024 bytes - 0x00000400
00000000  4f 6e 63 65 20 75 70 6f 6e 20 61 20 74 69 6d 65   |Once upon a time|
00000010  2e 20 54 68 65 72 65 20 77 61 73 20 61 20 6c 61   |. There was a la|
...
```

### **Analysis Example**:
```plaintext
=== File Analysis ===
Total Bytes: 1024
Unique Bytes: 50
Most Common Bytes (Top 5):
  Byte 20 (' '): 300 times
  Byte 61 ('a'): 150 times
  Byte 74 ('t'): 120 times
  Byte 65 ('e'): 110 times
  Byte 6e ('n'): 100 times
=====================
```

---

## **Log File**
All user inputs and options are recorded in `input_log.txt` with timestamps:
```plaintext
[2024-11-15 14:30:01] FILE: example.bin, FORMATS: ['hex'], ANALYZE: True
```

---



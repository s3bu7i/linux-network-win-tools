# 🌟 Bandit CTF Walkthrough 🌟

A complete guide to solving the Bandit wargame from OverTheWire.org

---

## 🚀 Getting Started

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
```

---

## 🎯 Level Solutions

### 🔹 Bandit 0 → 1  
**Password:** `ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If`
```bash
# No commands needed, just connect to bandit0
```

### 🔹 Bandit 1 → 2  
**Password:** `263JGJPfgU6LtdEvgfWU1XP5yac29mFx`
```bash
cat ./-
```

### 🔹 Bandit 2 → 3  
**Password:** `MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx`
```bash
cat "spaces in this filename"
```

### 🔹 Bandit 3 → 4  
**Password:** `2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ`
```bash
cat inhere/...Hiding-From-You
```

### 🔹 Bandit 4 → 5  
**Password:** `4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw`
```bash
file ./* | grep "ASCII" | awk -F: '{print $1}' | xargs cat
```

### 🔹 Bandit 5 → 6  
**Password:** `HWasnPhtq9AVKe0dmk45nxy20cvUa6EG`
```bash
find . -type f -size 1033c ! -executable -exec cat {} \;
```

### 🔹 Bandit 6 → 7  
**Password:** `morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj`
```bash
find / -type f -user bandit7 -group bandit6 -size 33c 2>/dev/null | xargs cat
```

### 🔹 Bandit 7 → 8  
**Password:** `dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc`
```bash
grep "millionth" data.txt
```

### 🔹 Bandit 8 → 9  
**Password:** `4CKMh1JI91bUIZZPXDqGanal4xvAg0JM`
```bash
sort data.txt | uniq -u
```

### 🔹 Bandit 9 → 10  
**Password:** `FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey`
```bash
strings data.txt | grep "===" | tail -n 1 | awk '{print $NF}'
```

### 🔹 Bandit 10 → 11  
**Password:** `dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr`
```bash
base64 -d data.txt
```

### 🔹 Bandit 11 → 12  
**Password:** `7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4`
```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

### 🔹 Bandit 12 → 13  
**Password:** `FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn`
```bash
# Multiple decompression steps required (gzip, bzip2, tar, etc.)
# See full solution in the original file or above sections
```

### 🔹 Bandit 13 → 14  
**Password:** `MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS`
```bash
ssh -i sshkey.private bandit14@localhost
cat /etc/bandit_pass/bandit14
```

### 🔹 Bandit 14 → 15  
**Password:** `8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo`
```bash
echo "MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS" | nc localhost 30000
```

### 🔹 Bandit 15 → 16  
**Password:** `kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx`
```bash
openssl s_client -connect localhost:30001
# Then paste the previous password
```

### 🔹 Bandit 16 → 17  
**Password:** `EReVavePLFHtFlFsjn3hyzMlvSuSAcRD`
```bash
# Find SSL port with nmap, then:
openssl s_client -quiet -connect localhost:31790
# Save the private key and use it to SSH
```

### 🔹 Bandit 17 → 18  
**Password:** `x2gLTTjFwMOhQ8oWNbMN362QKxfRqGlO`
```bash
diff passwords.old passwords.new | grep ">"
```

### 🔹 Bandit 18 → 19  
**Password:** `cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8`
```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 -t "/bin/sh"
cat readme
```

### 🔹 Bandit 19 → 20  
**Password:** `0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO`
```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

---

Happy hacking! 🚩

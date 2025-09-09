# RS-TOOL
A SIMPLE RECON SCANNER TOOL by ~harsh gupta


<img width="1843" height="370" alt="image" src="https://github.com/user-attachments/assets/1e89c3d9-2c95-4262-861e-68c7f5bf770e" />


---

> **RS TOOL** is a simple yet powerful reconnaissance automation tool by Harsh Gupta, designed to streamline the process of information gathering during penetration testing and bug bounty hunting.

---

## 🚀 Features

- **Subdomain Enumeration**: Discover subdomains using customizable wordlists.
- **Port Scanning**: Quickly identify open ports on the target.
- **Directory Searching**: Find hidden files and directories with dirsearch-like functionality.
- **JSON Output**: Save scan results in structured JSON format for further analysis.
- **All-in-One CLI**: Run multiple recon modules with a single command.
- **Extensible**: Easily add new modules and customize scans via command-line flags.

---

## 🖥️ Demo

```shell
python3 main.py -d testphp.vulnweb.com --subdomains --ports --dirsearch -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -o results.json
```


---

## 🛠️ Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/cazy8/RS-TOOL.git
   cd RS-TOOL
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

---

## ⚙️ Usage

```shell
python3 main.py -d <target-domain> [options]
```

### **Options**

| Option                 | Description                                               |
|------------------------|-----------------------------------------------------------|
| `-d <domain>`          | Target domain to scan (Required)                          |
| `--subdomains`         | Enable subdomain enumeration                              |
| `--ports`              | Enable port scanning                                      |
| `--dirsearch`          | Enable directory brute-forcing                            |
| `-w <wordlist>`        | Path to wordlist for subdomain/dirsearch modules          |
| `-o <output.json>`     | Output results to specified JSON file                     |

**Example:**
```shell
python3 main.py -d testphp.vulnweb.com --subdomains --ports --dirsearch -w /usr/share/wordlists/seclists/Discovery/DNS/namelist.txt -o results.json
```

---

## 📂 Output

- Results are displayed in the terminal and can be exported in JSON for further processing and reporting.

---

## 🤝 Contributing

Contributions are welcome! Please submit issues or pull requests for enhancements, bug fixes, or new modules.

---

## 👤 Author

- **Harsh Gupta**
- [GitHub Profile](https://github.com/cazy8)

---

## ⚠️ Disclaimer

This tool is intended for educational purposes and authorized security testing only. Do not use it on targets you do not have permission to test.

---

*Happy recon!*

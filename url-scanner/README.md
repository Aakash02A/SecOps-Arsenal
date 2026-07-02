# URL Scanner

This tool acts as a simple URL safety checker. It performs static regex pattern analysis to identify suspicious URL characteristics and uses the VirusTotal API to check the URL's reputation among security vendors.

## Features

1. **Static Pattern Checking:**
   - Detects if an IP address is used instead of a standard domain name.
   - Flags unusually long URLs or URLs with excessive subdomains.
   - Checks for unencrypted `http://` traffic.
   - Looks for basic obfuscation techniques (like `@` symbols in the domain part).

2. **Reputation Checking:**
   - Queries the VirusTotal v3 API.
   - Returns the number of security vendors that flag the URL as malicious, suspicious, or harmless.

## Prerequisites

Requires the `requests` library:

```bash
pip install requests
```

*(Optional but recommended)* You will need a **VirusTotal API Key** to use the reputation checking feature. You can get a free API key by signing up at [VirusTotal](https://www.virustotal.com/).

## Usage

Basic static pattern check:

```bash
python url_scanner.py "http://192.168.1.100/login.php"
```

With VirusTotal reputation check (passing the key directly):

```bash
python url_scanner.py "https://example.com" --api-key "YOUR_API_KEY"
```

With VirusTotal reputation check (using an environment variable):

```bash
# Linux / macOS
export VT_API_KEY="YOUR_API_KEY"
python url_scanner.py "https://example.com"

# Windows (Command Prompt)
set VT_API_KEY=YOUR_API_KEY
python url_scanner.py "https://example.com"

# Windows (PowerShell)
$env:VT_API_KEY="YOUR_API_KEY"
python url_scanner.py "https://example.com"
```

# Basic Recon Tools

This directory contains simple reconnaissance scripts to gather information about domains and IP addresses. 

## Included Tools

- `dns_lookup.py`: Perform basic DNS queries.
- `ip_info.py`: Fetch geolocation and AS information for an IP address.
- `whois_lookup.py`: Perform WHOIS queries to find domain registration details.
- `nmap_scanner.py`: A basic wrapper around Nmap for port scanning, service version detection, and OS fingerprinting.

## Prerequisites

For the Nmap wrapper, ensure you have Nmap installed on your system and the `python-nmap` module:

```bash
pip install python-nmap
```

*(Note: Nmap must also be installed on your host OS and accessible in your PATH).*

## Usage Example

```bash
# Basic Nmap Scan
python nmap_scanner.py 192.168.1.1 -p 22,80,443 -sV

# JSON output
python nmap_scanner.py scanme.nmap.org -p 80 --json
```

## ⚠️ Disclaimer
Only use these tools on systems and networks you own or have explicit authorization to scan.

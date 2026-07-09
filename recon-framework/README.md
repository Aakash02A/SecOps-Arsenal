# Recon Framework

Reconnaissance is the most critical phase of a penetration test. The more surface area an attacker can uncover, the higher the chance of finding a vulnerability. 

This tool is a multi-threaded Python framework designed to automate the two most common web recon tasks: finding hidden subdomains and uncovering hidden directories on a web server. It acts as a lightweight, combined alternative to tools like `ffuf`, `gobuster`, or `Amass`.

## Features

- **Multi-Threading**: Utilizes Python's `ThreadPoolExecutor` to send concurrent requests, vastly speeding up the enumeration process.
- **Subdomain Enumeration**: Performs DNS resolution to see if a subdomain exists (e.g., prepending a wordlist to `.target.com`).
- **Directory Brute-Forcing**: Sends HTTP GET requests to common paths to discover hidden administrative panels, backups, or configuration files (ignoring 404 Not Found responses).

## Prerequisites

Requires the `requests` library:

```bash
pip install requests
```

## Usage

You must specify a target domain, a wordlist file, and which modules to run (`--subdomains`, `--directories`, or both). 

A small sample `wordlist.txt` is included in this folder for testing.

### Subdomain Enumeration

```bash
python recon.py example.com -w wordlist.txt --subdomains
```

### Directory Brute-Forcing

```bash
python recon.py example.com -w wordlist.txt --directories
```

### Run Both Simultaneously with Custom Threads

Run both modules and increase the thread count to 20 for faster execution:

```bash
python recon.py example.com -w wordlist.txt --subdomains --directories -t 20
```

**⚠️ DISCLAIMER: Only run this tool against infrastructure you own or have explicit authorization to scan. Aggressive scanning can cause high load on target servers.**

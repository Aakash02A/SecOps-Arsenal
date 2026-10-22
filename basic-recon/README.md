# Basic Reconnaissance Tools

A collection of Python-based reconnaissance utilities for information gathering during security assessments and penetration tests.

---

## Overview

Reconnaissance is the critical first phase of any security assessment. Before you can test a system's defenses, you must understand its attack surface—what domains are registered, what IP addresses respond, what ports are open, and what services are running.

This toolkit provides four essential reconnaissance utilities that automate the tedious process of manual information gathering:

1. **DNS Lookup** - Query DNS records to understand a domain's infrastructure
2. **WHOIS Lookup** - Discover domain registration and ownership details
3. **IP Information** - Geolocate IP addresses and identify their network operators
4. **Nmap Scanner** - Discover open ports, services, and operating systems

These tools are designed for security professionals, penetration testers, and students learning offensive security techniques. They provide both command-line interfaces for quick queries and importable Python APIs for integration into larger security frameworks.

**Use Cases:**
- **Penetration Testing**: Gather intelligence during the reconnaissance phase
- **Threat Hunting**: Investigate suspicious domains and IP addresses
- **Asset Discovery**: Map your organization's external-facing infrastructure
- **Incident Response**: Quickly profile malicious domains/IPs during active incidents

---

## How It Works

Each tool in this suite follows a consistent design pattern:

### Architecture

```
┌──────────────────┐
│   CLI Interface  │  (Argparse-based command-line arguments)
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Core Function   │  (run_dns_lookup, run_whois, run_ip_info, run_nmap_scan)
│  (importable)    │
└────────┬─────────┘
         │
┌────────▼─────────┐
│  External API    │  (DNS resolvers, WHOIS servers, ipapi.co, Nmap engine)
└────────┬─────────┘
         │
┌────────▼─────────┐
│  Parsed Output   │  (Structured JSON or human-readable text)
└──────────────────┘
```

### Tool-Specific Workflows

**DNS Lookup (`dns_lookup.py`):**
- Uses `dnspython` library to query authoritative DNS servers
- Queries 7 common record types: A, AAAA, MX, NS, TXT, CNAME, SOA
- Returns results as structured dictionary or formatted text

**WHOIS Lookup (`whois_lookup.py`):**
- Uses `python-whois` library to query WHOIS servers
- Parses registration dates, registrar, name servers, and contact emails
- Handles regional WHOIS server variations automatically

**IP Information (`ip_info.py`):**
- Performs reverse DNS lookup using Python's `socket` library
- Queries **ipapi.co** (free API) for geolocation and ASN data
- Falls back gracefully if API is unreachable

**Nmap Scanner (`nmap_scanner.py`):**
- Wraps the native `nmap` binary using `python-nmap` library
- Supports port specification, service version detection, and OS fingerprinting
- Requires Nmap to be installed on the host system

---

## Features

### DNS Lookup
- ✅ Query 7 record types (A, AAAA, MX, NS, TXT, CNAME, SOA)
- ✅ Selective querying (e.g., only A and MX records)
- ✅ JSON output for automation
- ✅ Importable API for integration

### WHOIS Lookup
- ✅ Domain registration details (registrar, dates, name servers)
- ✅ Contact email extraction
- ✅ Raw WHOIS output available
- ✅ JSON output for automation
- ✅ Importable API for integration

### IP Information
- ✅ Reverse DNS (hostname resolution)
- ✅ Geolocation (city, region, country, coordinates)
- ✅ ASN and organization identification
- ✅ JSON output for automation
- ✅ Importable API for integration

### Nmap Scanner
- ✅ Custom port specification
- ✅ Service version detection (`-sV`)
- ✅ OS fingerprinting (`-O`)
- ✅ JSON output for automation
- ✅ Importable API for integration

---

## Prerequisites

### Python Requirements
- **Python**: 3.11 or higher

### Python Dependencies

```bash
# For DNS lookups
pip install dnspython

# For WHOIS lookups
pip install python-whois

# For IP information (geolocation)
pip install requests

# For Nmap wrapper
pip install python-nmap
```

Or install all at once from the root repository:

```bash
pip install -r requirements.txt
```

### System Requirements

**For Nmap Scanner Only:**
- **Nmap** must be installed on your system and accessible in your PATH

**Installation:**

```bash
# Windows
# Download installer from https://nmap.org/download.html

# Linux (Debian/Ubuntu)
sudo apt-get install nmap

# macOS
brew install nmap

# Verify installation
nmap --version
```

---

## Installation

### Step 1: Install Python Dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

Or install specific dependencies:

```bash
pip install dnspython python-whois requests python-nmap
```

### Step 2: Install Nmap (for scanner only)

See **System Requirements** section above.

### Step 3: Verify Installation

```bash
# Test DNS lookup
python basic-recon/dns_lookup.py example.com

# Test WHOIS lookup
python basic-recon/whois_lookup.py example.com

# Test IP info
python basic-recon/ip_info.py 8.8.8.8

# Test Nmap scanner (requires Nmap installed)
python basic-recon/nmap_scanner.py scanme.nmap.org -p 80
```

---

## Usage

### DNS Lookup

**Query all common DNS record types:**

```bash
python dns_lookup.py example.com
```

**Query specific record types:**

```bash
python dns_lookup.py example.com -t A MX NS
```

**JSON output:**

```bash
python dns_lookup.py example.com --json
```

---

### WHOIS Lookup

**Basic WHOIS query:**

```bash
python whois_lookup.py example.com
```

**JSON output:**

```bash
python whois_lookup.py github.com --json
```

---

### IP Information

**Look up IP geolocation and ASN:**

```bash
python ip_info.py 8.8.8.8
```

**JSON output:**

```bash
python ip_info.py 1.1.1.1 --json
```

---

### Nmap Scanner

**Basic scan (default ports):**

```bash
python nmap_scanner.py 192.168.1.1
```

**Scan specific ports:**

```bash
python nmap_scanner.py scanme.nmap.org -p 22,80,443
```

**Scan port range:**

```bash
python nmap_scanner.py 192.168.1.1 -p 1-1000
```

**Service version detection:**

```bash
python nmap_scanner.py scanme.nmap.org -p 80 -sV
```

**OS fingerprinting (requires root/admin):**

```bash
# Linux/macOS
sudo python nmap_scanner.py 192.168.1.1 -O

# Windows (run terminal as Administrator)
python nmap_scanner.py 192.168.1.1 -O
```

**JSON output:**

```bash
python nmap_scanner.py scanme.nmap.org -p 80 --json
```

**Combined options:**

```bash
python nmap_scanner.py scanme.nmap.org -p 22,80,443 -sV --json
```

---

## Output & Interpretation

### DNS Lookup Output

```
[+] DNS Records for: example.com
      A: 93.184.216.34
   AAAA: 2606:2800:220:1:248:1893:25c8:1946
     MX: 0 .
     NS: a.iana-servers.net., b.iana-servers.net.
    TXT: "v=spf1 -all", "wgyf8z8cgvm2qmxpnbnldrcltvk4xqfn"
  CNAME: Error: The DNS response does not contain an answer to the question
    SOA: a.iana-servers.net. noc.dns.icann.org. 2024010100 7200 3600 1209600 3600
```

**Key Fields:**
- **A**: IPv4 address(es)
- **AAAA**: IPv6 address(es)
- **MX**: Mail exchange servers (number is priority, lower = higher priority)
- **NS**: Authoritative name servers
- **TXT**: Text records (often used for SPF, DKIM, verification tokens)
- **CNAME**: Canonical name (alias records)
- **SOA**: Start of Authority (zone information)

---

### WHOIS Lookup Output

```
[+] Domain:      example.com
    Registrar:   RESERVED-Internet Assigned Numbers Authority
    Created:     1995-08-14 04:00:00
    Expires:     2024-08-13 04:00:00
    Name Servers: a.iana-servers.net, b.iana-servers.net
    Emails:      N/A
```

**Key Fields:**
- **Registrar**: Company that registered the domain
- **Created/Expires**: Registration lifecycle dates
- **Name Servers**: DNS servers authoritative for the domain
- **Emails**: Contact emails (often redacted by privacy protection)

---

### IP Information Output

```
[+] IP:       8.8.8.8
    Hostname: dns.google
    City:     Mountain View
    Region:   California
    Country:  US
    ASN:      AS15169
    Org:      Google LLC
```

**Key Fields:**
- **Hostname**: Reverse DNS name (PTR record)
- **City/Region/Country**: Physical location of the IP
- **ASN**: Autonomous System Number (routing identifier)
- **Org**: Organization that owns the IP block

---

### Nmap Scanner Output

```
[+] Host: scanme.nmap.org (State: up)
  Protocol: tcp
    Port: 22	State: open	Service: ssh OpenSSH 7.4
    Port: 80	State: open	Service: http Apache 2.4.7
    Port: 443	State: closed	Service: https
```

**Key Fields:**
- **State (host)**: `up` (responding) or `down` (not responding)
- **State (port)**: `open` (service running), `closed` (no service), `filtered` (firewall blocking)
- **Service**: Detected service name and version (with `-sV` flag)

---

## Security Considerations

### Legal & Ethical Warnings

⚠️ **CRITICAL**: Reconnaissance activities can be interpreted as hostile or illegal.

- **Authorization Required**: Only perform reconnaissance on:
  - Systems you own
  - Systems you have explicit written permission to test
  - Public infrastructure explicitly designated for testing (e.g., `scanme.nmap.org`)
- **CFAA Compliance (US)**: Unauthorized scanning may violate the Computer Fraud and Abuse Act
- **GDPR Considerations (EU)**: WHOIS queries may expose personal data—handle responsibly
- **Corporate Policies**: Scanning corporate networks without IT approval may result in termination

### Operational Security

- **Rate Limiting**: 
  - DNS queries: Most resolvers allow ~100 queries/minute
  - WHOIS queries: Many registrars rate-limit at 10-50 queries/minute
  - ipapi.co: Free tier allows 1,000 requests/day
  - Excessive queries may result in temporary IP bans
- **Network Visibility**: All reconnaissance activities are logged:
  - DNS queries are logged by resolvers
  - WHOIS queries are logged by registrars
  - Nmap scans trigger IDS/IPS alerts
  - Use from trusted networks only
- **Data Privacy**: Reconnaissance results may contain sensitive information (email addresses, internal IPs). Store securely and follow data retention policies

### Tool-Specific Risks

**Nmap Scanner:**
- **IDS/IPS Detection**: Aggressive scans (`-sV`, `-O`) generate significant network noise
- **Network Disruption**: Scanning fragile systems may cause crashes or service degradation
- **Legal Risk**: Port scanning is explicitly illegal in some jurisdictions without authorization

**IP Information:**
- **Third-Party Dependency**: Relies on ipapi.co API—their terms of service apply
- **Data Accuracy**: Geolocation is approximate (~city-level accuracy)

---

## Limitations & Known Issues

### DNS Lookup Limitations
1. **DNS Blocking**: Some networks block external DNS queries (port 53 UDP)
2. **DNSSEC**: Does not validate DNSSEC signatures
3. **Record Type Support**: Only queries 7 common record types (no CAA, SSHFP, etc.)
4. **Timeout**: Uses default DNS timeout (~5 seconds). Slow resolvers may fail

### WHOIS Lookup Limitations
1. **Privacy Protection**: WHOIS privacy services hide registrant details
2. **Regional Variations**: WHOIS format varies by TLD (.com vs .uk vs .jp)
3. **Rate Limiting**: Aggressive querying may result in temporary bans
4. **Incomplete Data**: Some registrars return minimal information

### IP Information Limitations
1. **API Dependency**: Requires internet access to ipapi.co (no offline mode)
2. **Geolocation Accuracy**: City-level accuracy only (~10-50km radius)
3. **Private IPs**: Cannot geolocate RFC1918 private IPs (10.x, 172.16.x, 192.168.x)
4. **Rate Limiting**: Free tier limited to 1,000 requests/day

### Nmap Scanner Limitations
1. **Requires Nmap**: Must have Nmap installed separately (not a pure Python solution)
2. **Privilege Requirements**: OS detection (`-O`) requires root/admin access
3. **Simplified Interface**: Does not expose all 80+ Nmap options
4. **Performance**: Slower than running Nmap directly (Python wrapper overhead)

### Known Issues
- **Windows PATH Issues**: If Nmap is installed but not in PATH, `python-nmap` will fail. Add Nmap to PATH manually
- **Firewall False Positives**: Personal firewalls may block outbound DNS/WHOIS queries
- **IPv6 Support**: Limited testing on IPv6-only networks

### What These Tools Do NOT Do
- ❌ Exploit vulnerabilities (reconnaissance only)
- ❌ Bypass authentication or authorization
- ❌ Perform active attacks (DoS, brute force, etc.)
- ❌ Decrypt encrypted traffic
- ❌ Provide real-time monitoring (single-query only)

---

## Related Tools & Further Reading

### SecOps-Arsenal Integration

- **`recon-framework/`**: Advanced multi-tool reconnaissance framework that orchestrates these utilities
- **`threat-intel/`**: Enrich reconnaissance findings with threat intelligence (IOC checking)
- **`web-scanner/`**: Perform deeper web application reconnaissance after discovering HTTP services
- **`packet-sniffer/`**: Capture network traffic from discovered services for further analysis

### External Tools

- **Amass**: Advanced DNS enumeration and subdomain discovery ([https://github.com/OWASP/Amass](https://github.com/OWASP/Amass))
- **theHarvester**: OSINT gathering tool for emails, subdomains, IPs ([https://github.com/laramies/theHarvester](https://github.com/laramies/theHarvester))
- **Shodan CLI**: Search engine for internet-connected devices ([https://cli.shodan.io/](https://cli.shodan.io/))
- **Masscan**: Ultra-fast port scanner ([https://github.com/robertdavidgraham/masscan](https://github.com/robertdavidgraham/masscan))

### Learning Resources

- [PTES Technical Guidelines - Intelligence Gathering](http://www.pentest-standard.org/index.php/Intelligence_Gathering)
- [OWASP Testing Guide - Information Gathering](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/README)
- [Nmap Official Documentation](https://nmap.org/book/man.html)
- [DNS RFC 1035](https://www.ietf.org/rfc/rfc1035.txt)

### Python API Usage

All tools provide importable functions for integration into larger scripts:

```python
from basic_recon.dns_lookup import run_dns_lookup
from basic_recon.whois_lookup import run_whois
from basic_recon.ip_info import run_ip_info
from basic_recon.nmap_scanner import run_nmap_scan

# DNS lookup
dns_data = run_dns_lookup("example.com")
print(dns_data["records"]["A"])

# WHOIS lookup
whois_data = run_whois("example.com")
print(whois_data["registrar"])

# IP info
ip_data = run_ip_info("8.8.8.8")
print(ip_data["country"])

# Nmap scan
scan_results = run_nmap_scan("scanme.nmap.org", "-p 80 -sV")
print(scan_results)
```

### Contributing

See the root [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding new reconnaissance utilities
- Improving error handling for edge cases
- Adding IPv6 support
- Implementing offline caching for API data
- Performance optimization for large-scale scans

---

**Last Updated:** 2026-10-16  
**Tested With:** Python 3.11, 3.12, 3.13 | Nmap 7.80+

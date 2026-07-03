# Red Team Tools (Educational)

This module explores the offensive side of cybersecurity. By understanding how attackers recon networks and create lures, defenders can build better detections and training programs.

**⚠️ DISCLAIMER: These tools are provided strictly for educational purposes and authorized penetration testing. Do not use these against systems or personnel without explicit consent.**

## Included Tools

1. **`smb_enum.py`**: A script to enumerate Server Message Block (SMB) shares on a target machine. This mimics how attackers find open file shares and misconfigured permissions on internal networks.
2. **`phish_gen.py`**: Generates a realistic HTML phishing email template. This is useful for internal security awareness training and authorized Red Team social engineering engagements.

## Prerequisites

For the SMB Enumerator, you need the `pysmb` library:

```bash
pip install pysmb
```

## Usage

### 1. SMB Share Enumeration

Attempt to list the shares on a target IP. By default, it tries to connect as the `guest` user with no password (null session).

```bash
# Basic Null/Guest Session Enum
python smb_enum.py 192.168.1.100

# Authenticated Enum
python smb_enum.py 192.168.1.100 -u Administrator -p "AdminPass123" -d "MYDOMAIN"
```

### 2. Phishing Template Generator

Generate a simulated phishing email to test email filters or train employees.

```bash
python phish_gen.py "employee@company.com" "http://evil-landing-page.com/login" -o test_phish.html
```

You can then open `test_phish.html` in your browser to see how the crafted email looks.

# Security Automation Playbooks

This directory contains standalone Python scripts that act as **Security Playbooks**. In a real-world Security Operations Center (SOC) or within a SOAR (Security Orchestration, Automation, and Response) platform, playbooks are automated actions taken in response to a detected threat.

## Included Playbooks

These scripts detect your operating system (Windows/Linux) and execute the appropriate native commands.

1. **`block_ip.py`**: Automatically blocks a malicious IP address at the host firewall level (`netsh advfirewall` on Windows, `iptables` on Linux).
2. **`lock_account.py`**: Disables a local user account if it exhibits suspicious behavior (e.g., too many failed logons, brute force detected).
3. **`email_alert.py`**: Sends an automated email alert to a security analyst or team regarding a security event.

## Usage

**⚠️ CAUTION:** The `block_ip.py` and `lock_account.py` scripts make active changes to your system's firewall and user accounts. You **must run them as Administrator (Windows)** or **root (Linux)** for them to work.

### 1. Block an IP Address

```bash
python block_ip.py 192.168.1.50
```

### 2. Lock a User Account

```bash
python lock_account.py TestUser
```

### 3. Send an Email Alert

To use the email script, you must first provide your SMTP credentials securely via environment variables:

```bash
# Set your credentials
export SMTP_USER="your_email@gmail.com"
export SMTP_PASS="your_app_password"

# Send the alert
python email_alert.py "security_team@example.com" --subject "[CRITICAL] Ransomware detected" --body "Machine DESKTOP-X has exhibited ransomware behavior. Proceed to isolate."
```
*(Note for Windows: Use `set SMTP_USER=...` in CMD or `$env:SMTP_USER="..."` in PowerShell).*

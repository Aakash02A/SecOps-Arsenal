# Blue Team Host Hardening Auditor

This tool acts as a local security baseline auditor for both **Windows** and **Linux** endpoints. System hardening is a critical Blue Team function; an unhardened server is much easier for an attacker to exploit, even if the application layer is secure.

## Features

The script automatically detects the host OS and runs a tailored set of baseline checks:

### Windows Checks
1. **Firewall Status**: Ensures the native Windows Firewall is enabled.
2. **Guest Account**: Verifies that the built-in Guest account is disabled (a common vector for privilege escalation).
3. **UAC (User Account Control)**: Checks the registry to ensure LUA (Limited User Access) is enabled.
4. **RDP (Remote Desktop)**: Checks if RDP is disabled (a secure baseline for endpoints that do not require remote administration).

### Linux Checks
1. **SSH Root Login**: Parses `/etc/ssh/sshd_config` to ensure `PermitRootLogin` is set to `no` or `prohibit-password`.
2. **UFW Status**: Checks if the Uncomplicated Firewall (UFW) is active.
3. **ASLR**: Reads `/proc/sys/kernel/randomize_va_space` to verify Address Space Layout Randomization is fully enabled (value of 2), protecting against memory corruption exploits.

## Usage

**Note:** For the most accurate results, run this script with elevated privileges (Administrator on Windows, `root`/`sudo` on Linux) so it can successfully query registry keys and protected configuration files.

```bash
python auditor.py
```

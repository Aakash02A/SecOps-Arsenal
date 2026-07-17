#!/usr/bin/env python3
"""Security Playbook: Block a malicious IP address at the host firewall level.

Supports Windows (netsh advfirewall) and Linux (iptables).
Requires Administrator/root privileges to modify firewall rules.

⚠️  CAUTION: This script modifies live firewall rules. Only use in
authorized environments or security labs.
"""

import argparse
import ipaddress
import subprocess
import platform
import sys


def validate_ip(ip_string):
    """Validate that the provided string is a legitimate IP address."""
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def block_ip_windows(ip, dry_run=False):
    """Block an IP address using Windows Firewall (netsh advfirewall)."""
    rule_name = f"AutoBlock_{ip}"
    cmd = [
        "netsh", "advfirewall", "firewall", "add", "rule",
        f"name={rule_name}", "dir=in", "action=block", f"remoteip={ip}",
    ]
    print(f"[*] Command: {' '.join(cmd)}")

    if dry_run:
        print("[*] DRY RUN — no changes made.")
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully blocked {ip} in Windows Firewall.")
    else:
        print(f"[-] Failed to block IP. Ensure you are running as Administrator.")
        print(f"    Error: {result.stderr.strip()}")


def block_ip_linux(ip, dry_run=False):
    """Block an IP address using iptables on Linux."""
    cmd = ["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"]
    print(f"[*] Command: {' '.join(cmd)}")

    if dry_run:
        print("[*] DRY RUN — no changes made.")
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully blocked {ip} using iptables.")
    else:
        print(f"[-] Failed to block IP. Ensure you are running as root.")
        print(f"    Error: {result.stderr.strip()}")


def main():
    parser = argparse.ArgumentParser(
        description="Security Playbook: IP Blocking",
    )
    parser.add_argument("ip", help="The IP address to block")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the command without executing it",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Skip the confirmation prompt",
    )

    args = parser.parse_args()

    if not validate_ip(args.ip):
        print(f"[-] Invalid IP address: {args.ip}")
        sys.exit(1)

    os_name = platform.system()
    print(f"[*] OS detected: {os_name}")

    if not args.yes and not args.dry_run:
        confirm = input(f"[?] Block IP {args.ip} in firewall? [y/N]: ").strip().lower()
        if confirm != "y":
            print("[*] Aborted.")
            sys.exit(0)

    if os_name == "Windows":
        block_ip_windows(args.ip, dry_run=args.dry_run)
    elif os_name == "Linux":
        block_ip_linux(args.ip, dry_run=args.dry_run)
    else:
        print(f"[-] Unsupported OS for automated blocking: {os_name}")
        sys.exit(1)


if __name__ == "__main__":
    main()

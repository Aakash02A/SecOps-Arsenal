#!/usr/bin/env python3
"""Security Playbook: Lock/disable a local user account.

Supports Windows (net user) and Linux (usermod -L).
Requires Administrator/root privileges.

⚠️  CAUTION: This script disables live user accounts. Only use in
authorized environments or security labs.
"""

import argparse
import re
import subprocess
import platform
import sys


def validate_username(username):
    """Validate that the username contains only safe characters."""
    # Allow alphanumeric, hyphens, underscores, and dots
    return bool(re.match(r"^[a-zA-Z0-9._-]+$", username))


def lock_account_windows(username, dry_run=False):
    """Disable a local Windows account using 'net user'."""
    cmd = ["net", "user", username, "/active:no"]
    print(f"[*] Command: {' '.join(cmd)}")

    if dry_run:
        print("[*] DRY RUN — no changes made.")
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully locked/disabled account: {username}")
    else:
        print("[-] Failed to lock account. Ensure you are running as Administrator.")
        print(f"    Error: {result.stderr.strip()}")


def lock_account_linux(username, dry_run=False):
    """Lock a Linux user account using 'usermod -L'."""
    cmd = ["usermod", "-L", username]
    print(f"[*] Command: {' '.join(cmd)}")

    if dry_run:
        print("[*] DRY RUN — no changes made.")
        return

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully locked account: {username}")
    else:
        print("[-] Failed to lock account. Ensure you are running as root.")
        print(f"    Error: {result.stderr.strip()}")


def main():
    parser = argparse.ArgumentParser(
        description="Security Playbook: Account Lock",
    )
    parser.add_argument("username", help="The local username to lock/disable")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the command without executing it",
    )
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Skip the confirmation prompt",
    )

    args = parser.parse_args()

    if not validate_username(args.username):
        print(f"[-] Invalid username: {args.username}")
        print("    Usernames may only contain letters, numbers, dots, hyphens, and underscores.")
        sys.exit(1)

    os_name = platform.system()
    print(f"[*] OS detected: {os_name}")

    if not args.yes and not args.dry_run:
        confirm = input(f"[?] Lock account '{args.username}'? [y/N]: ").strip().lower()
        if confirm != "y":
            print("[*] Aborted.")
            sys.exit(0)

    if os_name == "Windows":
        lock_account_windows(args.username, dry_run=args.dry_run)
    elif os_name == "Linux":
        lock_account_linux(args.username, dry_run=args.dry_run)
    else:
        print(f"[-] Unsupported OS for automated account locking: {os_name}")
        sys.exit(1)


if __name__ == "__main__":
    main()

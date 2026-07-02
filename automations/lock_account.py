import argparse
import subprocess
import platform

def lock_account_windows(username):
    # Disable the local account
    cmd = f'net user {username} /active:no'
    print(f"[*] Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully locked/disabled account: {username}")
    else:
        print(f"[-] Failed to lock account. Ensure you are running as Administrator.\nError: {result.stderr}")

def lock_account_linux(username):
    # Lock the user account using usermod
    cmd = f'usermod -L {username}'
    print(f"[*] Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully locked account: {username}")
    else:
        print(f"[-] Failed to lock account. Ensure you are running as root.\nError: {result.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Security Playbook: Account Lock")
    parser.add_argument("username", help="The local username to lock/disable")
    
    args = parser.parse_args()
    
    os_name = platform.system()
    print(f"[*] OS detected: {os_name}")
    
    if os_name == "Windows":
        lock_account_windows(args.username)
    elif os_name == "Linux":
        lock_account_linux(args.username)
    else:
        print(f"[-] Unsupported OS for automated account locking: {os_name}")

if __name__ == "__main__":
    main()

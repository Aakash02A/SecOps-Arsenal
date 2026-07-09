import platform
import os
import subprocess
import sys

def check_windows_baseline():
    """Perform security baseline checks for Windows environments."""
    print("[*] Running Windows Security Baseline Audit...\n")
    score = 0
    total_checks = 4
    
    # Check 1: Windows Firewall
    print("  [1] Checking Windows Firewall status...")
    try:
        res = subprocess.run('netsh advfirewall show currentprofile state', shell=True, capture_output=True, text=True)
        if "ON" in res.stdout:
            print("      [PASS] Windows Firewall is ENABLED.")
            score += 1
        else:
            print("      [FAIL] Windows Firewall is DISABLED.")
    except Exception as e:
        print(f"      [-] Error checking firewall: {e}")

    # Check 2: Guest Account Status
    print("  [2] Checking Guest Account status...")
    try:
        res = subprocess.run('net user Guest', shell=True, capture_output=True, text=True)
        if "Account active               No" in res.stdout:
            print("      [PASS] Guest account is DISABLED.")
            score += 1
        else:
            print("      [FAIL] Guest account is ENABLED.")
    except Exception as e:
        print(f"      [-] Error checking Guest account: {e}")

    # Check 3: UAC Status (Registry check via reg query)
    print("  [3] Checking User Account Control (UAC) status...")
    try:
        cmd = 'reg query HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if "0x1" in res.stdout:
            print("      [PASS] UAC is ENABLED.")
            score += 1
        else:
            print("      [FAIL] UAC is DISABLED.")
    except Exception as e:
        print(f"      [-] Error checking UAC: {e}")

    # Check 4: RDP Status
    print("  [4] Checking Remote Desktop (RDP) status...")
    try:
        cmd = 'reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections'
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # fDenyTSConnections = 1 means RDP is disabled (a more secure baseline for workstations)
        if "0x1" in res.stdout:
            print("      [PASS] RDP is DISABLED (Secure Baseline).")
            score += 1
        else:
            print("      [FAIL] RDP is ENABLED.")
    except Exception as e:
        print(f"      [-] Error checking RDP: {e}")

    print(f"\n[*] Audit Complete: Scored {score}/{total_checks}")
    if score == total_checks:
        print("[+] System meets basic hardening standards.")
    else:
        print("[-] System failed one or more hardening checks. Review failures above.")

def check_linux_baseline():
    """Perform security baseline checks for Linux environments."""
    print("[*] Running Linux Security Baseline Audit...\n")
    score = 0
    total_checks = 3
    
    # Check 1: Root SSH Login
    print("  [1] Checking SSH Root Login configuration...")
    try:
        if os.path.exists('/etc/ssh/sshd_config'):
            with open('/etc/ssh/sshd_config', 'r') as f:
                content = f.read()
                if "PermitRootLogin no" in content or "PermitRootLogin prohibit-password" in content:
                     print("      [PASS] Root SSH login is restricted.")
                     score += 1
                else:
                     print("      [FAIL] Root SSH login may be permitted.")
        else:
            print("      [-] sshd_config not found (SSH may not be installed).")
            # If not installed, it's technically secure from SSH attacks
            score += 1 
    except Exception as e:
        print(f"      [-] Error: {e}")

    # Check 2: UFW / Firewall Status
    print("  [2] Checking Firewall (UFW) status...")
    try:
        res = subprocess.run('ufw status', shell=True, capture_output=True, text=True)
        if "Status: active" in res.stdout:
            print("      [PASS] UFW Firewall is ACTIVE.")
            score += 1
        else:
            print("      [FAIL] UFW Firewall is INACTIVE or not installed.")
    except Exception as e:
        print(f"      [-] Error checking firewall: {e}")

    # Check 3: ASLR Status
    print("  [3] Checking ASLR (Address Space Layout Randomization) status...")
    try:
        with open('/proc/sys/kernel/randomize_va_space', 'r') as f:
            val = f.read().strip()
            if val == '2':
                print("      [PASS] ASLR is fully ENABLED.")
                score += 1
            else:
                print(f"      [FAIL] ASLR is NOT fully enabled (Value: {val}).")
    except Exception as e:
         print(f"      [-] Error checking ASLR: {e}")
         
    print(f"\n[*] Audit Complete: Scored {score}/{total_checks}")
    if score == total_checks:
        print("[+] System meets basic hardening standards.")
    else:
        print("[-] System failed one or more hardening checks. Review failures above.")

def main():
    print("="*50)
    print("   Host Hardening & Baseline Auditor")
    print("="*50)
    
    os_name = platform.system()
    print(f"[*] Detected Operating System: {os_name}\n")
    
    if os_name == "Windows":
        check_windows_baseline()
    elif os_name == "Linux":
        # Need root for some linux checks (like ufw)
        if os.geteuid() != 0:
            print("[-] WARNING: You are not running as root. Some checks may fail or return inaccurate results.")
        check_linux_baseline()
    else:
        print(f"[-] OS '{os_name}' is not currently supported by this auditor.")

if __name__ == "__main__":
    main()

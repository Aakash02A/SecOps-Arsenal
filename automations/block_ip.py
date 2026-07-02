import argparse
import subprocess
import platform

def block_ip_windows(ip):
    rule_name = f"AutoBlock_{ip}"
    cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
    print(f"[*] Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully blocked {ip} in Windows Firewall.")
    else:
        print(f"[-] Failed to block IP. Ensure you are running as Administrator.\nError: {result.stderr}")

def block_ip_linux(ip):
    cmd = f'iptables -A INPUT -s {ip} -j DROP'
    print(f"[*] Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"[+] Successfully blocked {ip} using iptables.")
    else:
        print(f"[-] Failed to block IP. Ensure you are running as root.\nError: {result.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Security Playbook: IP Blocking")
    parser.add_argument("ip", help="The IP address to block")
    
    args = parser.parse_args()
    
    os_name = platform.system()
    print(f"[*] OS detected: {os_name}")
    
    if os_name == "Windows":
        block_ip_windows(args.ip)
    elif os_name == "Linux":
        block_ip_linux(args.ip)
    else:
        print(f"[-] Unsupported OS for automated blocking: {os_name}")

if __name__ == "__main__":
    main()

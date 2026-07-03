import argparse
from smb.SMBConnection import SMBConnection
import sys

def enum_shares(ip, username, password, domain=""):
    print(f"[*] Attempting to enumerate SMB shares on {ip}...")
    
    # Generate a random client machine name
    client_machine_name = 'TEST_MACHINE'
    server_name = ip # Some servers require the actual netbios name, but IP often works for basic enum
    
    try:
        # Create connection object
        # is_direct_tcp=True uses port 445 (modern SMB) rather than port 139 (NetBIOS)
        conn = SMBConnection(username, password, client_machine_name, server_name, domain=domain, use_ntlm_v2=True, is_direct_tcp=True)
        
        print(f"[*] Connecting as '{domain}\\{username}'...")
        assert conn.connect(ip, 445)
        
        print("[+] Connection successful! Enumerating shares...\n")
        shares = conn.listShares()
        
        print(f"{'Share Name':<20} | {'Type':<15} | Comments")
        print("-" * 60)
        
        for share in shares:
            share_type = "Disk" if share.type == 0 else "IPC/Printer/Other"
            print(f"{share.name:<20} | {share_type:<15} | {share.comments}")
            
        conn.close()
        
    except Exception as e:
        print(f"[-] SMB connection failed: {e}")
        print("    (Check credentials, ensure port 445 is open, and verify SMBv2/v3 is enabled)")

def main():
    parser = argparse.ArgumentParser(description="Educational SMB Share Enumerator")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("-u", "--username", default="guest", help="Username (default: guest)")
    parser.add_argument("-p", "--password", default="", help="Password (default: empty)")
    parser.add_argument("-d", "--domain", default="", help="Domain name (optional)")
    
    args = parser.parse_args()
    
    enum_shares(args.ip, args.username, args.password, args.domain)

if __name__ == "__main__":
    main()

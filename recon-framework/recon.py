import requests
import argparse
import sys
import socket
from concurrent.futures import ThreadPoolExecutor

# Suppress insecure request warnings for testing
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_subdomain(domain, sub):
    """Check if a subdomain resolves to an IP address."""
    target = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(target)
        return f"{target} -> {ip}"
    except socket.gaierror:
        # Domain does not resolve
        return None

def check_directory(base_url, dir_name):
    """Check if a directory exists on the web server."""
    target = f"{base_url}/{dir_name}"
    try:
        # We use a timeout to prevent hanging on slow servers
        r = requests.get(target, verify=False, timeout=3, allow_redirects=False)
        # We ignore 404 Not Found. Other codes (200 OK, 403 Forbidden, 301 Redirect) indicate existence.
        if r.status_code != 404:
             return f"{target} (HTTP {r.status_code})"
    except requests.exceptions.RequestException:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Recon Framework: Subdomain & Directory Enumeration")
    parser.add_argument("target", help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads (default: 10)")
    parser.add_argument("--subdomains", action="store_true", help="Run subdomain enumeration")
    parser.add_argument("--directories", action="store_true", help="Run directory brute-force")
    
    args = parser.parse_args()
    
    if not args.subdomains and not args.directories:
        print("[-] You must specify what to run: --subdomains and/or --directories")
        sys.exit(1)
    
    try:
        with open(args.wordlist, 'r', encoding='utf-8') as f:
            # Strip whitespace and ignore empty lines
            words = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Error reading wordlist: {e}")
        sys.exit(1)
        
    print("==========================================")
    print("          Automated Recon Framework       ")
    print("==========================================")
    print(f"[*] Target: {args.target}")
    print(f"[*] Loaded {len(words)} words from {args.wordlist}")
    print(f"[*] Threads: {args.threads}")
    
    if args.subdomains:
        print("\n[*] Starting Subdomain Enumeration (DNS Resolution)...")
        found_subs = []
        # Use ThreadPoolExecutor for fast concurrent scanning
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            results = executor.map(lambda w: check_subdomain(args.target, w), words)
            for res in results:
                if res:
                    print(f"  [+] {res}")
                    found_subs.append(res)
        print(f"[*] Subdomain Enum Complete. Found {len(found_subs)} active subdomains.")

    if args.directories:
        print("\n[*] Starting Directory Brute-force (HTTP GET)...")
        # Ensure we have a valid URL protocol for web requests
        base_url = args.target
        if not base_url.startswith('http'):
            base_url = 'https://' + base_url 
            
        found_dirs = []
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            results = executor.map(lambda w: check_directory(base_url, w), words)
            for res in results:
                if res:
                    print(f"  [+] {res}")
                    found_dirs.append(res)
        print(f"[*] Directory Brute-force Complete. Found {len(found_dirs)} accessible paths.")

if __name__ == "__main__":
    main()

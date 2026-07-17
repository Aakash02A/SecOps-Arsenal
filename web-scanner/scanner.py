#!/usr/bin/env python3
"""Basic Web Vulnerability Scanner — header audit, TLS inspection, common exposure checks.

Performs checks commonly part of reconnaissance and vulnerability discovery:
security headers, TLS certificate validity, and exposed sensitive files.

⚠️  DISCLAIMER: Only run against web applications you own or have explicit
authorization to test.
"""

import argparse
import requests
import socket
import ssl
from datetime import datetime, timezone
import urllib.parse
import sys

# Suppress insecure request warnings for our basic scanning tool when hitting misconfigured servers
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_headers(url):
    print("\n[*] Auditing HTTP Security Headers...")
    security_headers = {
        'Strict-Transport-Security': 'Missing HSTS. Vulnerable to MITM SSL stripping.',
        'Content-Security-Policy': 'Missing CSP. Vulnerable to XSS.',
        'X-Frame-Options': 'Missing X-Frame-Options. Vulnerable to Clickjacking.',
        'X-Content-Type-Options': 'Missing X-Content-Type-Options. Vulnerable to MIME sniffing.'
    }
    
    try:
        response = requests.get(url, timeout=10, verify=False)
        headers = response.headers
        
        for header, warning in security_headers.items():
            if header in headers:
                print(f"  [+] {header} is present.")
            else:
                print(f"  [-] {warning}")
                
        # Check for information disclosure headers
        if 'Server' in headers:
            print(f"  [!] Info Disclosure: Server header is exposed -> {headers['Server']}")
        if 'X-Powered-By' in headers:
            print(f"  [!] Info Disclosure: X-Powered-By header is exposed -> {headers['X-Powered-By']}")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] Error retrieving headers: {e}")

def check_tls(hostname):
    print(f"\n[*] Inspecting TLS/SSL Certificate for {hostname}...")
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Extract Issuer and Subject common names safely
                issuer = dict(x[0] for x in cert.get('issuer', []))
                subject = dict(x[0] for x in cert.get('subject', []))
                
                print(f"  [+] Issued To: {subject.get('commonName', 'Unknown')}")
                print(f"  [+] Issued By: {issuer.get('organizationName', issuer.get('commonName', 'Unknown'))}")
                
                not_after = cert.get('notAfter')
                if not_after:
                    # SSL certificates use a specific date format: 'Oct 29 12:00:00 2024 GMT'
                    expire_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    days_left = (expire_date - datetime.now(timezone.utc)).days
                    
                    print(f"  [+] Expiration: {expire_date.strftime('%Y-%m-%d')} ({days_left} days remaining)")
                    if days_left < 30:
                        print(f"  [!] WARNING: Certificate expires soon ({days_left} days)!")
                else:
                    print("  [-] Could not parse expiration date.")
                    
    except socket.timeout:
         print("[-] Timeout connecting to port 443.")
    except ConnectionRefusedError:
         print("[-] Port 443 is closed.")
    except Exception as e:
        print(f"[-] Error retrieving TLS info: {e}")

def check_common_vulns(url):
    print("\n[*] Checking for Common Exposures...")
    
    # Ensure URL ends with a slash for appending paths
    if not url.endswith('/'):
        url += '/'
        
    endpoints = {
        'robots.txt': 'Check for exposed sensitive paths in robots.txt',
        '.git/config': 'CRITICAL: Git repository is publicly accessible!',
        '.env': 'CRITICAL: Environment file is publicly accessible!',
        'phpinfo.php': 'CRITICAL: PHPInfo page is exposed!'
    }
    
    for endpoint, description in endpoints.items():
        target = url + endpoint
        try:
            resp = requests.get(target, timeout=5, verify=False, allow_redirects=False)
            if resp.status_code == 200:
                print(f"  [!] FOUND: {target} - {description}")
            elif resp.status_code in [301, 302]:
                print(f"  [-] Redirected: {endpoint} (HTTP {resp.status_code})")
            else:
                print(f"  [-] Not found: {endpoint} (HTTP {resp.status_code})")
        except Exception as e:
            print(f"  [-] Error checking {endpoint}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Basic Web Vulnerability Scanner")
    parser.add_argument("url", help="Target URL (e.g., https://example.com)")
    
    args = parser.parse_args()
    url = args.url
    
    if not url.startswith('http'):
        url = 'https://' + url
        
    print(f"[*] Starting scan against: {url}")
    
    parsed = urllib.parse.urlparse(url)
    hostname = parsed.hostname
    
    if not hostname:
        print("[-] Invalid URL provided.")
        sys.exit(1)
        
    check_headers(url)
    
    if parsed.scheme == 'https':
        check_tls(hostname)
    else:
        print("\n[-] Skipping TLS check because scheme is HTTP.")
        
    check_common_vulns(url)
    print("\n[*] Scan complete.")

if __name__ == "__main__":
    main()

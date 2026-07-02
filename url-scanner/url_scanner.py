import argparse
import re
import os
import requests
import urllib.parse
import base64

def check_regex_patterns(url):
    """
    Check the URL against basic suspicious regex patterns.
    """
    findings = []
    
    # Check if URL uses HTTP instead of HTTPS
    if url.startswith("http://"):
        findings.append("URL uses unencrypted HTTP instead of HTTPS.")
        
    # Check for IP address instead of domain name
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(:[0-9]{1,5})?$")
    if ip_pattern.match(domain):
        findings.append("URL uses an IP address instead of a domain name.")
        
    # Check for excessive subdomains (e.g., a.b.c.d.example.com)
    # Exclude standard ones like www
    if domain.count('.') > 3:
        findings.append("URL has an unusually high number of subdomains.")
        
    # Check for abnormally long URL
    if len(url) > 75:
        findings.append("URL length is unusually long (>75 characters).")
        
    # Check for suspicious characters or obfuscation (e.g., @ symbol for basic auth)
    if "@" in domain:
        findings.append("URL contains '@' symbol in domain, often used to obscure the true destination.")
        
    return findings

def check_virustotal(url, api_key):
    """
    Query the VirusTotal v3 API for URL reputation.
    """
    if not api_key:
        return {"error": "VirusTotal API key not provided."}
        
    # VT v3 API requires the URL to be base64url encoded without padding
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    
    api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {
        "x-apikey": api_key
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
            return {"stats": stats}
        elif response.status_code == 404:
            return {"status": "URL not found in VirusTotal database (hasn't been scanned recently)."}
        elif response.status_code == 401:
            return {"error": "Invalid VirusTotal API Key."}
        else:
            return {"error": f"VirusTotal API returned HTTP {response.status_code}"}
            
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="URL Scanner: Regex + Reputation Checks")
    parser.add_argument("url", help="The URL to scan (e.g., https://example.com)")
    parser.add_argument("--api-key", help="VirusTotal API Key (can also be set via VT_API_KEY env var)")
    
    args = parser.parse_args()
    url = args.url
    
    # Ensure URL has scheme
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    print(f"\n[*] Scanning URL: {url}")
    
    # 1. Regex Checks
    print("\n[*] Running Static Pattern Checks...")
    regex_findings = check_regex_patterns(url)
    
    if not regex_findings:
        print("[+] No suspicious static patterns detected.")
    else:
        print("[-] Suspicious patterns found:")
        for finding in regex_findings:
            print(f"    - {finding}")
            
    # 2. VirusTotal Reputation Check
    print("\n[*] Running Reputation API Check (VirusTotal)...")
    vt_key = args.api_key or os.environ.get("VT_API_KEY")
    
    if vt_key:
        vt_results = check_virustotal(url, vt_key)
        
        if "error" in vt_results:
            print(f"[-] Error querying VirusTotal: {vt_results['error']}")
        elif "status" in vt_results:
            print(f"[*] {vt_results['status']}")
        else:
            stats = vt_results["stats"]
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0)
            
            print(f"[+] VirusTotal Results:")
            print(f"    - Malicious:  {malicious} vendors")
            print(f"    - Suspicious: {suspicious} vendors")
            print(f"    - Harmless:   {harmless} vendors")
            
            if malicious > 0 or suspicious > 0:
                print("\n[!] WARNING: This URL is flagged as malicious or suspicious by multiple security vendors!")
    else:
        print("[-] Skipping VirusTotal check (no API key provided).")
        print("    Set the VT_API_KEY environment variable or pass --api-key to enable.")

if __name__ == "__main__":
    main()

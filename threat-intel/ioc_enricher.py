import argparse
import requests
import os
import json
import sys

def check_abuseipdb(ip, api_key):
    """Query AbuseIPDB for IP reputation."""
    print(f"[*] Checking {ip} against AbuseIPDB...")
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return {
                "source": "AbuseIPDB", 
                "abuseConfidenceScore": f"{data.get('abuseConfidenceScore', 0)}%", 
                "totalReports": data.get('totalReports', 0), 
                "countryCode": data.get('countryCode')
            }
        else:
            return {"source": "AbuseIPDB", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"source": "AbuseIPDB", "error": str(e)}

def check_alienvault_otx(indicator, indicator_type, api_key):
    """Query AlienVault OTX for pulses containing the indicator."""
    print(f"[*] Checking {indicator} against AlienVault OTX...")
    
    # Map friendly names to OTX endpoint types
    otx_type_map = {
        "ip": "IPv4",
        "domain": "domain",
        "hash": "file"
    }
    
    mapped_type = otx_type_map.get(indicator_type)
    url = f"https://otx.alienvault.com/api/v1/indicators/{mapped_type}/{indicator}/general"
    headers = {
        'X-OTX-API-KEY': api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            pulses = data.get('pulse_info', {}).get('count', 0)
            tags = []
            
            # Extract tags from the pulses for quick context
            for pulse in data.get('pulse_info', {}).get('pulses', [])[:3]:
                tags.extend(pulse.get('tags', []))
                
            return {
                "source": "AlienVault OTX", 
                "pulseCount": pulses,
                "topTags": list(set(tags))[:5] # Return unique tags
            }
        else:
            return {"source": "AlienVault OTX", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"source": "AlienVault OTX", "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Threat Intel IOC Enricher")
    parser.add_argument("-i", "--ip", help="IP address to enrich")
    parser.add_argument("-d", "--domain", help="Domain to enrich")
    parser.add_argument("--hash", help="File hash (MD5, SHA1, SHA256) to enrich")
    
    args = parser.parse_args()
    
    # Retrieve API keys from environment variables for security
    abuseipdb_key = os.environ.get("ABUSEIPDB_API_KEY")
    otx_key = os.environ.get("OTX_API_KEY")
    
    if not any([args.ip, args.domain, args.hash]):
        print("[-] Please provide at least one IOC to enrich (-i, -d, or --hash).")
        sys.exit(1)
        
    results = {}
    
    if args.ip:
        print(f"\n[+] Enriching IP: {args.ip}")
        results[args.ip] = []
        if abuseipdb_key:
            results[args.ip].append(check_abuseipdb(args.ip, abuseipdb_key))
        else:
            print("  [-] ABUSEIPDB_API_KEY not set, skipping AbuseIPDB check...")
            
        if otx_key:
            results[args.ip].append(check_alienvault_otx(args.ip, 'ip', otx_key))
        else:
            print("  [-] OTX_API_KEY not set, skipping AlienVault OTX check...")
            
    if args.domain:
        print(f"\n[+] Enriching Domain: {args.domain}")
        results[args.domain] = []
        if otx_key:
            results[args.domain].append(check_alienvault_otx(args.domain, 'domain', otx_key))
        else:
            print("  [-] OTX_API_KEY not set, skipping AlienVault OTX check...")
            
    if args.hash:
        print(f"\n[+] Enriching Hash: {args.hash}")
        results[args.hash] = []
        if otx_key:
            results[args.hash].append(check_alienvault_otx(args.hash, 'hash', otx_key))
        else:
            print("  [-] OTX_API_KEY not set, skipping AlienVault OTX check...")
            
    print("\n" + "="*50)
    print("--- Enrichment Results ---")
    print(json.dumps(results, indent=4))
    print("="*50)

if __name__ == "__main__":
    main()

import argparse
import requests
import time
import sys

# Suppress insecure request warnings for testing
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_missing_auth(url, endpoint):
    """Check if an endpoint meant to be private is accessible without authentication."""
    print("\n[*] Test 1: Missing Authentication Check")
    target = f"{url}{endpoint}"
    print(f"    Targeting: {target} (without auth token)")
    
    try:
        response = requests.get(target, verify=False, timeout=5)
        if response.status_code in [200, 201]:
            print(f"  [!] VULNERABILITY FOUND: Endpoint is accessible without authentication (HTTP {response.status_code})")
        elif response.status_code in [401, 403]:
            print(f"  [+] Secure: Endpoint correctly rejected unauthenticated access (HTTP {response.status_code})")
        elif response.status_code == 404:
            print(f"  [-] Endpoint not found (HTTP 404).")
        else:
            print(f"  [-] Unexpected response: HTTP {response.status_code}")
    except Exception as e:
        print(f"  [-] Error: {e}")

def test_bola(url, endpoint, token, user_id, target_id):
    """Check for Broken Object Level Authorization (IDOR) by accessing another user's resource."""
    print("\n[*] Test 2: Broken Object Level Authorization (BOLA/IDOR) Check")
    headers = {"Authorization": f"Bearer {token}"}
    
    target = f"{url}{endpoint.replace('{id}', str(target_id))}"
    print(f"    Targeting: {target} (Using token for User ID: {user_id})")
    
    try:
        response = requests.get(target, headers=headers, verify=False, timeout=5)
        if response.status_code in [200, 201]:
            print(f"  [!] VULNERABILITY FOUND: Successfully accessed resource belonging to user {target_id}! (HTTP {response.status_code})")
        elif response.status_code in [401, 403]:
            print(f"  [+] Secure: Access denied to other user's resource (HTTP {response.status_code})")
        else:
            print(f"  [-] Unexpected response: HTTP {response.status_code}")
    except Exception as e:
        print(f"  [-] Error: {e}")

def test_rate_limiting(url, endpoint, requests_to_send=30):
    """Check if the API implements rate limiting to prevent brute force or DoS."""
    print("\n[*] Test 3: Rate Limiting Check")
    target = f"{url}{endpoint}"
    print(f"    Sending {requests_to_send} rapid requests to {target}")
    
    hit_limit = False
    try:
        for i in range(requests_to_send):
            response = requests.get(target, verify=False, timeout=5)
            if response.status_code == 429:
                print(f"  [+] Secure: Rate limit triggered at request #{i+1} (HTTP 429 Too Many Requests)")
                hit_limit = True
                break
            
        if not hit_limit:
            print(f"  [!] VULNERABILITY FOUND: No rate limiting detected after {requests_to_send} rapid requests.")
    except Exception as e:
        print(f"  [-] Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Automated API Security Tester")
    parser.add_argument("url", help="Base URL of the API (e.g., https://api.example.com)")
    parser.add_argument("-e", "--endpoint", default="/api/users/{id}", help="Endpoint to test (default: /api/users/{id})")
    parser.add_argument("-t", "--token", default="MOCK_TOKEN", help="Valid auth token for a specific user")
    parser.add_argument("-u", "--userid", default="100", help="ID belonging to the token owner")
    parser.add_argument("-x", "--targetid", default="101", help="ID belonging to a different user (for BOLA test)")
    
    args = parser.parse_args()
    
    url = args.url.rstrip('/')
    if not url.startswith('http'):
        url = 'https://' + url
        
    endpoint = args.endpoint if args.endpoint.startswith('/') else '/' + args.endpoint
    
    print(f"[*] Starting API Security Tests against: {url}")
    
    # 1. Test missing auth on the user's own endpoint
    own_endpoint = endpoint.replace('{id}', str(args.userid))
    test_missing_auth(url, own_endpoint)
    
    # 2. Test BOLA on another user's endpoint
    if '{id}' in endpoint:
        test_bola(url, endpoint, args.token, args.userid, args.targetid)
    else:
        print("\n[-] Skipping BOLA test because the placeholder '{id}' is not in the endpoint string.")
        
    # 3. Test rate limiting on the base endpoint
    test_rate_limiting(url, own_endpoint)
    
    print("\n[*] Scan complete.")

if __name__ == "__main__":
    main()

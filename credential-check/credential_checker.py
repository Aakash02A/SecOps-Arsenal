import argparse
import re
import hashlib
import requests
import sys

def check_password_complexity(password):
    """
    Check if the password meets complexity requirements.
    Requirements: Minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number, and 1 special character.
    """
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short (minimum 8 characters).")
        
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Missing uppercase letter.")
        
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Missing lowercase letter.")
        
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Missing number.")
        
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Missing special character.")
        
    return score, feedback

def check_pwned_passwords(password):
    """
    Check if the password has been exposed in a data breach using the Have I Been Pwned API.
    Uses k-Anonymity by only sending the first 5 characters of the SHA-1 hash.
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {
        "User-Agent": "Cybersecurity-BIAE-Tool"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[-] Error querying HIBP API: HTTP {response.status_code}")
            return None
            
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
        return 0
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Credential Checker: Complexity & Breach Lookup")
    parser.add_argument("password", help="Password to evaluate")
    parser.add_argument("--no-breach", action="store_true", help="Skip the breached password check")
    
    args = parser.parse_args()
    
    print(f"\n[*] Evaluating password complexity...")
    score, feedback = check_password_complexity(args.password)
    
    print(f"[+] Complexity Score: {score}/5")
    if score == 5:
        print("[+] Strong password complexity.")
    else:
        print("[-] Weak password. Feedback:")
        for fb in feedback:
            print(f"    - {fb}")
            
    if not args.no_breach:
        print(f"\n[*] Checking Have I Been Pwned database...")
        breach_count = check_pwned_passwords(args.password)
        
        if breach_count is not None:
            if breach_count > 0:
                print(f"[!] WARNING: This password has been seen {breach_count} times in data breaches!")
                print("[!] Do NOT use this password.")
            else:
                print("[+] Good news: This password was not found in known data breaches.")

if __name__ == "__main__":
    main()

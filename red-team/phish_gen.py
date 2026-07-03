import argparse
import os

TEMPLATE = """
Subject: Action Required: Update Your Account Security Settings
From: Security Team <security@company-update-portal.com>
To: {target_email}
Content-Type: text/html

<html>
<body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px;">
        <h2 style="color: #d9534f;">Security Alert</h2>
        <p>Dear User,</p>
        <p>We detected an unusual login attempt on your account from an unrecognized device.</p>
        <p>To secure your account, please verify your identity immediately by logging into the secure portal:</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{phishing_url}" style="background-color: #0275d8; color: white; padding: 12px 25px; text-decoration: none; border-radius: 4px; font-weight: bold;">Verify Account Now</a>
        </div>
        
        <p>If you do not verify your account within 24 hours, access may be temporarily suspended to prevent fraud.</p>
        <br>
        <p>Thank you,<br>IT Security Team</p>
    </div>
</body>
</html>
"""

def generate_template(email, url, output_file):
    print(f"[*] Generating phishing template for target: {email}")
    print(f"[*] Phishing URL (Payload): {url}")
    
    content = TEMPLATE.format(target_email=email, phishing_url=url)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"[+] Template successfully saved to {output_file}")
    print("[!] EDUCATIONAL USE ONLY: Do not use against unauthorized targets.")

def main():
    parser = argparse.ArgumentParser(description="Educational Phishing Template Generator")
    parser.add_argument("email", help="Target email address to simulate")
    parser.add_argument("url", help="The malicious URL/landing page to embed")
    parser.add_argument("-o", "--output", default="phishing_email.html", help="Output file name (default: phishing_email.html)")
    
    args = parser.parse_args()
    
    generate_template(args.email, args.url, args.output)

if __name__ == "__main__":
    main()

import smtplib
from email.message import EmailMessage
import argparse
import os
import sys

def send_alert(to_email, subject, body):
    # We use environment variables to keep credentials out of the source code
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    
    if not smtp_user or not smtp_pass:
        print("[-] Error: SMTP_USER and SMTP_PASS environment variables must be set.")
        print("    Example: export SMTP_USER='alert@example.com' && export SMTP_PASS='YourPassword'")
        sys.exit(1)

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    print(f"[*] Connecting to {smtp_server}:{smtp_port}...")
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print(f"[+] Alert email sent successfully to {to_email}")
    except Exception as e:
        print(f"[-] Failed to send email: {e}")

def main():
    parser = argparse.ArgumentParser(description="Security Playbook: Email Alert")
    parser.add_argument("to", help="Recipient email address")
    parser.add_argument("--subject", default="[SECURITY ALERT] Automated Playbook Triggered", help="Email subject")
    parser.add_argument("--body", required=True, help="Email body content")
    
    args = parser.parse_args()
    
    send_alert(args.to, args.subject, args.body)

if __name__ == "__main__":
    main()

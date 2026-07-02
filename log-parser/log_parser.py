import re
import csv
import json
import argparse
import sys
from collections import Counter

# Regex for standard Apache/Nginx Combined Log Format
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<bytes>\S+) '
    r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def parse_log_file(filepath):
    """
    Parses a web server access log file and returns a list of dictionaries.
    """
    parsed_logs = []
    error_count = 0
    
    print(f"[*] Parsing log file: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = LOG_PATTERN.match(line)
                if match:
                    data = match.groupdict()
                    # Clean up bytes if it's '-'
                    data['bytes'] = 0 if data['bytes'] == '-' else int(data['bytes'])
                    parsed_logs.append(data)
                else:
                    error_count += 1
                    
        print(f"[+] Successfully parsed {len(parsed_logs)} lines.")
        if error_count > 0:
            print(f"[-] Failed to parse {error_count} lines (format mismatch).")
            
        return parsed_logs
        
    except FileNotFoundError:
        print(f"[-] Error: File {filepath} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        sys.exit(1)

def analyze_logs(parsed_logs):
    """
    Perform basic analysis on the parsed logs.
    """
    ip_counter = Counter([log['ip'] for log in parsed_logs])
    status_counter = Counter([log['status'] for log in parsed_logs])
    
    print("\n--- Quick Analysis ---")
    
    print("\nTop 5 IP Addresses:")
    for ip, count in ip_counter.most_common(5):
        print(f"  {ip}: {count} requests")
        
    print("\nHTTP Status Codes:")
    for status, count in status_counter.most_common():
        print(f"  {status}: {count}")

def export_to_csv(parsed_logs, output_path):
    if not parsed_logs:
        return
        
    keys = parsed_logs[0].keys()
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(parsed_logs)
    print(f"\n[+] Exported structured data to {output_path}")

def export_to_json(parsed_logs, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(parsed_logs, f, indent=4)
    print(f"\n[+] Exported structured data to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Apache/Nginx Log Parser")
    parser.add_argument("log_file", help="Path to the access.log file")
    parser.add_argument("--csv", help="Output parsed data to CSV format")
    parser.add_argument("--json", help="Output parsed data to JSON format")
    parser.add_argument("--analyze", action="store_true", help="Perform and print quick analysis")
    
    args = parser.parse_args()
    
    parsed_logs = parse_log_file(args.log_file)
    
    if args.analyze:
        analyze_logs(parsed_logs)
        
    if args.csv:
        export_to_csv(parsed_logs, args.csv)
        
    if args.json:
        export_to_json(parsed_logs, args.json)
        
    if not args.csv and not args.json and not args.analyze:
        print("[!] No action specified. Use --analyze, --csv, or --json.")

if __name__ == "__main__":
    main()

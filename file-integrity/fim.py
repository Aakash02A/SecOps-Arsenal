import hashlib
import os
import json
import argparse
import time

def calculate_file_hash(filepath, algorithm='sha256'):
    """Calculate the hash of a file."""
    try:
        hash_func = getattr(hashlib, algorithm)()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except Exception as e:
        print(f"[-] Error reading {filepath}: {e}")
        return None

def build_baseline(directory, output_file, algorithm='sha256'):
    """Build a baseline of file hashes for a given directory."""
    baseline = {}
    print(f"[*] Building baseline for directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_file_hash(filepath, algorithm)
            if file_hash:
                baseline[filepath] = file_hash
                
    with open(output_file, 'w') as f:
        json.dump(baseline, f, indent=4)
    print(f"[+] Baseline saved to {output_file} with {len(baseline)} files.")

def monitor_integrity(directory, baseline_file, algorithm='sha256'):
    """Compare current file hashes against a saved baseline."""
    print(f"[*] Loading baseline from {baseline_file}...")
    try:
        with open(baseline_file, 'r') as f:
            baseline = json.load(f)
    except FileNotFoundError:
        print("[-] Baseline file not found. Please build a baseline first.")
        return

    print(f"[*] Checking integrity of {directory}...")
    current_files = set()
    
    # Check for modifications and new files
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            current_files.add(filepath)
            
            file_hash = calculate_file_hash(filepath, algorithm)
            if not file_hash:
                continue
                
            if filepath not in baseline:
                print(f"[!] NEW FILE DETECTED: {filepath}")
            elif baseline[filepath] != file_hash:
                print(f"[!] MODIFIED FILE DETECTED: {filepath}")
                
    # Check for deleted files
    for filepath in baseline:
        if filepath not in current_files:
            print(f"[!] DELETED FILE DETECTED: {filepath}")
            
    print("[*] Integrity check complete.")

def main():
    parser = argparse.ArgumentParser(description="File Integrity Monitor (FIM)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Baseline command
    parser_build = subparsers.add_parser("build", help="Build a new baseline")
    parser_build.add_argument("directory", help="Directory to monitor")
    parser_build.add_argument("-o", "--output", default="baseline.json", help="Output baseline file (default: baseline.json)")
    parser_build.add_argument("-a", "--algorithm", default="sha256", choices=['md5', 'sha1', 'sha256', 'sha512'], help="Hash algorithm")
    
    # Check command
    parser_check = subparsers.add_parser("check", help="Check integrity against baseline")
    parser_check.add_argument("directory", help="Directory to monitor")
    parser_check.add_argument("-b", "--baseline", default="baseline.json", help="Baseline file (default: baseline.json)")
    parser_check.add_argument("-a", "--algorithm", default="sha256", choices=['md5', 'sha1', 'sha256', 'sha512'], help="Hash algorithm")

    # Monitor command
    parser_monitor = subparsers.add_parser("monitor", help="Continuously monitor integrity against baseline")
    parser_monitor.add_argument("directory", help="Directory to monitor")
    parser_monitor.add_argument("-b", "--baseline", default="baseline.json", help="Baseline file (default: baseline.json)")
    parser_monitor.add_argument("-a", "--algorithm", default="sha256", choices=['md5', 'sha1', 'sha256', 'sha512'], help="Hash algorithm")
    parser_monitor.add_argument("-i", "--interval", type=int, default=10, help="Check interval in seconds")

    args = parser.parse_args()
    
    if args.command == "build":
        build_baseline(args.directory, args.output, args.algorithm)
    elif args.command == "check":
        monitor_integrity(args.directory, args.baseline, args.algorithm)
    elif args.command == "monitor":
        print(f"[*] Starting continuous monitoring every {args.interval} seconds. Press Ctrl+C to stop.")
        try:
            while True:
                monitor_integrity(args.directory, args.baseline, args.algorithm)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[*] Monitoring stopped.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

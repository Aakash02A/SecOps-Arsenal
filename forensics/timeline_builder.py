import os
import csv
import argparse
from datetime import datetime

def build_timeline(directory, output_csv):
    print(f"[*] Scanning directory recursively: {directory}")
    
    timeline_events = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                stat = os.stat(filepath)
                # Create MAC times (Modified, Accessed, Created)
                
                # Windows uses st_ctime for Creation Time. On some Unix systems, this is Change Time.
                # Modified
                timeline_events.append({
                    "Timestamp": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "Type": "Modified (M)",
                    "File": filepath,
                    "Size": stat.st_size
                })
                # Accessed
                timeline_events.append({
                    "Timestamp": datetime.fromtimestamp(stat.st_atime).isoformat(),
                    "Type": "Accessed (A)",
                    "File": filepath,
                    "Size": stat.st_size
                })
                # Created
                timeline_events.append({
                    "Timestamp": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "Type": "Created/Changed (C)",
                    "File": filepath,
                    "Size": stat.st_size
                })
            except Exception as e:
                print(f"[-] Could not access {filepath}: {e}")
                
    # Sort all collected events chronologically
    print("[*] Sorting timeline...")
    timeline_events.sort(key=lambda x: x["Timestamp"])
    
    print(f"[*] Exporting {len(timeline_events)} events to {output_csv}")
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Timestamp", "Type", "File", "Size"])
        writer.writeheader()
        writer.writerows(timeline_events)
        
    print("[+] Timeline generation complete. You can open this CSV in Excel or Timeline Explorer.")

def main():
    parser = argparse.ArgumentParser(description="Forensic Timeline Builder")
    parser.add_argument("directory", help="Directory to scan for artifacts")
    parser.add_argument("-o", "--output", default="timeline.csv", help="Output CSV file (default: timeline.csv)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print(f"[-] Directory not found: {args.directory}")
        return
        
    build_timeline(args.directory, args.output)

if __name__ == "__main__":
    main()

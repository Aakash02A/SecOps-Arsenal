import platform
import subprocess
import os
import datetime
import argparse
import sys

def run_cmd(cmd):
    """Executes a shell command and returns the output safely."""
    try:
        # We capture output to save it, setting a timeout to prevent hanging commands
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        
        # If standard output is empty but error exists, return the error
        if not res.stdout.strip() and res.stderr.strip():
            return f"[-] Command ran but returned error: {res.stderr}"
            
        return res.stdout
    except subprocess.TimeoutExpired:
        return f"[-] Command timed out: {cmd}"
    except Exception as e:
        return f"[-] Error running {cmd}: {e}"

def collect_windows(out_dir):
    """Native commands for Windows live response."""
    commands = {
        "network_connections.txt": "netstat -ano",
        "running_processes.txt": "tasklist /v",
        "system_info.txt": "systeminfo",
        "local_users.txt": "net user",
        "active_services.txt": "sc query state= all"
    }
    return collect_evidence(commands, out_dir)

def collect_linux(out_dir):
    """Native commands for Linux live response."""
    commands = {
        "network_connections.txt": "netstat -tulpn || ss -tulpn",
        "running_processes.txt": "ps auxf",
        "system_info.txt": "uname -a && cat /etc/os-release",
        "local_users.txt": "cat /etc/passwd",
        "active_services.txt": "systemctl list-units --type=service"
    }
    return collect_evidence(commands, out_dir)

def collect_evidence(commands, out_dir):
    files_created = []
    for filename, cmd in commands.items():
        print(f"[*] Collecting {filename} (Command: {cmd})...")
        output = run_cmd(cmd)
        
        filepath = os.path.join(out_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"--- Artifact output for command: {cmd} ---\n\n")
                f.write(output)
            files_created.append(filename)
        except Exception as e:
            print(f"[-] Could not write to {filepath}: {e}")
            
    return files_created

def generate_report(out_dir, files_created, os_name):
    """Generates a clean Markdown report summarizing the triage."""
    print("\n[*] Generating IR Report...")
    report_path = os.path.join(out_dir, "IR_Report.md")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Incident Response Triage Report\n\n")
            f.write(f"**Date/Time Collected:** {timestamp}\n")
            f.write(f"**Target OS:** {os_name}\n")
            f.write(f"**Host Name:** {platform.node()}\n")
            f.write(f"**Collection Directory:** `{os.path.abspath(out_dir)}`\n\n")
            
            f.write("## Evidence Collected\n")
            f.write("The following evidence files were successfully extracted from the live system using native binaries:\n\n")
            for file in files_created:
                f.write(f"- `{file}`\n")
                
            f.write("\n## Next Steps for the SOC Analyst\n")
            f.write("1. **Network Analysis**: Review `network_connections.txt` for suspicious outbound connections (e.g., C2 beacons). Look up unknown external IPs.\n")
            f.write("2. **Process Analysis**: Review `running_processes.txt` for unusual process names, or processes running out of temporary directories like `AppData` or `/tmp`.\n")
            f.write("3. **Persistence**: Review `local_users.txt` to ensure no unauthorized accounts were added for backdoor access.\n")
            
        print(f"[+] Report generated successfully at {report_path}")
    except Exception as e:
        print(f"[-] Failed to generate report: {e}")

def main():
    parser = argparse.ArgumentParser(description="Automated IR Evidence Collector")
    parser.add_argument("-o", "--output", default="ir_evidence", help="Output directory to store evidence (default: ir_evidence)")
    
    args = parser.parse_args()
    out_dir = args.output
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    os_name = platform.system()
    print("==========================================")
    print("      Automated IR Triage Collector")
    print("==========================================")
    print(f"[*] Detected OS: {os_name}")
    print(f"[*] Saving artifacts to: {out_dir}\n")
    
    if os_name == "Windows":
        files = collect_windows(out_dir)
    elif os_name == "Linux":
        files = collect_linux(out_dir)
    else:
        print(f"[-] OS '{os_name}' not supported by this collector.")
        sys.exit(1)
        
    generate_report(out_dir, files, os_name)
    print("\n[*] Triage complete. Zip the folder securely and transfer to analysis workstation.")

if __name__ == "__main__":
    main()

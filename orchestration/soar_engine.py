import yaml
import json
import subprocess
import argparse
import sys
import time
import os

def load_yaml(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[-] Error loading {filepath}: {e}")
        return None

def execute_action(action, alert_data):
    """Executes a defined playbook action, substituting alert variables into the command."""
    cmd_template = action.get('command', '')
    
    # Replace placeholders with actual data from the JSON alert
    # e.g., {src_ip} becomes the actual IP address
    cmd = cmd_template
    for key, value in alert_data.items():
        placeholder = f"{{{key}}}"
        if placeholder in cmd:
            cmd = cmd.replace(placeholder, str(value))
            
    print(f"      [>>] Executing Action: {cmd}")
    
    try:
        # In a real SOAR, you'd capture structured output, handle timeouts, and manage state
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        # We don't fail the whole script if an automation script fails, just log it
        if result.returncode == 0:
            print(f"      [OK] Action succeeded.")
        else:
            print(f"      [FAIL] Action failed: {result.stderr.strip()}")
    except Exception as e:
        print(f"      [FAIL] Exception during execution: {e}")

def process_alert(alert, playbooks):
    alert_type = alert.get('type')
    alert_severity = alert.get('severity', 'LOW')
    
    print(f"\n[*] Processing Alert: {alert_type} (Severity: {alert_severity})")
    
    matched_playbook = None
    for pb in playbooks.get('playbooks', []):
        # Match playbook by the specific trigger type
        if pb.get('trigger') == alert_type:
            matched_playbook = pb
            break
            
    if not matched_playbook:
        print(f"  [-] No playbook found for alert type: {alert_type}")
        return
        
    print(f"  [+] Matched Playbook: {matched_playbook.get('name')}")
    
    actions = matched_playbook.get('actions', [])
    for action in actions:
        execute_action(action, alert)

def main():
    parser = argparse.ArgumentParser(description="SOAR-lite Orchestration Engine")
    parser.add_argument("alert_file", help="Path to JSON file containing the incoming alert(s)")
    parser.add_argument("-p", "--playbooks", default="playbooks.yaml", help="Path to YAML playbooks file")
    
    args = parser.parse_args()
    
    print("==========================================")
    print("           SOAR-lite Engine v1.0          ")
    print("==========================================")
    
    if not os.path.exists(args.playbooks):
        print(f"[-] Playbooks file not found: {args.playbooks}")
        sys.exit(1)
        
    playbooks = load_yaml(args.playbooks)
    if not playbooks:
        sys.exit(1)
        
    try:
        with open(args.alert_file, 'r', encoding='utf-8') as f:
            alert_data = json.load(f)
    except Exception as e:
        print(f"[-] Error loading alert file: {e}")
        sys.exit(1)
        
    # Process a single alert or a list of alerts
    if isinstance(alert_data, list):
        for alert in alert_data:
            process_alert(alert, playbooks)
            time.sleep(1) # Small pause between alerts for readability
    else:
        process_alert(alert_data, playbooks)
        
    print("\n[*] Orchestration complete.")

if __name__ == "__main__":
    main()

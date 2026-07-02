import yaml
import json
import re
import argparse
from datetime import datetime
import sys

class AlertEngine:
    def __init__(self, rules_file):
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                self.rules = data.get('rules', [])
            print(f"[*] Loaded {len(self.rules)} rules from {rules_file}.")
        except Exception as e:
            print(f"[-] Error loading rules file: {e}")
            sys.exit(1)

    def evaluate(self, log_entry):
        alerts = []
        for rule in self.rules:
            condition = rule.get('conditions', {})
            field = condition.get('field')
            operator = condition.get('operator')
            target_value = condition.get('value')
            
            # If the log doesn't have the field we are checking, skip it
            if field not in log_entry:
                continue
                
            actual_value = log_entry[field]
            match = False
            
            try:
                if operator == 'regex':
                    if isinstance(actual_value, str) and re.search(str(target_value), actual_value):
                        match = True
                elif operator == 'contains':
                    if isinstance(actual_value, str) and str(target_value) in actual_value:
                        match = True
                elif operator == 'equals':
                    if str(actual_value) == str(target_value):
                        match = True
            except re.error as e:
                print(f"[-] Invalid regex in rule {rule['id']}: {e}")
                continue
                    
            if match:
                alerts.append({
                    "timestamp": datetime.now().isoformat(),
                    "rule_id": rule.get('id'),
                    "rule_name": rule.get('name'),
                    "severity": rule.get('severity'),
                    "source_ip": log_entry.get('ip', 'unknown'),
                    "trigger_value": actual_value
                })
        return alerts

def main():
    parser = argparse.ArgumentParser(description="Rule-Based Alert Generator (IDS/IPS logic)")
    parser.add_argument("logs", help="Path to JSON file containing parsed logs")
    parser.add_argument("-r", "--rules", default="rules.yaml", help="Path to YAML rules file (default: rules.yaml)")
    
    args = parser.parse_args()
    
    engine = AlertEngine(args.rules)
    
    print(f"[*] Loading logs from {args.logs}...")
    try:
        with open(args.logs, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except Exception as e:
        print(f"[-] Error loading logs: {e}")
        sys.exit(1)
        
    if not isinstance(logs, list):
        logs = [logs]
        
    print(f"[*] Scanning {len(logs)} log entries...\n")
    
    total_alerts = 0
    for entry in logs:
        alerts = engine.evaluate(entry)
        for alert in alerts:
            total_alerts += 1
            severity = alert['severity'].upper()
            
            # Color code based on severity (ANSI)
            if severity == "HIGH":
                color = "\033[91m" # Red
            elif severity == "MEDIUM":
                color = "\033[93m" # Yellow
            else:
                color = "\033[94m" # Blue
            reset = "\033[0m"
            
            print(f"{color}[!] ALERT [Sev: {severity}] | Rule: {alert['rule_name']} (ID: {alert['rule_id']}){reset}")
            print(f"    Source IP: {alert['source_ip']}")
            print(f"    Trigger Value: {alert['trigger_value']}")
            print("-" * 50)
            
    print(f"\n[*] Scan complete. Generated {total_alerts} alerts.")

if __name__ == "__main__":
    main()

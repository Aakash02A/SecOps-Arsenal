import argparse
import json
from collections import defaultdict


def load_logs(filepath):
    try:
        with open(filepath) as f:
            return json.load(f)
    except Exception as e:
        print(f"[-] Error loading {filepath}: {e}")
        return []


def correlate_events(auth_logs, net_logs):
    """Correlate authentication and network events to detect threats.

    This function is designed to be testable without side effects.
    Progress messages should be printed by the caller (main()) not here.
    """
    # 1. Aggregate failed logins by IP
    failed_logins = defaultdict(int)
    successful_logins = set()

    for event in auth_logs:
        ip = event.get("ip")
        action = event.get("action")

        if action == "failed_login":
            failed_logins[ip] += 1
        elif action == "success_login":
            successful_logins.add(ip)

    # 2. Find IPs that brute-forced (e.g., >= 3 fails) AND successfully logged in
    brute_force_success = set()
    for ip, count in failed_logins.items():
        if count >= 3 and ip in successful_logins:
            brute_force_success.add(ip)

    # 3. Aggregate network traffic by IP
    traffic_bytes = defaultdict(int)
    for event in net_logs:
        ip = event.get("src_ip")
        bytes_sent = event.get("bytes_sent", 0)
        traffic_bytes[ip] += bytes_sent

    # 4. Correlation: Brute Force Success + High Data Exfiltration (>10MB)
    alerts = []
    for ip in brute_force_success:
        data_sent_mb = traffic_bytes.get(ip, 0) / (1024 * 1024)
        if data_sent_mb > 10:
            alerts.append(
                {
                    "severity": "CRITICAL",
                    "ip": ip,
                    "reason": (
                        f"Brute force success ({failed_logins[ip]} fails) followed by "
                        f"massive data transfer ({data_sent_mb:.2f} MB)."
                    ),
                }
            )
        else:
            alerts.append(
                {
                    "severity": "HIGH",
                    "ip": ip,
                    "reason": (
                        f"Brute force success ({failed_logins[ip]} fails) but normal "
                        f"data transfer ({data_sent_mb:.2f} MB)."
                    ),
                }
            )

    return alerts


def main():
    parser = argparse.ArgumentParser(description="Security Log Correlation Engine")
    parser.add_argument("auth_log", help="Path to authentication JSON log")
    parser.add_argument("net_log", help="Path to network traffic JSON log")

    args = parser.parse_args()

    auth_data = load_logs(args.auth_log)
    net_data = load_logs(args.net_log)

    # Warn on empty sources but still run — correlate_events() handles empty
    # input gracefully, and partial data is still worth reporting on.
    if not auth_data:
        print(f"[-] Warning: no events loaded from {args.auth_log}.")
    if not net_data:
        print(f"[-] Warning: no events loaded from {args.net_log}.")

    print("[*] Starting Log Correlation Engine...\n")
    alerts = correlate_events(auth_data, net_data)

    print("=" * 65)
    print("                   CORRELATION ALERTS")
    print("=" * 65)

    if not alerts:
        print("[+] No correlated threats detected.")
    else:
        for alert in alerts:
            # Add basic ANSI coloring for terminal
            color = "\033[91m" if alert["severity"] == "CRITICAL" else "\033[93m"
            reset = "\033[0m"
            print(f"{color}[!] {alert['severity']} ALERT | Threat IP: {alert['ip']}{reset}")
            print(f"    Reason: {alert['reason']}")
            print("-" * 65)


if __name__ == "__main__":
    main()

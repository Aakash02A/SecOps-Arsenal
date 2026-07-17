#!/usr/bin/env python3
"""SOAR-lite Orchestration Engine — automated incident response.

Ingests security alerts (JSON), matches them against YAML playbooks,
and executes defined response actions. Designed for educational use
in security labs and authorized environments.

⚠️  CAUTION: This engine executes system commands defined in playbooks.
Only run with trusted playbook files in controlled environments.
"""

import yaml
import json
import re
import shlex
import subprocess
import argparse
import logging
import sys
import time
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def load_yaml(filepath):
    """Load and parse a YAML file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error("Error loading %s: %s", filepath, e)
        return None


def sanitize_value(value):
    """Sanitize a template variable value to prevent injection.

    Only allows alphanumeric characters, dots, hyphens, underscores,
    at-signs (for emails), and colons (for IPv6).
    """
    value_str = str(value)
    if not re.match(r"^[a-zA-Z0-9@._:/ -]+$", value_str):
        raise ValueError(f"Unsafe character in alert value: {value_str!r}")
    return value_str


def execute_action(action, alert_data, dry_run=False):
    """Execute a playbook action, substituting alert variables into the command."""
    cmd_template = action.get("command", "")

    # Replace placeholders with sanitized data from the JSON alert
    cmd = cmd_template
    for key, value in alert_data.items():
        placeholder = f"{{{key}}}"
        if placeholder in cmd:
            try:
                safe_value = sanitize_value(value)
            except ValueError as e:
                logger.warning("Skipping action — %s", e)
                return
            cmd = cmd.replace(placeholder, safe_value)

    logger.info("      [>>] Executing Action: %s", cmd)

    if dry_run:
        logger.info("      [DRY RUN] — no changes made.")
        return

    try:
        # Parse the command string into an argument list for safe execution
        cmd_parts = shlex.split(cmd)
        result = subprocess.run(
            cmd_parts, capture_output=True, text=True, timeout=10,
        )

        if result.returncode == 0:
            logger.info("      [OK] Action succeeded.")
        else:
            logger.warning("      [FAIL] Action failed: %s", result.stderr.strip())
    except Exception as e:
        logger.error("      [FAIL] Exception during execution: %s", e)


def process_alert(alert, playbooks, dry_run=False):
    """Match an alert to a playbook and execute its actions."""
    alert_type = alert.get("type")
    alert_severity = alert.get("severity", "LOW")

    logger.info("Processing Alert: %s (Severity: %s)", alert_type, alert_severity)

    matched_playbook = None
    for pb in playbooks.get("playbooks", []):
        if pb.get("trigger") == alert_type:
            matched_playbook = pb
            break

    if not matched_playbook:
        logger.info("  [-] No playbook found for alert type: %s", alert_type)
        return

    logger.info("  [+] Matched Playbook: %s", matched_playbook.get("name"))

    actions = matched_playbook.get("actions", [])
    for action in actions:
        execute_action(action, alert, dry_run=dry_run)


def main():
    parser = argparse.ArgumentParser(description="SOAR-lite Orchestration Engine")
    parser.add_argument(
        "alert_file",
        help="Path to JSON file containing the incoming alert(s)",
    )
    parser.add_argument(
        "-p", "--playbooks", default="playbooks.yaml",
        help="Path to YAML playbooks file",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print commands without executing them",
    )

    args = parser.parse_args()

    print("==========================================")
    print("           SOAR-lite Engine v1.1          ")
    print("==========================================")

    if not os.path.exists(args.playbooks):
        logger.error("Playbooks file not found: %s", args.playbooks)
        sys.exit(1)

    playbooks = load_yaml(args.playbooks)
    if not playbooks:
        sys.exit(1)

    try:
        with open(args.alert_file, "r", encoding="utf-8") as f:
            alert_data = json.load(f)
    except Exception as e:
        logger.error("Error loading alert file: %s", e)
        sys.exit(1)

    # Process a single alert or a list of alerts
    if isinstance(alert_data, list):
        for alert in alert_data:
            process_alert(alert, playbooks, dry_run=args.dry_run)
            time.sleep(1)
    else:
        process_alert(alert_data, playbooks, dry_run=args.dry_run)

    logger.info("Orchestration complete.")


if __name__ == "__main__":
    main()

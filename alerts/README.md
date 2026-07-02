# Rule-Based Alert Generator

This project is a lightweight Intrusion Detection System (IDS) logic engine. It behaves similarly to Zeek or Suricata but is highly simplified for educational purposes. 

It reads structured data (like the JSON output from our `log-parser` project) and evaluates each entry against a set of rules defined in a YAML file. If a log entry matches the conditions of a rule, an alert is generated.

## Features

- **YAML Rule Definitions:** Easy to write and understand detection rules without touching the code.
- **Multiple Operators:** Supports `regex`, `contains`, and `equals` checks against specific log fields.
- **Severity Levels:** Classifies alerts by severity and color-codes the terminal output.

## Included Files

1. **`rules.yaml`**: The configuration file containing the detection rules (e.g., detecting SQL Injection attempts, path traversal, or suspicious user agents).
2. **`alert_engine.py`**: The core Python script that loads the rules and scans a JSON log file.

## Prerequisites

Requires the `PyYAML` library to parse the rules file:

```bash
pip install pyyaml
```

## Usage

You need a JSON log file to scan. You can generate one using the tool we built in **Project 5 (`log-parser`)**. 

To run the engine using the default `rules.yaml` file:

```bash
python alert_engine.py ../log-parser/parsed_logs.json
```

If you want to specify a custom rules file:

```bash
python alert_engine.py ../log-parser/parsed_logs.json -r my_custom_rules.yaml
```

## Writing Custom Rules

Rules are written in YAML format. Here is the structure of a rule:

```yaml
- id: 1005                  # Unique Rule ID
  name: "Rule Name"         # Short name
  description: "Details"    # Description of what it detects
  severity: "Medium"        # High, Medium, or Low
  conditions:
    field: "path"           # Which field in the JSON log to check
    operator: "contains"    # 'regex', 'contains', or 'equals'
    value: "admin"          # The value to look for
```

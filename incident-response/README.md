# Incident Response Automated Collector

When a machine is suspected of being compromised, Incident Responders must collect volatile data (data that is lost when the machine is rebooted) immediately. This process is called "live response" or "triage."

This script automates the collection of vital system states and packages them alongside an easy-to-read markdown report.

## Features

- **Cross-Platform**: Automatically detects if the system is Windows or Linux and uses the appropriate native commands.
- **Volatile Evidence Extraction**: Captures active network connections (`netstat`), running processes (`tasklist` / `ps`), system info, local users, and active services.
- **Report Generation**: Automatically creates an `IR_Report.md` file summarizing the collection and giving the analyst immediate next steps.

## Usage

**Note:** Run this script as Administrator (Windows) or root (Linux) to ensure it has permission to view all processes and network connections.

Run the collector:

```bash
python ir_collector.py
```

By default, this will create a folder called `ir_evidence` in your current directory containing all the text files and the Markdown report.

If you want to specify a custom output directory (e.g., directly to a USB drive for air-gapped systems):

```bash
python ir_collector.py -o E:\Incident_Triage_Data
```

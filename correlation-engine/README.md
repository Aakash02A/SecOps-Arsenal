# Log Correlation Engine

A lightweight SIEM correlation engine that detects multi-stage attacks by connecting events from separate log sources.

---

## Overview

Security Operations Centers (SOCs) rarely see the full picture from a single log file. Advanced Persistent Threats (APTs) and sophisticated attackers spread their activities across multiple systems—they brute-force authentication systems, compromise accounts, and then exfiltrate data through network channels.

This Log Correlation Engine demonstrates the core concept behind advanced SIEM analytics: **Event Correlation**. By analyzing authentication logs alongside network traffic logs, it identifies patterns that would be invisible when examining each data source in isolation.

This tool is designed for SOC analysts, security researchers, and students learning SIEM correlation principles. It provides a foundation for understanding how enterprise platforms like Splunk, QRadar, and Elastic SIEM detect complex attack chains.

---

## How It Works

The engine implements a **three-phase correlation workflow**:

### Phase 1: Data Ingestion
- Reads structured JSON logs from two separate sources:
  - **Authentication logs**: Failed and successful login attempts with IP addresses and timestamps
  - **Network traffic logs**: Data transfer volumes indexed by source IP address

### Phase 2: Pattern Aggregation
- Builds behavioral profiles by IP address:
  - Counts failed login attempts per IP
  - Identifies successful logins per IP
  - Calculates total bytes transferred per IP

### Phase 3: Correlation & Alert Generation
- Detects the **brute-force → compromise → exfiltration** attack chain:
  1. **Brute Force Detection**: Identifies IPs with 3+ failed login attempts followed by a successful login
  2. **Exfiltration Detection**: Calculates data transfer volume for compromised IPs
  3. **Severity Classification**:
     - **CRITICAL**: Brute force success + >10MB data transfer (indicates data theft)
     - **HIGH**: Brute force success + <10MB data transfer (suspicious but limited impact)

### Detection Logic

```
IF (failed_login_count[ip] >= 3) AND (successful_login[ip] == True) THEN
    IF (bytes_transferred[ip] > 10MB) THEN
        ALERT: CRITICAL - Brute Force + Data Exfiltration
    ELSE
        ALERT: HIGH - Brute Force Success
```

---

## Features

- **Multi-Source Correlation**: Analyzes authentication and network logs simultaneously
- **Behavioral Aggregation**: Builds per-IP threat profiles from historical events
- **Attack Chain Detection**: Identifies multi-stage attack patterns (brute force → compromise → exfiltration)
- **Severity Scoring**: Classifies alerts as CRITICAL or HIGH based on data exfiltration volume
- **Color-Coded Output**: ANSI terminal colors for quick visual threat assessment
- **Mock Data Generator**: Included utility to create realistic test datasets
- **Threshold Tuning**: Easily adjustable thresholds for failed login counts (default: 3) and exfiltration volume (default: 10MB)

---

## Prerequisites

- **Python**: 3.11 or higher (uses standard library only)
- **Dependencies**: None (uses only Python standard library: `json`, `argparse`, `collections`)
- **Input Format**: JSON-formatted log files with specific schemas (see Usage section)

---

## Installation

This tool requires no external dependencies. Ensure you have Python 3.11+ installed:

```bash
# Verify Python version
python --version

# Navigate to the correlation-engine directory
cd correlation-engine/
```

No additional setup is required—the tool uses only Python standard library modules.

---

## Usage

### Step 1: Generate Mock Data

For testing and demonstration purposes, create realistic authentication and network log files:

```bash
python generate_mock_data.py
```

**Output:**
- `mock_auth.json` - Authentication events (failed and successful logins)
- `mock_net.json` - Network traffic events (data transfer volumes)

### Step 2: Run the Correlation Engine

Execute the correlator against the mock data:

```bash
python correlator.py mock_auth.json mock_net.json
```

### Using Your Own Logs

To analyze real data, format your logs as JSON arrays matching these schemas:

**Authentication Log Format (`auth_log.json`):**
```json
[
    {
        "timestamp": "2024-01-01T10:05:00Z",
        "ip": "10.0.0.99",
        "action": "failed_login"
    },
    {
        "timestamp": "2024-01-01T10:05:15Z",
        "ip": "10.0.0.99",
        "action": "success_login"
    }
]
```

**Network Traffic Log Format (`net_log.json`):**
```json
[
    {
        "timestamp": "2024-01-01T10:06:00Z",
        "src_ip": "10.0.0.99",
        "dst_ip": "1.1.1.1",
        "bytes_sent": 52428800
    }
]
```

Then run:
```bash
python correlator.py auth_log.json net_log.json
```

---

## Output & Interpretation

### Sample Output

```
[*] Starting Log Correlation Engine...

=================================================================
                   CORRELATION ALERTS
=================================================================
[!] CRITICAL ALERT | Threat IP: 10.0.0.99
    Reason: Brute force success (3 fails) followed by massive data transfer (50.00 MB).
-----------------------------------------------------------------
[!] HIGH ALERT | Threat IP: 203.0.113.5
    Reason: Brute force success (3 fails) but normal data transfer (1.00 MB).
-----------------------------------------------------------------
```

### Understanding Alerts

| Severity | Color | Meaning | Response Action |
|----------|-------|---------|-----------------|
| **CRITICAL** | Red | Brute force attack succeeded AND attacker exfiltrated >10MB of data | Immediate incident response: isolate IP, lock compromised account, investigate data loss |
| **HIGH** | Yellow | Brute force attack succeeded but limited data transfer detected | Investigate account activity, force password reset, monitor for escalation |
| **None** | Green | No correlated threats detected | Continue monitoring |

### Key Metrics

- **Failed Login Threshold**: 3 attempts (hard-coded in `correlate_events()` line 32)
- **Exfiltration Threshold**: 10 MB (hard-coded in `correlate_events()` line 48)
- **Data Units**: All byte counts are converted to MB for readability

---

## Security Considerations

### Intended Use
- **Authorized Testing Only**: This tool analyzes log data and does not perform active scanning or exploitation
- **Data Privacy**: Log files may contain sensitive information (IP addresses, usernames, timestamps). Handle them according to your organization's data retention policies
- **False Positives**: Legitimate users may trigger failed login thresholds due to forgotten passwords. Always investigate context before taking action

### Operational Security
- **Log Integrity**: Ensure log sources are tamper-proof. Attackers may attempt to delete or modify logs to evade correlation
- **Time Synchronization**: Correlation accuracy depends on synchronized timestamps across log sources. Use NTP in production environments
- **Threshold Tuning**: Default thresholds (3 failed logins, 10MB transfer) are conservative. Tune based on your environment's baseline behavior

---

## Limitations & Known Issues

### Current Limitations
1. **Static Thresholds**: Failed login counts and data transfer thresholds are hard-coded. Future versions may support configuration files
2. **No Time-Window Analysis**: The engine does not enforce time constraints between brute force attempts and data exfiltration (e.g., "within 1 hour"). It correlates all events across the entire log dataset
3. **Two Data Sources Only**: Currently limited to authentication and network logs. Real SIEM platforms correlate dozens of sources (firewall, endpoint, email, etc.)
4. **No Persistent State**: Each run starts fresh. The engine does not maintain historical baselines or track repeated offenders across multiple executions
5. **JSON Input Only**: Does not parse raw syslog, Windows Event Logs, or other native formats. Pre-processing required

### Known Issues
- **Large Datasets**: Performance degrades with logs containing >100,000 events. Consider log sampling or database indexing for production scale
- **Duplicate IPs**: If the same IP appears with different actions at the exact same timestamp, behavior is undefined (consider data deduplication)

### What This Tool Does NOT Do
- ❌ Parse raw log formats (syslog, CEF, Windows EVTX)
- ❌ Collect logs from live systems (see `../siem-ingest/` for data collection)
- ❌ Generate alerts via email/Slack (see `../automations/` for notification integrations)
- ❌ Provide real-time streaming correlation (batch processing only)
- ❌ Detect attacks beyond the brute-force-exfiltration pattern

---

## Related Tools & Further Reading

### SecOps-Arsenal Integration
- **`log-parser/`**: Parse raw web server logs into JSON format suitable for this correlator
- **`alerts/`**: Rule-based IDS engine for single-source event detection (compare to correlation approach)
- **`orchestration/`**: SOAR engine that can automatically respond to correlation alerts
- **`siem-ingest/`**: Collect and normalize logs from multiple sources into a centralized SIEM stack

### External Resources
- [MITRE ATT&CK - Brute Force (T1110)](https://attack.mitre.org/techniques/T1110/)
- [MITRE ATT&CK - Exfiltration Over C2 Channel (T1041)](https://attack.mitre.org/techniques/T1041/)
- [NIST SP 800-92: Guide to Computer Security Log Management](https://csrc.nist.gov/publications/detail/sp/800-92/final)
- [Splunk Correlation Searches Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Alert/Correlationsearches)

### Contributing
See the root [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding new correlation patterns
- Optimizing performance for large datasets
- Integrating additional log sources
- Submitting test cases

---

**Last Updated:** 2026-10-16  
**Tested With:** Python 3.11, 3.12, 3.13

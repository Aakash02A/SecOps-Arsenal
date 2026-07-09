# Log Correlation Engine

This project demonstrates the core concept behind advanced SIEM analytics: **Event Correlation**. Looking at a single log file rarely tells the whole story. By tying together events from different sources, we can detect complex, multi-stage attacks.

## How it Works

The script (`correlator.py`) reads two separate data sources:
1. **Authentication Logs**: Tracks successful and failed login attempts.
2. **Network Traffic Logs**: Tracks the amount of data transferred by IP addresses.

It correlates these events to find a specific attack pattern: **A successful brute-force attack followed by data exfiltration.**

If an IP fails to login 3+ times, successfully logs in, and then transfers more than 10MB of data, it flags the event as `CRITICAL`. If they brute-force successfully but don't transfer much data, it flags it as `HIGH`.

## Usage

First, generate the mock data files to test the engine:

```bash
python generate_mock_data.py
```

This will create `mock_auth.json` and `mock_net.json`. 

Next, run the correlation engine against those two log files:

```bash
python correlator.py mock_auth.json mock_net.json
```

You will see the engine piece together the brute-force attacks and network anomalies to generate the correct alerts.

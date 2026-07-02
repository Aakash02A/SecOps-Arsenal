# Log Parser & Dashboard

This project provides tools to parse, analyze, and visualize web server logs (Apache/Nginx). Analyzing logs is a fundamental skill for incident response and threat hunting to identify scanning, brute force attacks, or malicious payloads.

## Included Tools

1. **`log_parser.py`**: A command-line script that parses standard "Combined Log Format" access logs using regular expressions. It extracts IPs, timestamps, HTTP methods, paths, status codes, and user agents, exporting the structured data to CSV or JSON.
2. **`dashboard.py`**: A Streamlit web application that ingests the CSV output from the parser and provides an interactive visualization dashboard (useful for quick visual analysis of traffic patterns and anomalies).

## Prerequisites

For the parser, no external libraries are strictly required.
For the dashboard, you will need `pandas`, `streamlit`, and `plotly`:

```bash
pip install pandas streamlit plotly
```

## Usage

### 1. Parse an Access Log

Parse an Apache or Nginx access log file and output it to a CSV file (and print a quick analysis to the console):

```bash
python log_parser.py access.log --analyze --csv parsed_logs.csv
```
*(You can also use `--json parsed_logs.json` to output to JSON).*

### 2. Launch the Dashboard

Once you have generated your `parsed_logs.csv`, start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

This will open a local web server (usually at `http://localhost:8501`). You can then upload the `parsed_logs.csv` file directly into the web UI to view the visualizations.

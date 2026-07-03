# Threat Intel IOC Enricher

When investigating a security incident, a SOC analyst will often find "Indicators of Compromise" (IOCs) such as suspicious IP addresses, unfamiliar domain names, or file hashes. 

This tool automates the process of "Enrichment"—querying external Threat Intelligence platforms to see if the broader cybersecurity community already knows these indicators are malicious.

## Supported APIs

This script integrates with:
1. **[AbuseIPDB](https://www.abuseipdb.com/)**: Excellent for checking if an IP address is a known spammer, scanner, or attacker.
2. **[AlienVault OTX (Open Threat Exchange)](https://otx.alienvault.com/)**: A massive community-driven threat intel platform for checking IPs, Domains, and File Hashes.

## Prerequisites

Requires the `requests` library:

```bash
pip install requests
```

You must obtain free API keys from the services above and export them as environment variables:

```bash
# Linux / macOS
export ABUSEIPDB_API_KEY="your_abuseipdb_key"
export OTX_API_KEY="your_alienvault_otx_key"

# Windows (Command Prompt)
set ABUSEIPDB_API_KEY=your_abuseipdb_key
set OTX_API_KEY=your_alienvault_otx_key

# Windows (PowerShell)
$env:ABUSEIPDB_API_KEY="your_abuseipdb_key"
$env:OTX_API_KEY="your_alienvault_otx_key"
```

## Usage

You can enrich a single IP, Domain, or Hash, or query them all at once.

### Enrich an IP Address
```bash
python ioc_enricher.py -i 8.8.8.8
```

### Enrich a Domain Name
```bash
python ioc_enricher.py -d evil-malware-domain.com
```

### Enrich a File Hash
```bash
python ioc_enricher.py --hash 44d88612fea8a8f36de82e1278abb02f
```

The script will query the configured APIs and output a consolidated JSON report showing how many reports/pulses have been filed against the IOC and the associated threat tags.

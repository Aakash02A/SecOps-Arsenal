# Lightweight Packet Sniffer

A Python-based network packet capture tool for real-time traffic analysis and protocol inspection.

---

## Overview

Network packet sniffers are essential tools in every security professional's arsenal. They allow analysts to see raw network traffic flowing across interfaces—revealing communication patterns, protocol details, and potentially malicious payloads that higher-level tools miss.

This Lightweight Packet Sniffer uses Python and the `scapy` library to capture live network traffic, inspect packet headers, and display real-time information such as source/destination IP addresses, ports, protocols, and HTTP payloads. It's designed for network troubleshooting, security monitoring, and educational purposes.

**Use Cases:**
- **Incident Response**: Capture network activity during active security incidents
- **Malware Analysis**: Monitor malware network communications in sandboxed environments
- **Protocol Learning**: Understand how TCP/UDP protocols work at the packet level
- **Network Debugging**: Troubleshoot connectivity issues by inspecting raw traffic

---

## How It Works

The sniffer operates using **Scapy's packet capture engine**, which interfaces with the operating system's network stack:

### Architecture

```
┌─────────────────────┐
│  Network Interface  │  (eth0, wlan0, etc.)
└──────────┬──────────┘
           │
    ┌──────▼──────────┐
    │  Packet Filter  │  (BPF - Berkeley Packet Filter)
    │   "tcp port 80" │
    └──────┬──────────┘
           │
    ┌──────▼──────────┐
    │  Scapy Engine   │  (Captures matching packets)
    └──────┬──────────┘
           │
    ┌──────▼──────────┐
    │ packet_callback │  (Extracts IP/TCP/UDP/Raw layers)
    └──────┬──────────┘
           │
    ┌──────▼──────────┐
    │  Terminal Output│  (Formatted packet details)
    └─────────────────┘
```

### Processing Pipeline

1. **Interface Binding**: Attaches to a network interface (or all interfaces if unspecified)
2. **BPF Filtering**: Applies Berkeley Packet Filter syntax to capture only matching packets (e.g., `tcp port 80` for HTTP)
3. **Layer Extraction**: For each captured packet:
   - Checks for IP layer (IPv4)
   - Identifies transport protocol (TCP, UDP, or other)
   - Extracts source/destination IPs and ports
4. **Payload Inspection**: If the packet contains a Raw layer with HTTP keywords, displays the first 100 bytes
5. **Real-Time Display**: Prints timestamped packet summaries to the terminal as they arrive

### Why Scapy?

Scapy is a powerful Python library that provides low-level packet manipulation and capture capabilities without requiring platform-specific code. It abstracts away OS differences (Linux libpcap vs Windows WinPcap/Npcap) while maintaining full control over packet inspection.

---

## Features

- **Live Packet Capture**: Real-time traffic interception from network interfaces
- **Protocol Support**: Handles TCP, UDP, and other IP protocols
- **Port-Level Detail**: Displays source and destination ports for TCP/UDP traffic
- **HTTP Payload Detection**: Identifies and previews HTTP traffic payloads
- **BPF Filtering**: Supports Berkeley Packet Filter syntax for granular traffic selection
- **Interface Selection**: Sniff on specific interfaces (e.g., `eth0`) or all interfaces
- **Packet Count Limiting**: Capture a specific number of packets or run indefinitely
- **Timestamping**: Every packet includes a human-readable timestamp
- **Memory Efficient**: Uses `store=0` flag to avoid buffering packets in memory (suitable for long captures)

---

## Prerequisites

### Python Requirements
- **Python**: 3.11 or higher
- **Scapy Library**: Packet manipulation framework

### System Requirements

**Windows:**
- **Npcap** (required): Download from [https://npcap.com/](https://npcap.com/)
  - Install with "WinPcap API-compatible Mode" enabled
  - Required for raw socket access on Windows
- **Administrator Privileges**: Must run terminal as Administrator

**Linux:**
- **Root Privileges**: Required for raw socket access (`sudo`)
- **libpcap** (usually pre-installed on most distributions)

**macOS:**
- **Root Privileges**: Required (`sudo`)
- **libpcap** (pre-installed)

---

## Installation

### Step 1: Install Scapy

```bash
pip install scapy
```

### Step 2: Install Platform-Specific Dependencies

**On Windows:**
1. Download and install [Npcap](https://npcap.com/) (latest version)
2. During installation, check "Install Npcap in WinPcap API-compatible Mode"
3. Restart your terminal

**On Linux/macOS:**
```bash
# Verify libpcap is installed (usually pre-installed)
# On Debian/Ubuntu (if needed):
sudo apt-get install libpcap-dev

# On macOS (if needed):
brew install libpcap
```

### Step 3: Verify Installation

```bash
# Test Scapy import
python -c "from scapy.all import sniff; print('Scapy installed successfully')"
```

---

## Usage

### ⚠️ Privilege Requirements

**Linux/macOS:**
```bash
sudo python sniffer.py [options]
```

**Windows:**
- Right-click your terminal (Command Prompt or PowerShell)
- Select "Run as Administrator"
- Then run: `python sniffer.py [options]`

---

### Basic Sniffing

Capture all IP traffic on all available interfaces (infinite capture):

```bash
# Linux/macOS
sudo python sniffer.py

# Windows (in Administrator terminal)
python sniffer.py
```

---

### Sniffing a Specific Interface

Capture packets on a specific network interface:

```bash
# Linux - Ethernet interface
sudo python sniffer.py -i eth0

# Linux - Wireless interface
sudo python sniffer.py -i wlan0

# Windows - List interfaces first
python sniffer.py  # Will show error and list available interfaces
python sniffer.py -i "Ethernet"
```

**Tip:** On Windows, interface names often contain spaces (e.g., `"Wi-Fi"`, `"Ethernet"`). Use quotes around the interface name.

---

### Using BPF Filters

Berkeley Packet Filter (BPF) syntax allows you to capture only specific traffic:

**Capture HTTP traffic (port 80):**
```bash
sudo python sniffer.py -f "tcp port 80"
```

**Capture DNS queries (port 53):**
```bash
sudo python sniffer.py -f "udp port 53"
```

**Capture traffic to/from a specific IP:**
```bash
sudo python sniffer.py -f "host 192.168.1.100"
```

**Capture ICMP (ping) packets:**
```bash
sudo python sniffer.py -f "icmp"
```

**Complex filter (HTTP or HTTPS):**
```bash
sudo python sniffer.py -f "tcp port 80 or tcp port 443"
```

---

### Limiting Packet Count

Capture a specific number of packets and then stop:

```bash
# Capture exactly 10 packets
sudo python sniffer.py -c 10

# Capture 50 DNS packets
sudo python sniffer.py -f "udp port 53" -c 50
```

---

### Combined Options

Capture 20 HTTP packets on a specific interface:

```bash
sudo python sniffer.py -i eth0 -f "tcp port 80" -c 20
```

---

## Output & Interpretation

### Sample Output

```
[*] Starting Packet Sniffer...
[*] Interface: eth0
[*] Filter: tcp port 80
[*] Count: 10
[*] Press Ctrl+C to stop.

[2026-10-16 14:23:45] TCP | 192.168.1.100:54321 -> 93.184.216.34:80
    [+] HTTP Payload Detected: b'GET /index.html HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0...'
[2026-10-16 14:23:45] TCP | 93.184.216.34:80 -> 192.168.1.100:54321
[2026-10-16 14:23:46] TCP | 192.168.1.100:54322 -> 93.184.216.34:80
[2026-10-16 14:23:47] UDP | 192.168.1.100:53124 -> 8.8.8.8:53
```

### Understanding Output

Each line represents a captured packet:

```
[Timestamp] Protocol | Source_IP:Source_Port -> Destination_IP:Destination_Port
```

**Components:**
- **Timestamp**: When the packet was captured (local system time)
- **Protocol**: TCP, UDP, or other IP protocol number
- **Source IP:Port**: The sender's IP address and source port
- **Destination IP:Port**: The recipient's IP address and destination port
- **HTTP Payload**: If detected, shows the first 100 bytes of HTTP data

### Common Port Numbers

| Port | Protocol | Description |
|------|----------|-------------|
| 80 | HTTP | Unencrypted web traffic |
| 443 | HTTPS | Encrypted web traffic (payload encrypted) |
| 53 | DNS | Domain name lookups |
| 22 | SSH | Encrypted remote shell |
| 21 | FTP | File transfer protocol |
| 25 | SMTP | Email transmission |
| 3389 | RDP | Windows Remote Desktop |

---

## Security Considerations

### Legal & Ethical Warnings

⚠️ **CRITICAL**: Packet sniffing can intercept sensitive data (passwords, session tokens, personal information).

- **Authorization Required**: Only capture traffic on networks you own or have explicit written permission to monitor
- **Privacy Laws**: Unauthorized packet sniffing may violate wiretapping laws (e.g., CFAA in the US, GDPR in EU)
- **Workplace Policies**: Sniffing corporate networks without IT approval may result in termination or legal action
- **Credential Exposure**: HTTP payloads may contain plaintext passwords. Handle captured data responsibly

### Operational Security

- **Encrypted Traffic**: HTTPS/TLS traffic will show encrypted payloads (not human-readable). This tool does NOT decrypt SSL/TLS
- **Promiscuous Mode**: The sniffer operates in promiscuous mode, capturing all traffic on the interface (not just traffic destined for your machine)
- **Network Visibility**: On switched networks, you typically only see traffic to/from your own machine unless:
  - You're on a network hub (rare)
  - You're using ARP spoofing/MitM techniques (not provided by this tool)
  - You're monitoring a mirrored port (SPAN port) configured by a network administrator
- **Resource Usage**: Infinite captures (`-c 0`) can consume significant CPU on high-traffic networks. Use filters to reduce load

### Privilege Escalation Risks

- **Root/Admin Access**: This tool requires elevated privileges. Never run untrusted code with `sudo` or as Administrator
- **Secure Environment**: Only run on trusted systems. A compromised sniffer could be used to exfiltrate captured credentials

---

## Limitations & Known Issues

### Current Limitations

1. **IPv4 Only**: Does not capture IPv6 traffic (filter checks `packet.haslayer(IP)` for IPv4)
2. **No Packet Storage**: Uses `store=0` flag—captured packets are not saved to disk or memory (display-only)
3. **No PCAP Export**: Cannot export captures to Wireshark-compatible `.pcap` files (use `tcpdump` or `tshark` for that)
4. **HTTP Detection Only**: Payload inspection only triggers on HTTP. Does not decode other protocols (DNS, SMB, FTP)
5. **First 100 Bytes Only**: HTTP payloads are truncated to 100 bytes for display purposes
6. **No Packet Reassembly**: Does not reassemble fragmented packets or TCP streams (shows individual packets)
7. **No Decryption**: Cannot decrypt HTTPS/TLS traffic (would require MitM certificates, which is unethical without consent)

### Known Issues

- **Windows Interface Names**: Windows interface names can be ambiguous. Run without `-i` flag first to see available interface names in error message
- **Permission Errors**: If `PermissionError` occurs, verify:
  - Linux/macOS: Running with `sudo`
  - Windows: Terminal is running as Administrator AND Npcap is installed
- **High CPU Usage**: On gigabit networks without filters, CPU usage can spike. Use BPF filters (`-f`) to reduce load
- **Terminal Flooding**: Infinite captures on busy networks will flood the terminal. Use `-c` to limit output or redirect to a file:
  ```bash
  sudo python sniffer.py -c 100 > capture.log
  ```

### What This Tool Does NOT Do

- ❌ Decrypt SSL/TLS traffic
- ❌ Perform ARP spoofing or MitM attacks
- ❌ Save packets to `.pcap` files
- ❌ Reassemble TCP streams
- ❌ Provide packet statistics or graphs
- ❌ Capture IPv6 traffic
- ❌ Inject or modify packets

For advanced features, use **Wireshark**, **tcpdump**, or **tshark**.

---

## Related Tools & Further Reading

### SecOps-Arsenal Integration

- **`recon-framework/`**: Use packet sniffing to discover active hosts and services during reconnaissance
- **`incident-response/`**: Capture network evidence during incident response investigations
- **`log-parser/`**: Parse captured HTTP payloads for further analysis
- **`blue-team/`**: Integrate packet captures into blue team defensive workflows

### External Tools

- **Wireshark**: GUI-based packet analyzer with deep protocol inspection ([https://www.wireshark.org/](https://www.wireshark.org/))
- **tcpdump**: Command-line packet sniffer with PCAP export ([https://www.tcpdump.org/](https://www.tcpdump.org/))
- **tshark**: Wireshark's CLI version for automated packet analysis

### Learning Resources

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Berkeley Packet Filter (BPF) Syntax Guide](https://biot.com/capstats/bpf.html)
- [TCP/IP Illustrated by W. Richard Stevens](https://en.wikipedia.org/wiki/TCP/IP_Illustrated)
- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/)

### Contributing

See the root [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding IPv6 support
- Implementing PCAP export functionality
- Adding protocol-specific decoders (DNS, FTP, SMB)
- Performance optimization for high-throughput networks

---

**Last Updated:** 2026-10-16  
**Tested With:** Python 3.11, 3.12, 3.13 | Scapy 2.5.0+ | Npcap 1.70+ (Windows)

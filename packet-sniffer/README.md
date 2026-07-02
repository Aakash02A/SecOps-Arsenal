# Lightweight Packet Sniffer

This tool uses Python and the `scapy` library to capture live network traffic, inspect packet headers, and display real-time information such as source and destination IP addresses, ports, and protocols.

## Features

- Captures TCP and UDP packets.
- Prints the source and destination IP addresses and ports.
- Detects raw HTTP payloads in TCP traffic.
- Supports Berkeley Packet Filter (BPF) syntax to isolate specific traffic (e.g., only HTTP or only DNS).

## Prerequisites

Requires the `scapy` library:

```bash
pip install scapy
```

*Note on Windows:* You may also need to install [Npcap](https://npcap.com/) for Scapy to capture packets effectively.
*Note on Linux/macOS:* You typically need root privileges to sniff network interfaces.

## Usage

**Important:** You must run this script with administrator/root privileges!

### Basic Sniffing

Capture all IP packets on the default interfaces infinitely:

```bash
sudo python sniffer.py
```

*(On Windows, run your terminal as Administrator and simply type `python sniffer.py`)*

### Sniffing a Specific Interface

Capture packets on a specific interface like `eth0`:

```bash
sudo python sniffer.py -i eth0
```

### Using Filters

Capture only HTTP traffic (port 80):

```bash
sudo python sniffer.py -f "tcp port 80"
```

Capture only DNS traffic (port 53):

```bash
sudo python sniffer.py -f "udp port 53"
```

### Limiting Packet Count

Capture exactly 10 packets and then stop:

```bash
sudo python sniffer.py -c 10
```

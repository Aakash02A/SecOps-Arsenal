import argparse
from scapy.all import sniff, IP, TCP, UDP, Raw
from datetime import datetime
import sys

def packet_callback(packet):
    """
    Callback function that is executed for every captured packet.
    """
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        proto = ip_layer.proto
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if packet.haslayer(TCP):
            tcp_layer = packet.getlayer(TCP)
            src_port = tcp_layer.sport
            dst_port = tcp_layer.dport
            
            print(f"[{timestamp}] TCP | {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            
            # Optionally print payload if it contains HTTP data
            if packet.haslayer(Raw):
                payload = packet.getlayer(Raw).load
                if b"HTTP" in payload:
                    print(f"    [+] HTTP Payload Detected: {payload[:100]}...")
                    
        elif packet.haslayer(UDP):
            udp_layer = packet.getlayer(UDP)
            src_port = udp_layer.sport
            dst_port = udp_layer.dport
            print(f"[{timestamp}] UDP | {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            
        else:
            print(f"[{timestamp}] Protocol:{proto} | {src_ip} -> {dst_ip}")

def main():
    parser = argparse.ArgumentParser(description="Lightweight Network Packet Sniffer")
    parser.add_argument("-i", "--interface", help="Interface to sniff on (e.g., eth0, wlan0). Defaults to all interfaces.")
    parser.add_argument("-c", "--count", type=int, default=0, help="Number of packets to capture (0 = infinite)")
    parser.add_argument("-f", "--filter", default="ip", help="BPF filter (e.g., 'tcp port 80', 'icmp')")
    
    args = parser.parse_args()
    
    print(f"[*] Starting Packet Sniffer...")
    print(f"[*] Interface: {args.interface if args.interface else 'All'}")
    print(f"[*] Filter: {args.filter}")
    print(f"[*] Count: {args.count if args.count > 0 else 'Infinite'}")
    print("[*] Press Ctrl+C to stop.\n")
    
    try:
        sniff(iface=args.interface, filter=args.filter, prn=packet_callback, store=0, count=args.count)
    except PermissionError:
        print("[-] Permission Error: Sniffing requires root/administrator privileges.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

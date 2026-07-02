import nmap
import argparse
import sys
import json

def run_nmap_scan(target, arguments):
    """
    Run a basic Nmap scan against the specified target.
    """
    nm = nmap.PortScanner()
    
    print(f"[*] Starting Nmap scan on target: {target}")
    print(f"[*] Arguments: {arguments}")
    
    try:
        nm.scan(hosts=target, arguments=arguments)
    except nmap.PortScannerError as e:
        print(f"[-] Nmap error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[-] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
        
    results = {}
    for host in nm.all_hosts():
        results[host] = {
            "state": nm[host].state(),
            "protocols": {}
        }
        for proto in nm[host].all_protocols():
            results[host]["protocols"][proto] = {}
            ports = nm[host][proto].keys()
            for port in sorted(ports):
                results[host]["protocols"][proto][port] = nm[host][proto][port]

    return results

def main():
    parser = argparse.ArgumentParser(description="Basic Nmap Wrapper")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g., 22,80,443 or 1-1024)")
    parser.add_argument("-sV", "--service-version", action="store_true", help="Probe open ports to determine service/version info")
    parser.add_argument("-O", "--os-detection", action="store_true", help="Enable OS detection (requires root/admin)")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    nmap_args = []
    if args.ports:
        nmap_args.append(f"-p {args.ports}")
    if args.service_version:
        nmap_args.append("-sV")
    if args.os_detection:
        nmap_args.append("-O")
        
    arg_string = " ".join(nmap_args)
    
    results = run_nmap_scan(args.target, arg_string)
    
    if args.json:
        print(json.dumps(results, indent=4))
    else:
        for host, data in results.items():
            print(f"\n[+] Host: {host} (State: {data['state']})")
            for proto, ports in data.get('protocols', {}).items():
                print(f"  Protocol: {proto}")
                for port, port_data in ports.items():
                    state = port_data.get('state', 'unknown')
                    name = port_data.get('name', 'unknown')
                    version = port_data.get('version', '')
                    print(f"    Port: {port}\tState: {state}\tService: {name} {version}")

if __name__ == "__main__":
    main()

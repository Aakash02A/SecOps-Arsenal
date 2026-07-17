#!/usr/bin/env python3
"""IP information lookup — fetch geolocation, ASN, and reverse DNS data.

Provides both an importable API (`run_ip_info`) and a standalone CLI.
"""

import argparse
import json
import socket
import requests


def get_ipinfo_api(ip: str) -> dict:
    """Query ipapi.co for IP intelligence."""
    try:
        url = f"https://ipapi.co/{ip}/json/"
        response = requests.get(url, timeout=5).json()

        if "error" in response:
            return None

        return {
            "ip": ip,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country"),
            "postal": response.get("postal"),
            "latitude": response.get("latitude"),
            "longitude": response.get("longitude"),
            "asn": response.get("asn"),
            "org": response.get("org"),
        }
    except requests.RequestException:
        return None


def get_hostname(ip: str) -> str:
    """Reverse DNS lookup for hostname."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return None


def run_ip_info(ip: str) -> dict:
    """Main function to get IP info with fallback logic."""
    result = {
        "ip": ip,
        "hostname": get_hostname(ip),
        "city": None,
        "region": None,
        "country": None,
        "latitude": None,
        "longitude": None,
        "asn": None,
        "org": None,
        "raw": {},
    }

    # Query API
    data = get_ipinfo_api(ip)

    if data:
        result.update(data)
        result["raw"] = data

    return result


def main():
    parser = argparse.ArgumentParser(description="IP Address Information Lookup")
    parser.add_argument("ip", help="IP address to look up (e.g., 8.8.8.8)")
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results in JSON format",
    )

    args = parser.parse_args()
    result = run_ip_info(args.ip)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"[+] IP:       {result['ip']}")
        print(f"    Hostname: {result['hostname'] or 'N/A'}")
        print(f"    City:     {result['city'] or 'N/A'}")
        print(f"    Region:   {result['region'] or 'N/A'}")
        print(f"    Country:  {result['country'] or 'N/A'}")
        print(f"    ASN:      {result['asn'] or 'N/A'}")
        print(f"    Org:      {result['org'] or 'N/A'}")


if __name__ == "__main__":
    main()

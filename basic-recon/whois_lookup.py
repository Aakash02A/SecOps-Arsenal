#!/usr/bin/env python3
"""WHOIS lookup utility — query domain registration details.

Provides both an importable API (`run_whois`) and a standalone CLI.
"""

import argparse
import json
import whois


def run_whois(domain: str) -> dict:
    """Perform a WHOIS lookup and return parsed data."""
    result = {
        "domain": domain,
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "name_servers": [],
        "emails": [],
        "raw": "",
    }

    try:
        data = whois.whois(domain)

        result["registrar"] = data.registrar
        result["creation_date"] = str(data.creation_date)
        result["expiration_date"] = str(data.expiration_date)
        result["name_servers"] = data.name_servers or []
        result["emails"] = data.emails or []
        result["raw"] = data.text  # full WHOIS output

        return result

    except Exception as e:
        return {
            "error": str(e),
            "domain": domain,
        }


def main():
    parser = argparse.ArgumentParser(description="WHOIS Domain Lookup")
    parser.add_argument("domain", help="Domain to look up (e.g., example.com)")
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results in JSON format",
    )

    args = parser.parse_args()
    result = run_whois(args.domain)

    if args.json_output:
        print(json.dumps(result, indent=2, default=str))
    else:
        if "error" in result:
            print(f"[-] Error: {result['error']}")
        else:
            print(f"[+] Domain:      {result['domain']}")
            print(f"    Registrar:   {result['registrar']}")
            print(f"    Created:     {result['creation_date']}")
            print(f"    Expires:     {result['expiration_date']}")
            print(f"    Name Servers: {', '.join(result['name_servers'])}")
            print(f"    Emails:      {', '.join(result['emails']) if result['emails'] else 'N/A'}")


if __name__ == "__main__":
    main()

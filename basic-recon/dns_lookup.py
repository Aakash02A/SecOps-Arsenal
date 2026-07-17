#!/usr/bin/env python3
"""DNS lookup utility — query multiple DNS record types for a domain.

Provides both an importable API (`run_dns_lookup`) and a standalone CLI.
"""

import argparse
import json
import dns.resolver


def query_record(domain: str, record_type: str):
    """Helper: query a single DNS record type."""
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except Exception as e:
        return [f"Error: {str(e)}"]


def run_dns_lookup(domain: str) -> dict:
    """Perform a full DNS lookup on a domain."""
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
    result = {
        "domain": domain,
        "records": {},
    }

    for rtype in record_types:
        result["records"][rtype] = query_record(domain, rtype)

    return result


def main():
    parser = argparse.ArgumentParser(description="DNS Record Lookup")
    parser.add_argument("domain", help="Domain to look up (e.g., example.com)")
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results in JSON format",
    )
    parser.add_argument(
        "-t", "--type", dest="record_types", nargs="+",
        default=None,
        help="Specific record types to query (e.g., A MX NS)",
    )

    args = parser.parse_args()

    if args.record_types:
        result = {"domain": args.domain, "records": {}}
        for rtype in args.record_types:
            result["records"][rtype.upper()] = query_record(args.domain, rtype.upper())
    else:
        result = run_dns_lookup(args.domain)

    if args.json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"[+] DNS Records for: {result['domain']}")
        for rtype, records in result["records"].items():
            print(f"    {rtype:>6}: {', '.join(records)}")


if __name__ == "__main__":
    main()

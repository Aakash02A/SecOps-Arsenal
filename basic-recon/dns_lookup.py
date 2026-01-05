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
        "records": {}
    }

    for rtype in record_types:
        result["records"][rtype] = query_record(domain, rtype)

    return result

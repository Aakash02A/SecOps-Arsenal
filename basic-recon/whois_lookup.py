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
        "raw": ""
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
            "domain": domain
        }

print(run_whois("google.com"))

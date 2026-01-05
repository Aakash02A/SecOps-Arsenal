import requests
import socket

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
    except:
        return None


def get_hostname(ip: str) -> str:
    """Reverse DNS lookup for hostname."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
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
        "raw": {}
    }

    # Query API
    data = get_ipinfo_api(ip)

    if data:
        result.update(data)
        result["raw"] = data

    return result

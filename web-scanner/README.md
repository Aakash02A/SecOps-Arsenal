# Web Application Scanner

A lightweight Python tool that acts as a basic web vulnerability scanner. It performs checks that are commonly part of the reconnaissance and vulnerability discovery phases of a penetration test or a blue team web audit.

## Features

1. **Security Header Audit**: Checks for the presence of crucial HTTP security headers (like `Strict-Transport-Security`, `Content-Security-Policy`, and `X-Frame-Options`) and flags information disclosure headers like `Server` or `X-Powered-By`.
2. **TLS/SSL Inspection**: Connects directly via sockets to pull the SSL certificate. It verifies who issued the certificate and checks if it will expire within the next 30 days.
3. **Common Exposures Check**: Attempts to load common files that should not be publicly accessible (such as `.env`, `.git/config`, `phpinfo.php`) and checks for `robots.txt`.

## Prerequisites

Requires the `requests` library:

```bash
pip install requests
```

*(Note: `urllib3` is used internally by requests and is used here to suppress warnings about insecure certificates when scanning testing environments).*

## Usage

Provide the URL of the web application you wish to scan.

```bash
python scanner.py https://example.com
```

If you omit the protocol, the script defaults to `https://`:

```bash
python scanner.py example.com
```

**⚠️ DISCLAIMER: Only run this scanner against web applications you own or have explicit authorization to test.**

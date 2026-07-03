# API Security Tester

APIs are the backbone of modern web applications, but they are often vulnerable to logical flaws that traditional web scanners miss. This tool automates the testing of common API vulnerabilities as defined by the [OWASP API Security Top 10](https://owasp.org/www-project-api-security/).

## Features

1. **Broken Object Level Authorization (BOLA/IDOR)**: Tests if a user (with a valid token) can access resources belonging to a *different* user just by changing an ID parameter in the URL.
2. **Missing Authentication**: Tests if a supposedly private endpoint allows requests without an Authorization token.
3. **Lack of Rate Limiting**: Sends rapid bursts of traffic to an endpoint to check if the server responds with a `429 Too Many Requests` code, which protects against brute-force and DoS attacks.

## Prerequisites

Requires the `requests` library:

```bash
pip install requests
```

## Usage

You can test a mock or real API by providing the base URL, the endpoint format containing an `{id}` placeholder, a valid auth token, the user's ID, and a target victim's ID.

```bash
python api_tester.py "https://api.example.com" -e "/api/v1/users/{id}/profile" -t "eyJhbGciOi..." -u 1001 -x 1002
```

### Parameters

- `url`: Base URL of the API (e.g., `https://api.example.com`).
- `-e, --endpoint`: The API endpoint to test. Use `{id}` as a placeholder where the user ID goes.
- `-t, --token`: The Bearer token belonging to your test user.
- `-u, --userid`: The ID of your test user.
- `-x, --targetid`: The ID of a *different* user (the BOLA test will attempt to access this ID using your token).

**⚠️ DISCLAIMER: Only run this tester against APIs you own or have explicit authorization to test.**

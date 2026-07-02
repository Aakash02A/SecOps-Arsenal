# Credential Check

This tool helps assess password strength and securely checks if a password has been compromised in a known data breach.

## Features

- **Complexity Tester:** Checks for minimum length (8 chars), uppercase, lowercase, numbers, and special characters.
- **Breach Lookup:** Queries the [Have I Been Pwned API](https://haveibeenpwned.com/API/v3) using $k$-Anonymity. It only sends the first 5 characters of the SHA-1 hashed password, ensuring the actual password or its full hash is never transmitted over the network.

## Prerequisites

Requires the `requests` library for querying the external API:

```bash
pip install requests
```

## Usage

Check a password for complexity and breach status:

```bash
python credential_checker.py "YourP@ssw0rd!"
```

To evaluate complexity only and skip the Have I Been Pwned breach check:

```bash
python credential_checker.py "YourP@ssw0rd!" --no-breach
```

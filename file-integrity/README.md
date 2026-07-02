# File Integrity Monitor (FIM)

A basic File Integrity Monitoring tool designed to detect unauthorized changes to files within a directory. 

## How It Works

1. **Build a Baseline:** The tool recursively hashes all files in a specified directory (using SHA-256 by default) and saves the results to a JSON baseline file.
2. **Check/Monitor:** It later re-hashes the directory and compares the current hashes against the saved baseline, alerting you to:
   - New files
   - Modified files
   - Deleted files

## Usage

### 1. Build a Baseline

Create a baseline of known-good file states.

```bash
python fim.py build /path/to/directory
```
*Options:*
- `-o`: Specify an output file (default: `baseline.json`)
- `-a`: Specify hash algorithm (`md5`, `sha1`, `sha256`, `sha512`)

### 2. Check Integrity

Perform a one-time check against the saved baseline.

```bash
python fim.py check /path/to/directory
```

### 3. Continuous Monitoring

Continuously monitor a directory, checking for changes at a set interval.

```bash
# Monitor every 10 seconds (default)
python fim.py monitor /path/to/directory

# Monitor every 30 seconds
python fim.py monitor /path/to/directory -i 30
```

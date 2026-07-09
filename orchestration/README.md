# SOAR-Lite Orchestration Engine

SOAR (Security Orchestration, Automation, and Response) platforms act as the connective tissue in a modern SOC. They ingest alerts from SIEMs or IDSes, evaluate them against predefined "Playbooks", and automatically execute response actions.

This project is a lightweight, Dockerized SOAR engine.

## How It Works

1. **Alert Ingestion**: The engine (`soar_engine.py`) reads incoming security alerts formatted as JSON (e.g., `sample_alerts.json`).
2. **Playbook Matching**: It looks at the alert's `type` and finds a matching playbook in `playbooks.yaml`.
3. **Action Execution**: It executes the actions defined in the playbook. Crucially, it takes contextual data from the JSON alert (like the attacker's IP or the compromised username) and dynamically injects them into the automation scripts we built in **Project 10 (`automations/`)**.

## Included Files

- `soar_engine.py`: The core orchestrator.
- `playbooks.yaml`: The logical workflows defining how to respond to specific threats.
- `sample_alerts.json`: A mock feed of alerts to test the engine.
- `Dockerfile` & `requirements.txt`: To run the engine in a consistent, containerized environment.

## Usage

### Local Testing

You can run the engine directly with Python (requires `PyYAML`):

```bash
pip install -r requirements.txt
python soar_engine.py sample_alerts.json
```

### Dockerized Execution

In a production environment, SOAR engines run as persistent microservices. You can build and run this engine in Docker:

```bash
# Build the image
docker build -t soar-lite .

# Run the container (it will execute against sample_alerts.json by default)
docker run --rm soar-lite
```

Watch as the engine parses the JSON, matches the `RANSOMWARE_DETECTED` alert to the appropriate playbook, and dynamically generates the commands to lock the account and send an email!

# SIEM Ingestion Tools (ELK Stack)

This project demonstrates how to ingest security logs into a SIEM (Security Information and Event Management) system. We use the ELK stack (Elasticsearch, Logstash, Kibana) as our SIEM platform.

## Included Files

1. **`docker-compose.yml`**: A configuration file to spin up a local instance of Elasticsearch and Kibana quickly.
2. **`logstash.conf`**: A sample Logstash configuration file showing how to parse raw Apache access logs, enrich them with GeoIP data, and send them to Elasticsearch.
3. **`ingest_data.py`**: A Python script using the `elasticsearch` library to bulk-ingest JSON data into an index. You can use the JSON output from **Project 5 (`log-parser/`)** as your data source.

## Prerequisites

- **Docker & Docker Compose**: Required to spin up the local ELK stack.
- **Python libraries**: If you plan to use the Python script.

```bash
pip install elasticsearch
```

## Usage

### 1. Start the SIEM (Elasticsearch + Kibana)

Navigate to this directory and start the containers:

```bash
docker-compose up -d
```

Wait a minute or two for the services to fully start.
- **Elasticsearch** is running on `http://localhost:9200`
- **Kibana** is running on `http://localhost:5601`

### 2. Ingest Data via Python (Easiest)

If you generated a `parsed_logs.json` file in Project #5 (`log-parser`), you can ingest it directly into Elasticsearch:

```bash
python ingest_data.py ../log-parser/parsed_logs.json -i "web-traffic-logs"
```

### 3. Explore the Data in Kibana

1. Open your browser and go to `http://localhost:5601`.
2. Go to **Stack Management** > **Data Views** (or Index Patterns) and create a Data View for `web-traffic-logs` (or whatever index you named).
3. Go to **Discover** to query, filter, and view your logs.

### 4. Stopping the Environment

To shut down the SIEM and remove the containers:

```bash
docker-compose down
```
*(Warning: This will delete your indexed data since we didn't mount persistent volumes in the basic setup).*

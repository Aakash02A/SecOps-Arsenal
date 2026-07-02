import json
import argparse
import sys
from elasticsearch import Elasticsearch, helpers

def ingest_json(es, index_name, file_path):
    print(f"[*] Reading data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        sys.exit(1)
        
    # Ensure data is a list of documents
    if not isinstance(data, list):
        data = [data]
        
    # Prepare documents for bulk ingestion
    actions = [
        {
            "_index": index_name,
            "_source": doc
        }
        for doc in data
    ]
    
    print(f"[*] Bulk indexing {len(actions)} documents into '{index_name}'...")
    try:
        success, failed = helpers.bulk(es, actions)
        print(f"[+] Successfully indexed {success} documents.")
    except Exception as e:
        print(f"[-] Error during bulk ingestion: {e}")

def main():
    parser = argparse.ArgumentParser(description="SIEM JSON Ingestion Script (Elasticsearch)")
    parser.add_argument("file", help="Path to JSON file containing logs (e.g., from project 5)")
    parser.add_argument("-i", "--index", default="security-logs", help="Target Elasticsearch index (default: security-logs)")
    parser.add_argument("-u", "--url", default="http://localhost:9200", help="Elasticsearch URL (default: http://localhost:9200)")
    
    args = parser.parse_args()
    
    print(f"[*] Connecting to Elasticsearch at {args.url}")
    # Disable timeout limits for large bulk uploads and ignore TLS warnings if testing locally
    es = Elasticsearch(args.url, request_timeout=60)
    
    if not es.ping():
        print("[-] Could not connect to Elasticsearch. Ensure your docker container is running (docker-compose up -d).")
        sys.exit(1)
        
    ingest_json(es, args.index, args.file)

if __name__ == "__main__":
    main()

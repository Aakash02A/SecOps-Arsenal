import json

# Simulated Authentication Logs
auth_logs = [
    {"timestamp": "2024-01-01T10:00:00Z", "ip": "192.168.1.5", "action": "success_login"},
    {"timestamp": "2024-01-01T10:05:00Z", "ip": "10.0.0.99", "action": "failed_login"},
    {"timestamp": "2024-01-01T10:05:05Z", "ip": "10.0.0.99", "action": "failed_login"},
    {"timestamp": "2024-01-01T10:05:10Z", "ip": "10.0.0.99", "action": "failed_login"},
    {"timestamp": "2024-01-01T10:05:15Z", "ip": "10.0.0.99", "action": "success_login"}, # Brute force succeeded
    {"timestamp": "2024-01-01T10:10:00Z", "ip": "203.0.113.5", "action": "failed_login"},
    {"timestamp": "2024-01-01T10:10:05Z", "ip": "203.0.113.5", "action": "failed_login"},
    {"timestamp": "2024-01-01T10:10:10Z", "ip": "203.0.113.5", "action": "failed_login"},
    {"timestamp": "2024-01-01T10:10:15Z", "ip": "203.0.113.5", "action": "success_login"} # Brute force succeeded
]

# Simulated Network Logs (Bytes Sent)
net_logs = [
    {"timestamp": "2024-01-01T10:01:00Z", "src_ip": "192.168.1.5", "dst_ip": "8.8.8.8", "bytes_sent": 5000},
    # 10.0.0.99 exfiltrates 50MB of data (CRITICAL Alert)
    {"timestamp": "2024-01-01T10:06:00Z", "src_ip": "10.0.0.99", "dst_ip": "1.1.1.1", "bytes_sent": 52428800}, 
    # 203.0.113.5 just does normal browsing, 1MB (HIGH Alert, but not critical)
    {"timestamp": "2024-01-01T10:11:00Z", "src_ip": "203.0.113.5", "dst_ip": "8.8.4.4", "bytes_sent": 1048576} 
]

with open('mock_auth.json', 'w') as f:
    json.dump(auth_logs, f, indent=4)
    
with open('mock_net.json', 'w') as f:
    json.dump(net_logs, f, indent=4)
    
print("[+] Created mock_auth.json and mock_net.json for testing.")

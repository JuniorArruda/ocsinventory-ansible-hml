import json
import csv

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    hosts = data.get("zabbix_export", {}).get("hosts", [])
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["host", "ip", "description", "os"])
        
        for host in hosts:
            host_name = host.get("host", "")
            ip = host.get("interfaces", [{}])[0].get("ip", "")
            description = host.get("name", "")
            os_info = next((t["name"] for t in host.get("templates", []) if "Linux" in t["name"] or "Windows" in t["name"]), "")
            
            writer.writerow([host_name, ip, description, os_info])

# Uso do script
json_to_csv("zbx_export_hosts.json", "hosts.csv")

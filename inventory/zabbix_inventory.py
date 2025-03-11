#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar inventário Ansible a partir de hosts do Zabbix
Método: Arquivo de exportação manual
"""

import json
import sys
import os
import argparse
import csv

# Definição do arquivo de hosts (ajuste conforme necessário)
HOSTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zabbix_hosts.csv')

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Inventário Ansible do Zabbix')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true', help='Listar todos os grupos')
    group.add_argument('--host', help='Obter variáveis para host específico')
    return parser.parse_args()

def read_hosts_from_csv():
    """Ler hosts do arquivo CSV exportado do Zabbix"""
    hosts = {}
    groups = {'linux': {'hosts': []}}
    
    try:
        with open(HOSTS_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                hostname = row.get('host', '').strip()
                if not hostname:
                    continue
                
                # Adicionar host à lista
                hosts[hostname] = {
                    'ansible_host': row.get('ip', hostname).strip(),
                    'ansible_user': 'adm_far',
                    'ansible_become': True,
                    'ansible_become_method': 'sudo'
                }
                
                # Adicionar ao grupo linux
                groups['linux']['hosts'].append(hostname)
    except Exception as e:
        sys.stderr.write(f"Erro ao ler arquivo de hosts: {str(e)}\n")
        groups = {'linux': {'hosts': []}}
    
    return hosts, groups

def list_hosts():
    """Listar todos os hosts e grupos"""
    hosts, groups = read_hosts_from_csv()
    return groups

def get_host_vars(host):
    """Obter variáveis para um host específico"""
    hosts, _ = read_hosts_from_csv()
    return hosts.get(host, {})

def main():
    """Função principal"""
    args = parse_args()
    
    if args.list:
        print(json.dumps(list_hosts(), indent=2))
    elif args.host:
        print(json.dumps(get_host_vars(args.host), indent=2))

if __name__ == '__main__':
    main()
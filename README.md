# Projeto Ansible para Instalação do OCS Inventory Agent

Este projeto automatiza a instalação e configuração do OCS Inventory Agent em múltiplas máquinas Linux, utilizando o Zabbix como fonte de hosts.

## Pré-requisitos

- Ansible 2.9+
- Python 3.6+
- Acesso SSH às máquinas de destino
- Usuário com permissões sudo (adm_far)
- Exportação CSV dos hosts do Zabbix

## Estrutura do Projeto

```
.
├── ansible.cfg                  # Configuração do Ansible
├── inventory/                   # Inventário dinâmico
│   ├── zabbix_inventory.py      # Script para inventário do Zabbix
│   └── zabbix_hosts.csv         # Arquivo CSV exportado do Zabbix
├── roles/                       # Roles do Ansible
│   └── ocs_inventory/           # Role para OCS Inventory
├── tasks/                       # Tarefas compartilhadas
│   └── diagnostico.yml          # Script de diagnóstico
├── templates/                   # Templates compartilhados
│   └── diagnostico_report.j2    # Template de relatório
├── files/                       # Arquivos estáticos
│   └── packages/                # Pacotes para instalação local
├── playbook.yml                 # Playbook principal
├── rollback.yml                 # Playbook de rollback
└── group_vars/                  # Variáveis globais
    └── all.yml                  # Configurações globais
```

## Preparação do Ambiente

1. **Exportar hosts do Zabbix**:
   - Acesse o Zabbix e exporte a lista de hosts
   - Salve como CSV no formato esperado (veja exemplo em `inventory/zabbix_hosts.csv`)

2. **Preparar pacotes locais (opcional)**:
   - Para ambientes sem acesso à internet
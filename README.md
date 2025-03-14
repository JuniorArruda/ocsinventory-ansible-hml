# Projeto Ansible para Instalação do OCS Inventory Agent

Este projeto automatiza a instalação e configuração do OCS Inventory Agent em múltiplas máquinas Linux, utilizando o Zabbix como fonte de hosts.

## Pré-requisitos

- Ansible 2.9+
- Python 3.6+
- Acesso SSH às máquinas de destino
- Usuário com permissões sudo
- Exportação CSV dos hosts do Zabbix

## Estrutura do Projeto

1. **Exportar hosts do Zabbix**:
   - Acesse o Zabbix e exporte a lista de hosts
   - Salve como CSV no formato esperado (veja exemplo em `inventory/hosts.csv`)

2. **Preparar pacotes locais (opcional)**:
   - Para ambientes sem acesso à internet

SETUP

# Clonar repositório

git clone https://github.com/JuniorArruda/ocsinventory-ansible-hml.git

# No arquivo ansible.conf altere o parâmetro abaixo substituindo linuxuser por um usuário sudoer do seu ambiente

remote_user = linuxuser

# No arquivo inventory/group_var/all.yml altere '10.2.100.50' para o ip do seu servidor OCS inventory nas duas linhas abaixo

ocs_server_url: "http://10.2.100.50/ocsinventory/"
ocs_server_host: "10.2.100.50"

# Atualize o csv com inventário de acordo com seu ambiente e necessidade

inventory/hosts.csv

# Criar um arquivo criptografado para armazenar a senha
ansible-vault create inventory/group_vars/all/vault.yml

No editor que se abre, adicione:

ansible_sudo_pass: "sua_senha_aqui"

# Testar o inventário
./inventory/inventory.py --list

Preparar os pacotes locais (se você optou por usar pacotes locais):
files/packages/debian, files/packages/redhat, files/packages/suse, etc...
# Baixe e coloque os pacotes nos diretórios correspondentes

ansible all -m ping --ask-vault-pass

Executar apenas o diagnóstico para verificar se todas as máquinas estão prontas:

ansible-playbook playbook.yml --tags diagnose --ask-vault-pass

Executar o playbook completo para instalar e configurar o OCS Inventory Agent:

ansible-playbook playbook.yml --ask-vault-pass

Verificar o status da instalação:

ansible all -i inventory/inventory.py -m shell -a "ps aux | grep ocsinventory-agent | grep -v grep" --ask-vault-pass

Se necessário, forçar a execução do inventário em todos os hosts:

ansible all -i inventory/inventory.py -m shell -a "/usr/local/bin/run-ocs-agent.sh" --ask-vault-pass

Em caso de problemas, executar o rollback:

ansible-playbook rollback.yml

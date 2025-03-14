# 📌 Projeto Ansible para Instalação do OCS Inventory Agent

Este projeto automatiza a instalação e configuração do **OCS Inventory Agent** em múltiplas máquinas Linux, utilizando o **Zabbix** como fonte de hosts.

---

## ✅ Pré-requisitos

- **Ansible** 2.9+
- **Python** 3.6+
- Acesso **SSH** às máquinas de destino
- Usuário com permissões **sudo**
- Exportação **CSV** dos hosts do Zabbix

---

## 📂 Estrutura do Projeto

1️⃣ **Exportar hosts do Zabbix**  
   - Acesse o **Zabbix** e exporte a lista de hosts
   - Salve como **CSV** no formato esperado (exemplo: `inventory/hosts.csv`)

2️⃣ **Preparar pacotes locais (opcional)**  
   - Para ambientes sem acesso à internet, coloque os pacotes em `files/packages/{distro}`

---

## 🚀 Setup e Configuração

### 🔹 Clonar o repositório
```bash
git clone https://github.com/JuniorArruda/ocsinventory-ansible-hml.git
cd ocsinventory-ansible-hml
```

### 🔹 Configurar variáveis essenciais
#### 1️⃣ **Definir usuário sudoer**
Edite o arquivo `ansible.conf` e altere:
```ini
remote_user = linuxuser  # Substitua 'linuxuser' pelo usuário sudoer do seu ambiente
```

#### 2️⃣ **Configurar o servidor OCS Inventory**
Edite o arquivo `inventory/group_vars/all.yml` e substitua `10.2.100.50` pelo IP do seu servidor OCS Inventory:
```yaml
ocs_server_url: "http://10.2.100.50/ocsinventory/"
ocs_server_host: "10.2.100.50"
```

#### 3️⃣ **Atualizar o inventário de hosts**
Edite `inventory/hosts.csv` conforme seu ambiente.

#### 4️⃣ **Criar um arquivo criptografado para armazenar senha**
```bash
ansible-vault create inventory/group_vars/all/vault.yml
```
No editor que se abre, adicione:
```yaml
ansible_sudo_pass: "sua_senha_aqui"
```

---

## 🔍 Testando e Executando

### 🔹 Testar conexão com os hosts
```bash
ansible all -m ping --ask-vault-pass
```

### 🔹 Diagnóstico inicial (verifica se os hosts estão prontos)
```bash
ansible-playbook playbook.yml --tags diagnose --ask-vault-pass
```

### 🔹 Executar instalação completa do OCS Inventory Agent
```bash
ansible-playbook playbook.yml --ask-vault-pass
```

### 🔹 Verificar status da instalação
```bash
ansible all -i inventory/inventory.py -m shell -a "ps aux | grep ocsinventory-agent | grep -v grep" --ask-vault-pass
```

### 🔹 Forçar execução do inventário nos hosts
```bash
ansible all -i inventory/inventory.py -m shell -a "/usr/local/bin/run-ocs-agent.sh" --ask-vault-pass
```

### 🔹 Rollback (caso necessário)
```bash
ansible-playbook rollback.yml
```

---

## 📌 Notas Finais

🚨 **OBS:** Tentamos centralizar as variáveis no arquivo `global.yml`, mas isso quebrou o projeto. Talvez tentemos novamente no futuro.

📌 Este projeto facilita futuras implantações e configurações do OCS Inventory Agent, permitindo que usuários alterem apenas um único arquivo para apontar para seus servidores e definir o usuário sudoer.

👨‍💻 Desenvolvido por [JuniorArruda](https://github.com/JuniorArruda)


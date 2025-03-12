#!/bin/bash

# Diretório do projeto (padrão: diretório atual)
PROJECT_DIR="${1:-$(pwd)}"
OUTPUT_FILE="project_overview.txt"
SCRIPT_NAME=$(basename "$0")

# Limpar ou criar o arquivo de saída
echo "" > "$OUTPUT_FILE"

# Encontrar todos os arquivos no projeto, ignorando .git, arquivos .env*, o próprio script e o arquivo de saída
mapfile -t FILES < <(find "$PROJECT_DIR" -type f ! -path "*/.git/*" ! -name "$SCRIPT_NAME" ! -name "$OUTPUT_FILE" ! -name ".env*" | nl)

# Exibir lista de arquivos numerada
echo "Arquivos encontrados no projeto:" 
for FILE in "${FILES[@]}"; do
    FILE_NUMBER=$(echo "$FILE" | awk '{print $1}')
    FILE_PATH=$(echo "$FILE" | awk '{ $1=""; print substr($0,2) }')
    RELATIVE_PATH=${FILE_PATH#"$PROJECT_DIR/"}
    echo "$FILE_NUMBER - $RELATIVE_PATH" 
    echo "---------------------------------------------------"
done

echo "" | tee -a "$OUTPUT_FILE"
echo "Informe os números dos arquivos que deseja incluir no prompt (separados por espaço e/ou intervalos como 5-9):"
read -r FILE_NUMS

echo "" | tee -a "$OUTPUT_FILE"
echo "=== Informações do Projeto ===" | tee -a "$OUTPUT_FILE"

echo -e "\nEstrutura de diretórios do projeto:\n" | tee -a "$OUTPUT_FILE"
tree -L 10 "$PROJECT_DIR" | tee -a "$OUTPUT_FILE"

echo -e "\nConteúdo dos arquivos selecionados:\n" | tee -a "$OUTPUT_FILE"

# Função para expandir intervalos numéricos
expand_numbers() {
    local input="$1"
    local result=()
    for item in $input; do
        if [[ "$item" =~ ^[0-9]+-[0-9]+$ ]]; then
            IFS='-' read -r start end <<< "$item"
            for ((i=start; i<=end; i++)); do
                result+=("$i")
            done
        else
            result+=("$item")
        fi
    done
    echo "${result[@]}"
}

# Expandir intervalos
EXPANDED_NUMS=$(expand_numbers "$FILE_NUMS")

for NUM in $EXPANDED_NUMS; do
    FILE_PATH=$(echo "${FILES[$((NUM-1))]}" | awk '{ $1=""; print substr($0,2) }')
    RELATIVE_PATH=${FILE_PATH#"$PROJECT_DIR/"}
    if [ -f "$FILE_PATH" ]; then
        echo -e "\n=== $RELATIVE_PATH ===\n" | tee -a "$OUTPUT_FILE"
        cat "$FILE_PATH" | tee -a "$OUTPUT_FILE"
    fi
done

echo -e "\nResumo salvo em $OUTPUT_FILE"

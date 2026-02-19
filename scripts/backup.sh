#!/bin/bash

# =============================================================================
# Home Security DIY - Automated Backup Script
# =============================================================================
# Faz backup das configurações e do banco de dados PostgreSQL.
#
# Uso: ./backup.sh [backup_dir]
#   BACKUP_ENV=docker   (padrão) — usa docker exec para acessar o PostgreSQL
#   BACKUP_ENV=k8s      — usa kubectl exec para acessar o PostgreSQL
#
# Recomendado: Adicionar ao cron (ex: diário às 3h da manhã)
#   0 3 * * * /path/to/scripts/backup.sh >> /var/log/home-security-backup.log 2>&1
#
# Rotação de backups PostgreSQL:
#   daily/    — retém os últimos 7 dias
#   weekly/   — retém as últimas 4 semanas (todo domingo)
#   monthly/  — retém os últimos 12 meses (dia 1 de cada mês)
# =============================================================================

# --- Configuração ---
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$PROJECT_ROOT/src"
DEFAULT_BACKUP_DIR="$PROJECT_ROOT/backups"
BACKUP_DIR="${1:-$DEFAULT_BACKUP_DIR}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=30
LOG_FILE="$BACKUP_DIR/backup.log"
BACKUP_ENCRYPTION_PASSPHRASE="${BACKUP_ENCRYPTION_PASSPHRASE:-}"

# Ambiente de execução: docker (padrão) ou k8s
BACKUP_ENV="${BACKUP_ENV:-docker}"

# Configurações PostgreSQL (lidas do ambiente ou .env)
POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-home-security-postgres}"
POSTGRES_K8S_NAMESPACE="${POSTGRES_K8S_NAMESPACE:-home-security}"
POSTGRES_K8S_STATEFULSET="${POSTGRES_K8S_STATEFULSET:-postgres-0}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_DB="${POSTGRES_DB:-homedb}"
POSTGRES_SCHEMAS=("homeassistant" "dashboard" "metrics")

# Diretórios de configuração para backup (relativo a src/)
DIRS_TO_BACKUP=(
    "homeassistant"
    "zigbee2mqtt"
    "mosquitto/config"
    "frigate/config.yml"
)

# --- Funções auxiliares ---
mkdir -p "$BACKUP_DIR"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Executa pg_dump no container correto (Docker ou K8s)
pg_dump_remote() {
    local args="$*"
    if [ "$BACKUP_ENV" = "k8s" ]; then
        kubectl exec -n "$POSTGRES_K8S_NAMESPACE" "$POSTGRES_K8S_STATEFULSET" \
            -- bash -c "pg_dump $args"
    else
        docker exec "$POSTGRES_CONTAINER" \
            bash -c "pg_dump $args"
    fi
}

# Verifica se o PostgreSQL está acessível
postgres_is_available() {
    if [ "$BACKUP_ENV" = "k8s" ]; then
        kubectl exec -n "$POSTGRES_K8S_NAMESPACE" "$POSTGRES_K8S_STATEFULSET" \
            -- pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1
    else
        docker exec "$POSTGRES_CONTAINER" \
            pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1
    fi
}

# =============================================================================
# Função: backup_postgres
# Realiza dump completo e por schema, com rotação diária/semanal/mensal
# =============================================================================
backup_postgres() {
    local pg_backup_dir="$BACKUP_DIR/postgres"
    local daily_dir="$pg_backup_dir/daily"
    local weekly_dir="$pg_backup_dir/weekly"
    local monthly_dir="$pg_backup_dir/monthly"
    local day_of_week
    local day_of_month
    day_of_week=$(date +%u)   # 1=Segunda … 7=Domingo
    day_of_month=$(date +%d)  # 01-31

    mkdir -p "$daily_dir" "$weekly_dir" "$monthly_dir"

    log "--- Backup PostgreSQL (ambiente: $BACKUP_ENV) ---"

    if ! postgres_is_available; then
        log "AVISO: PostgreSQL não está acessível. Pulando backup do banco."
        return 1
    fi

    # ------------------------------------------------------------------
    # 1. Full dump (todos os schemas) — sempre executado
    # ------------------------------------------------------------------
    local full_dump="$daily_dir/full_${TIMESTAMP}.dump"
    log "Criando dump completo: $full_dump"

    if pg_dump_remote "-U $POSTGRES_USER -d $POSTGRES_DB -Fc" > "$full_dump" 2>> "$LOG_FILE"; then
        local size
        size=$(du -h "$full_dump" | cut -f1)
        log "Dump completo criado com sucesso. Tamanho: $size"
    else
        log "ERRO: Falha ao criar dump completo do PostgreSQL!"
        rm -f "$full_dump"
        return 1
    fi

    # ------------------------------------------------------------------
    # 2. Dumps por schema (incremental por domínio de aplicação)
    # ------------------------------------------------------------------
    for schema in "${POSTGRES_SCHEMAS[@]}"; do
        local schema_dump="$daily_dir/${schema}_${TIMESTAMP}.dump"
        log "Criando dump do schema '$schema': $schema_dump"

        if pg_dump_remote "-U $POSTGRES_USER -d $POSTGRES_DB -n $schema -Fc" > "$schema_dump" 2>> "$LOG_FILE"; then
            local schema_size
            schema_size=$(du -h "$schema_dump" | cut -f1)
            log "Schema '$schema' ok. Tamanho: $schema_size"
        else
            log "AVISO: Falha no dump do schema '$schema'."
            rm -f "$schema_dump"
        fi
    done

    # ------------------------------------------------------------------
    # 3. Backup semanal (todo domingo)
    # ------------------------------------------------------------------
    if [ "$day_of_week" = "7" ]; then
        local weekly_dump="$weekly_dir/full_$(date +%Y-W%V).dump"
        log "Criando backup semanal: $weekly_dump"
        cp "$full_dump" "$weekly_dump" 2>> "$LOG_FILE" && \
            log "Backup semanal criado: $weekly_dump" || \
            log "AVISO: Falha ao criar backup semanal."
    fi

    # ------------------------------------------------------------------
    # 4. Backup mensal (dia 1 de cada mês)
    # ------------------------------------------------------------------
    if [ "$day_of_month" = "01" ]; then
        local monthly_dump="$monthly_dir/full_$(date +%Y-%m).dump"
        log "Criando backup mensal: $monthly_dump"
        cp "$full_dump" "$monthly_dump" 2>> "$LOG_FILE" && \
            log "Backup mensal criado: $monthly_dump" || \
            log "AVISO: Falha ao criar backup mensal."
    fi

    # ------------------------------------------------------------------
    # 5. Rotação e retenção
    # ------------------------------------------------------------------
    log "Aplicando política de retenção de backups PostgreSQL..."

    # Daily: últimos 7 dias
    find "$daily_dir" -name "*.dump" -type f -mtime +7 -delete -print >> "$LOG_FILE"

    # Weekly: últimas 4 semanas (28 dias)
    find "$weekly_dir" -name "*.dump" -type f -mtime +28 -delete -print >> "$LOG_FILE"

    # Monthly: últimos 12 meses (365 dias)
    find "$monthly_dir" -name "*.dump" -type f -mtime +365 -delete -print >> "$LOG_FILE"

    log "--- Backup PostgreSQL concluído ---"
}

# =============================================================================
# Backup das configurações (tar/gzip)
# =============================================================================
log "Iniciando backup do Home Security DIY..."

ARCHIVE_NAME="home_security_configs_$TIMESTAMP.tar.gz"
log "Criando arquivo de configurações: $ARCHIVE_NAME"

EXISTING_DIRS=()
for dir in "${DIRS_TO_BACKUP[@]}"; do
    if [ -e "$SRC_DIR/$dir" ]; then
        EXISTING_DIRS+=("$dir")
    else
        log "AVISO: Ignorando diretório ausente: $SRC_DIR/$dir"
    fi
done

if [ ${#EXISTING_DIRS[@]} -gt 0 ]; then
    cd "$SRC_DIR" || exit 1
    tar \
        --exclude='*.db-wal' \
        --exclude='*.db-shm' \
        --exclude='homeassistant/home-assistant_v2.db' \
        -czf "$BACKUP_DIR/$ARCHIVE_NAME" \
        "${EXISTING_DIRS[@]}" 2>> "$LOG_FILE"

    if [ $? -eq 0 ]; then
        size=$(du -h "$BACKUP_DIR/$ARCHIVE_NAME" | cut -f1)
        log "Configurações salvas: $BACKUP_DIR/$ARCHIVE_NAME ($size)"
    else
        log "ERRO: Falha ao criar backup das configurações!"
        exit 1
    fi

    if [ -n "$BACKUP_ENCRYPTION_PASSPHRASE" ]; then
        ENCRYPTED_ARCHIVE="$BACKUP_DIR/${ARCHIVE_NAME}.enc"
        log "Criptografando backup de configurações em: $ENCRYPTED_ARCHIVE"
        if openssl enc -aes-256-cbc -salt -pbkdf2 \
            -in "$BACKUP_DIR/$ARCHIVE_NAME" \
            -out "$ENCRYPTED_ARCHIVE" \
            -pass "env:BACKUP_ENCRYPTION_PASSPHRASE" 2>> "$LOG_FILE"; then
            rm -f "$BACKUP_DIR/$ARCHIVE_NAME"
            log "Backup criptografado com sucesso."
        else
            log "ERRO: Falha ao criptografar backup."
            exit 1
        fi
    fi
else
    log "AVISO: Nenhuma configuração encontrada para backup."
fi

# Retenção das configurações (30 dias)
log "Limpando backups de configuração com mais de $RETENTION_DAYS dias..."
find "$BACKUP_DIR" -maxdepth 1 -name "home_security_configs_*.tar.gz" \
    -type f -mtime +$RETENTION_DAYS -delete -print >> "$LOG_FILE"
find "$BACKUP_DIR" -maxdepth 1 -name "home_security_configs_*.tar.gz.enc" \
    -type f -mtime +$RETENTION_DAYS -delete -print >> "$LOG_FILE"

# =============================================================================
# Backup do PostgreSQL
# =============================================================================
backup_postgres

log "Backup concluído com sucesso."
exit 0

#!/bin/bash
# =============================================================================
# PostgreSQL Initialization Script — Home Security DIY
# Executado automaticamente no primeiro boot do container PostgreSQL.
# Lê senhas das variáveis de ambiente para evitar credenciais hardcoded.
# =============================================================================
set -euo pipefail

echo "[postgres-init] Iniciando configuração do banco de dados..."

psql -v ON_ERROR_STOP=1 \
     --username "$POSTGRES_USER" \
     --dbname "$POSTGRES_DB" <<-EOSQL

    ---------------------------------------------------------------------------
    -- Usuários de serviço com senhas injetadas via variáveis de ambiente
    ---------------------------------------------------------------------------
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ha_user') THEN
            CREATE USER ha_user WITH PASSWORD '${POSTGRES_HA_PASSWORD}';
            RAISE NOTICE 'Usuário ha_user criado.';
        ELSE
            ALTER USER ha_user WITH PASSWORD '${POSTGRES_HA_PASSWORD}';
            RAISE NOTICE 'Senha do ha_user atualizada.';
        END IF;

        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'dashboard_user') THEN
            CREATE USER dashboard_user WITH PASSWORD '${POSTGRES_DASHBOARD_PASSWORD}';
            RAISE NOTICE 'Usuário dashboard_user criado.';
        ELSE
            ALTER USER dashboard_user WITH PASSWORD '${POSTGRES_DASHBOARD_PASSWORD}';
            RAISE NOTICE 'Senha do dashboard_user atualizada.';
        END IF;

        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'metrics_user') THEN
            CREATE USER metrics_user WITH PASSWORD '${POSTGRES_METRICS_PASSWORD}';
            RAISE NOTICE 'Usuário metrics_user criado.';
        ELSE
            ALTER USER metrics_user WITH PASSWORD '${POSTGRES_METRICS_PASSWORD}';
            RAISE NOTICE 'Senha do metrics_user atualizada.';
        END IF;
    END
    \$\$;

    ---------------------------------------------------------------------------
    -- Schemas isolados por domínio de aplicação
    ---------------------------------------------------------------------------
    CREATE SCHEMA IF NOT EXISTS homeassistant AUTHORIZATION ha_user;
    CREATE SCHEMA IF NOT EXISTS dashboard AUTHORIZATION dashboard_user;
    CREATE SCHEMA IF NOT EXISTS metrics AUTHORIZATION metrics_user;

    ---------------------------------------------------------------------------
    -- Permissões de conexão ao banco
    ---------------------------------------------------------------------------
    GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ha_user, dashboard_user, metrics_user;

    -- Revogar acesso ao schema público para usuários de serviço
    REVOKE ALL ON SCHEMA public FROM ha_user, dashboard_user, metrics_user;

    ---------------------------------------------------------------------------
    -- Schema: homeassistant (Home Assistant recorder)
    ---------------------------------------------------------------------------
    GRANT USAGE ON SCHEMA homeassistant TO ha_user;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA homeassistant TO ha_user;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA homeassistant TO ha_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA homeassistant GRANT ALL ON TABLES TO ha_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA homeassistant GRANT ALL ON SEQUENCES TO ha_user;

    ---------------------------------------------------------------------------
    -- Schema: dashboard (Dashboard operacional — Issue #2)
    ---------------------------------------------------------------------------
    GRANT USAGE ON SCHEMA dashboard TO dashboard_user;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA dashboard TO dashboard_user;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA dashboard TO dashboard_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA dashboard GRANT ALL ON TABLES TO dashboard_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA dashboard GRANT ALL ON SEQUENCES TO dashboard_user;

    ---------------------------------------------------------------------------
    -- Schema: metrics (Métricas do sistema)
    ---------------------------------------------------------------------------
    GRANT USAGE ON SCHEMA metrics TO metrics_user;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA metrics TO metrics_user;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA metrics TO metrics_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA metrics GRANT ALL ON TABLES TO metrics_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA metrics GRANT ALL ON SEQUENCES TO metrics_user;

    ---------------------------------------------------------------------------
    -- Configurações de banco
    ---------------------------------------------------------------------------
    ALTER DATABASE ${POSTGRES_DB} SET timezone TO 'America/Sao_Paulo';

    -- Documentação
    COMMENT ON SCHEMA homeassistant IS 'Home Assistant: histórico de estados e eventos (recorder)';
    COMMENT ON SCHEMA dashboard     IS 'Dashboard operacional: dados em tempo real (Issue #2)';
    COMMENT ON SCHEMA metrics       IS 'Métricas do sistema de segurança (sensores, câmeras, drones)';

EOSQL

echo "[postgres-init] Configuração concluída com sucesso."
echo "[postgres-init] Schemas criados: homeassistant, dashboard, metrics"

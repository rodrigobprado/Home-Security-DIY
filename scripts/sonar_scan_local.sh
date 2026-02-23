#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   SONAR_TOKEN=<token> scripts/sonar_scan_local.sh
# Optional env vars:
#   SONAR_PROJECT_KEY (default: Home-Security-DIY)
#   SONAR_HOST_URL    (default: https://sonar.toca.lan)
#   SONAR_SOURCES     (default: .)
# Extra sonar-scanner arguments can be passed to this script.

SONAR_PROJECT_KEY="${SONAR_PROJECT_KEY:-Home-Security-DIY}"
SONAR_HOST_URL="${SONAR_HOST_URL:-https://sonar.toca.lan}"
SONAR_SOURCES="${SONAR_SOURCES:-.}"
SONAR_TOKEN="${SONAR_TOKEN:-}"

if [[ -z "$SONAR_TOKEN" ]]; then
  echo "ERRO: defina SONAR_TOKEN com o token do SonarQube." >&2
  echo "Exemplo: SONAR_TOKEN=*** scripts/sonar_scan_local.sh" >&2
  exit 1
fi

MKCERT_CAROOT="${MKCERT_CAROOT:-}"
if [[ -z "$MKCERT_CAROOT" ]]; then
  if command -v mkcert >/dev/null 2>&1; then
    MKCERT_CAROOT="$(mkcert -CAROOT)"
  else
    MKCERT_CAROOT="$HOME/.local/share/mkcert"
  fi
fi

MKCERT_ROOT_CA="$MKCERT_CAROOT/rootCA.pem"
if [[ ! -f "$MKCERT_ROOT_CA" ]]; then
  echo "ERRO: rootCA do mkcert não encontrada em: $MKCERT_ROOT_CA" >&2
  echo "Instale/configure mkcert e gere a CA local antes de rodar o scanner." >&2
  exit 1
fi

TRUSTSTORE_DIR="${SONAR_TRUSTSTORE_DIR:-.sonar-local}"
TRUSTSTORE_PATH="$TRUSTSTORE_DIR/mkcert-truststore.p12"
TRUSTSTORE_PASSWORD="${SONAR_TRUSTSTORE_PASSWORD:-changeit}"

mkdir -p "$TRUSTSTORE_DIR"
rm -f "$TRUSTSTORE_PATH"

keytool -importcert \
  -noprompt \
  -alias mkcert-local-ca \
  -file "$MKCERT_ROOT_CA" \
  -keystore "$TRUSTSTORE_PATH" \
  -storetype PKCS12 \
  -storepass "$TRUSTSTORE_PASSWORD" >/dev/null

SONAR_SCANNER_OPTS="${SONAR_SCANNER_OPTS:-} -Djavax.net.ssl.trustStore=$TRUSTSTORE_PATH -Djavax.net.ssl.trustStorePassword=$TRUSTSTORE_PASSWORD -Djavax.net.ssl.trustStoreType=PKCS12"
export SONAR_SCANNER_OPTS

sonar-scanner \
  -Dsonar.projectKey="$SONAR_PROJECT_KEY" \
  -Dsonar.sources="$SONAR_SOURCES" \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.login="$SONAR_TOKEN" \
  "$@"

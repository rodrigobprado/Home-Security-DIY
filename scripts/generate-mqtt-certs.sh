#!/usr/bin/env bash
# =============================================================================
# generate-mqtt-certs.sh — Self-signed TLS certificates for Mosquitto MQTT
# Home Security DIY
# =============================================================================
# Generates a local CA + server certificate for TLS on port 8883.
# Output: src/mosquitto/certs/{ca.crt, ca.key, server.crt, server.key}
#
# Usage:
#   bash scripts/generate-mqtt-certs.sh [--days DAYS] [--cn COMMON_NAME]
#
# After running:
#   1. Uncomment the TLS block in src/mosquitto/config/mosquitto.conf
#   2. Mount src/mosquitto/certs/ into the container at /mosquitto/certs/
#   3. Expose port 8883 instead of (or alongside) 1883
#   4. Add ca.crt to client trust stores (HA, Zigbee2MQTT, etc.)
#
# IMPORTANT: Never commit the generated .key files to git.
#   Add src/mosquitto/certs/*.key to .gitignore.
# =============================================================================
set -euo pipefail

DAYS="${DAYS:-3650}"
CN="${CN:-mqtt.home.local}"
CERTS_DIR="src/mosquitto/certs"

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    --days) DAYS="$2"; shift 2 ;;
    --cn)   CN="$2";   shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

command -v openssl >/dev/null 2>&1 || { echo "openssl is required but not installed." >&2; exit 1; }

mkdir -p "$CERTS_DIR"

echo "==> Generating self-signed MQTT TLS certificates"
echo "    Output : $CERTS_DIR"
echo "    CN     : $CN"
echo "    Expiry : $DAYS days"
echo

# --- 1. Generate CA key + self-signed cert ---
echo "[1/4] Generating CA private key..."
openssl genrsa -out "$CERTS_DIR/ca.key" 4096

echo "[2/4] Generating CA certificate..."
openssl req -new -x509 -days "$DAYS" \
  -key "$CERTS_DIR/ca.key" \
  -out "$CERTS_DIR/ca.crt" \
  -subj "/CN=Home-Security-MQTT-CA/O=HomeSecurityDIY/C=BR"

# --- 2. Generate server key + CSR + sign with CA ---
echo "[3/4] Generating server private key and CSR..."
openssl genrsa -out "$CERTS_DIR/server.key" 4096
openssl req -new \
  -key "$CERTS_DIR/server.key" \
  -out "$CERTS_DIR/server.csr" \
  -subj "/CN=$CN/O=HomeSecurityDIY/C=BR"

echo "[4/4] Signing server certificate with CA..."
openssl x509 -req -days "$DAYS" \
  -in "$CERTS_DIR/server.csr" \
  -CA "$CERTS_DIR/ca.crt" \
  -CAkey "$CERTS_DIR/ca.key" \
  -CAcreateserial \
  -out "$CERTS_DIR/server.crt"

# --- Cleanup CSR (not needed after signing) ---
rm -f "$CERTS_DIR/server.csr" "$CERTS_DIR/ca.srl"

# --- Set restrictive permissions on private keys ---
chmod 600 "$CERTS_DIR/ca.key" "$CERTS_DIR/server.key"
chmod 644 "$CERTS_DIR/ca.crt" "$CERTS_DIR/server.crt"

echo
echo "==> Certificates generated successfully:"
ls -lh "$CERTS_DIR"
echo
echo "==> Next steps:"
echo "    1. Edit src/mosquitto/config/mosquitto.conf"
echo "       Uncomment the TLS listener block (port 8883)"
echo "    2. Mount $CERTS_DIR/ into container at /mosquitto/certs/"
echo "       Add to docker-compose.yml volumes:"
echo "         - ./mosquitto/certs:/mosquitto/certs:ro"
echo "    3. Distribute ca.crt to all MQTT clients:"
echo "       - Home Assistant: Settings → Integrations → MQTT → CA certificate"
echo "       - Zigbee2MQTT: advanced.ssl_ca in zigbee2mqtt/configuration.yaml"
echo "    4. Ensure *.key files are in .gitignore (NEVER commit private keys)"
echo
echo "Certificate info:"
openssl x509 -noout -subject -dates -in "$CERTS_DIR/server.crt"

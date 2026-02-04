#!/bin/bash

# Query Consent Script
# Query consent data by citizen_id

set -e

CITIZEN_ID="$1"
ENV_FILE="${2:-.env.sit}"

if [ -z "$CITIZEN_ID" ]; then
    echo "Usage: $0 <citizen_id> [env-file]"
    echo "Example: $0 1234567890123"
    echo "Example: $0 1234567890123 .env.uat"
    exit 1
fi

echo "========================================"
echo "Query Consent for Citizen: $CITIZEN_ID"
echo "========================================"
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo "ERROR: psql (PostgreSQL client) is not installed"
    exit 1
fi

# Check if environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: Environment file not found: $ENV_FILE"
    exit 1
fi

echo "Loading environment from: $ENV_FILE"
export $(grep -v '^#' "$ENV_FILE" | xargs)

# Check required variables
if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
    echo "ERROR: Missing required database environment variables"
    exit 1
fi

SSL_MODE="${DB_SSL_MODE:-require}"
DB_URL="host=$DB_HOST port=${DB_PORT:-5432} user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$SSL_MODE"

echo "Database: $DB_NAME"
echo ""

# Check if data subject exists
echo "1. Checking Data Subject..."
echo "========================================"
psql "$DB_URL" -c "
SELECT 
    ds.id,
    ds.citizen_id,
    ds.created_at
FROM data_subjects ds
WHERE ds.citizen_id = '$CITIZEN_ID';
" || true

echo ""
echo "2. All Consents..."
echo "========================================"
psql "$DB_URL" -c "
SELECT 
    c.id,
    p.code as purpose_code,
    c.purpose_version,
    dc.code as data_consumer_code,
    c.status,
    c.granted_date,
    c.revoked_date,
    c.created_at
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
JOIN data_consumers dc ON c.dc_id = dc.id
WHERE c.scope_value = '$CITIZEN_ID'
ORDER BY c.created_at DESC;
" || true

echo ""
echo "3. Active Consents Only..."
echo "========================================"
psql "$DB_URL" -c "
SELECT 
    c.id,
    p.code as purpose_code,
    c.purpose_version,
    dc.code as data_consumer_code,
    c.granted_date
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
JOIN data_consumers dc ON c.dc_id = dc.id
WHERE c.scope_value = '$CITIZEN_ID'
AND c.status = 'active'
ORDER BY c.created_at DESC;
" || true

echo ""
echo "4. Audit Trail (Recent)..."
echo "========================================"
# Get consent IDs for this citizen
CONSENT_IDS=$(psql "$DB_URL" -t -c "
SELECT c.id::text
FROM consents c
WHERE c.scope_value = '$CITIZEN_ID'
ORDER BY c.created_at DESC
LIMIT 10;
" 2>/dev/null | tr '\n' ',' | sed 's/,$//')

if [ -n "$CONSENT_IDS" ]; then
    psql "$DB_URL" -c "
SELECT 
    cal.consent_id,
    cal.transaction_id,
    cal.action,
    cal.performed_by,
    cal.performed_at,
    cal.metadata->>'ip_address' as ip_address
FROM consent_audit_logs cal
WHERE cal.consent_id IN ($CONSENT_IDS)
ORDER BY cal.performed_at DESC
LIMIT 20;
    " || true
else
    echo "No consents found for audit trail"
fi

echo ""
echo "========================================"
echo "Query Complete"
echo "========================================"

#!/bin/bash

# Database Connection Script
# Connect to consent service PostgreSQL RDS

set -e

ENV_FILE="${1:-.env.sit}"

echo "========================================"
echo "Consent Service DB Connection"
echo "========================================"
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo "ERROR: psql (PostgreSQL client) is not installed"
    echo "Install with: brew install postgresql (macOS)"
    exit 1
fi

# Check if environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: Environment file not found: $ENV_FILE"
    echo "Usage: $0 [env-file]"
    echo "Example: $0 .env.sit"
    exit 1
fi

echo "Loading environment from: $ENV_FILE"
export $(grep -v '^#' "$ENV_FILE" | xargs)

# Check required variables
if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
    echo "ERROR: Missing required database environment variables"
    echo "Required: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME"
    exit 1
fi

echo "Connecting to database..."
echo "Host: $DB_HOST"
echo "Port: ${DB_PORT:-5432}"
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo ""

# Set SSL mode if not specified
SSL_MODE="${DB_SSL_MODE:-require}"

# Connect to database
psql "host=$DB_HOST port=${DB_PORT:-5432} user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$SSL_MODE" -c "\conninfo"

echo ""
echo "Connected successfully!"
echo ""
echo "Useful queries:"
echo "  \\dt - List tables"
echo "  SELECT COUNT(*) FROM consents; - Count consents"
echo "  SELECT * FROM purposes; - List purposes"
echo ""

# Start interactive session
psql "host=$DB_HOST port=${DB_PORT:-5432} user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$SSL_MODE"

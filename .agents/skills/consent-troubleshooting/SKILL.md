---
name: consent-troubleshooting
description: Troubleshoot the consent service running on AWS EKS with PostgreSQL RDS backend. Use when investigating service health issues, pod failures, database connectivity problems, consent data anomalies, audit log discrepancies, or consent code bugs. Covers Kubernetes diagnostics (pod status, logs, events), PostgreSQL queries for consent/audit data verification, and common issue resolution workflows.
---

# Consent Service Troubleshooting

Troubleshoot the consent service deployed on AWS EKS with PostgreSQL RDS backend.

## Configuration

- **EKS Cluster**: `arn:aws:eks:ap-southeast-7:290768402609:cluster/aux-eks-goqmac0w`
- **Namespace**: `consent`
- **RDS Host**: `aux-rds-goqmac0w.cluster-cpig66gqgrwx.ap-southeast-7.rds.amazonaws.com`
- **Database**: `sit_consent`
- **Credentials**: Load from `.env.sit`, `.env.uat`, or `.env` based on environment

## Workflow Decision Tree

```
START: User reports issue
│
├─► Service unavailable / 500 errors?
│   └─► Check Kubernetes (see Kubernetes Diagnostics)
│       ├─► Pod status: kubectl get pods -n consent
│       ├─► Pod logs: kubectl logs deployment/consent -n consent
│       ├─► Events: kubectl get events -n consent --sort-by='.lastTimestamp'
│       └─► ExternalSecret sync: kubectl get externalsecret -n consent
│
├─► Consent data incorrect / not found?
│   └─► Query Database (see Database Investigation)
│       ├─► Check consent by citizen_id
│       ├─► Verify audit logs
│       └─► Validate data consistency
│
├─► Consent code bug?
│   └─► See [consent-code-bugs.md](references/consent-code-bugs.md)
│       ├─► Code not found
│       ├─► Duplicate code
│       ├─► Case sensitivity
│       └─► Version mismatch
│
└─► Unknown issue?
    └─► Full diagnostics (K8s + DB)
```

## Core Capabilities

### 1. Kubernetes Diagnostics

Check service health in EKS cluster:

```bash
# Set context
kubectl config use-context arn:aws:eks:ap-southeast-7:290768402609:cluster/aux-eks-goqmac0w

# Check all resources in namespace
kubectl get all -n consent

# Check pod status
kubectl get pods -n consent -o wide

# View pod logs
kubectl logs -n consent deployment/consent --tail=100

# Check for errors
kubectl logs -n consent deployment/consent | grep -i error

# Describe pod for detailed status
kubectl describe pod -n consent <pod-name>

# Check rollout status
kubectl rollout status deployment/consent -n consent

# View events
kubectl get events -n consent --sort-by='.lastTimestamp'

# Check ExternalSecret sync status
kubectl get externalsecret -n consent
kubectl describe externalsecret consent-secrets -n consent

# Port forward for local debugging
kubectl port-forward -n consent svc/consent 8080:8080
```

### 2. Database Investigation

Connect to PostgreSQL RDS and query consent data:

```bash
# Load environment variables
export $(cat .env.sit | xargs)

# Connect to database
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME

# Or use SSL mode
psql "host=$DB_HOST port=$DB_PORT user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$DB_SSL_MODE"
```

See [common-queries.md](references/common-queries.md) for pre-built queries.

### 3. Consent Code Bug Investigation

For consent code-related issues, see [consent-code-bugs.md](references/consent-code-bugs.md).

## Quick Start

### Check Service Health

```bash
# Run diagnostics script
./scripts/k8s-diagnostics.sh
```

### Query Consent Data

```bash
# Connect and query
./scripts/db-connect.sh
./scripts/query-consent.sh <citizen_id>
```

## Resources

### scripts/
Executable scripts for common troubleshooting tasks:

- `k8s-diagnostics.sh` - Check pod health, logs, and events
- `db-connect.sh` - Connect to PostgreSQL RDS
- `query-consent.sh` - Query consent data by citizen_id

### references/
Reference documentation for detailed troubleshooting:

- `database-schema.md` - All 13 tables schema and relationships
- `k8s-deployment-reference.md` - Deployment, service, and secret configurations
- `common-queries.md` - Pre-built SQL queries for troubleshooting
- `troubleshooting-guide.md` - Step-by-step issue resolution workflows
- `consent-code-bugs.md` - Consent code troubleshooting scenarios

### Environment Files

Credentials are stored in environment files:
- `.env` - Local development
- `.env.sit` - SIT environment (sit_consent database)
- `.env.uat` - UAT environment

Load with: `export $(cat .env.sit | xargs)`

# Troubleshooting Guide

Step-by-step troubleshooting workflows for common consent service issues.

## Table of Contents

1. [Service Unavailable](#service-unavailable)
2. [Pod CrashLoopBackOff](#pod-crashloopbackoff)
3. [Database Connection Errors](#database-connection-errors)
4. [Consent Not Found](#consent-not-found)
5. [Missing Audit Logs](#missing-audit-logs)
6. [ExternalSecret Sync Failed](#externalsecret-sync-failed)
7. [High Latency / Slow Queries](#high-latency--slow-queries)

---

## Service Unavailable

**Symptoms**: API returns 503/504 errors, health check fails, requests timeout

### Step 1: Check Pod Status

```bash
kubectl config use-context arn:aws:eks:ap-southeast-7:290768402609:cluster/aux-eks-goqmac0w
kubectl get pods -n consent
```

**Expected**: Pods in `Running` state with `1/1` ready
**Problem**: Pods in `Pending`, `CrashLoopBackOff`, or `Error` state

### Step 2: Check Service Endpoints

```bash
kubectl get svc -n consent
kubectl get endpoints -n consent
```

**Issue**: Endpoints show no pods → Check readiness probe

### Step 3: Check Pod Logs

```bash
# Get logs from all pods
kubectl logs -n consent -l app=consent --tail=100

# Search for errors
kubectl logs -n consent -l app=consent | grep -i error

# Get logs from previous container (if restarted)
kubectl logs -n consent <pod-name> --previous
```

### Step 4: Describe Resources

```bash
# Check pod events and conditions
kubectl describe pod -n consent <pod-name>

# Check service details
kubectl describe svc consent -n consent
```

### Step 5: Check Events

```bash
# Get recent events
kubectl get events -n consent --sort-by='.lastTimestamp' | tail -20
```

### Common Fixes

| Issue | Fix |
|-------|-----|
| Pod `Pending` | Check resource limits, node capacity |
| Pod `CrashLoopBackOff` | Check logs for startup errors |
| No endpoints | Check readiness probe, label selectors |
| High restart count | Check memory limits, application logs |

---

## Pod CrashLoopBackOff

**Symptoms**: Pod repeatedly restarts, status shows `CrashLoopBackOff`

### Step 1: Get Previous Logs

```bash
kubectl logs -n consent <pod-name> --previous
```

### Step 2: Check Events

```bash
kubectl describe pod -n consent <pod-name>
```

Look for:
- `Back-off restarting failed container`
- `OOMKilled` (Out of Memory)
- `Error: ImagePullBackOff`

### Step 3: Common Causes

#### Cause A: Database Connection Failed

**Log pattern**:
```
failed to connect to database: connection refused
dial tcp: lookup aux-rds-goqmac0w...: no such host
```

**Diagnosis**:
```bash
# Check secret exists
kubectl get secret consent-secrets -n consent

# Verify DB credentials in pod
kubectl exec -n consent <pod-name> -- env | grep DB_
```

**Fix**:
- Check ExternalSecret sync: `kubectl get externalsecret -n consent`
- Verify RDS security group allows pod IP range
- Check VPC peering if cross-VPC

#### Cause B: Application Error on Startup

**Log pattern**:
```
panic: runtime error: invalid memory address
FATAL: failed to initialize service
```

**Diagnosis**:
```bash
# Check recent deployment
kubectl rollout history deployment/consent -n consent

# Check configmap values
kubectl get configmap consent-config -n consent -o yaml
```

**Fix**:
- Rollback to previous version: `kubectl rollout undo deployment/consent -n consent`
- Fix configuration issue and redeploy

#### Cause C: Out of Memory

**Log pattern**:
```
OOMKilled
Exit Code: 137
```

**Diagnosis**:
```bash
# Check memory usage
kubectl top pod -n consent

# Check resource limits
kubectl describe pod -n consent <pod-name> | grep -A5 "Limits"
```

**Fix**:
- Increase memory limits in deployment
- Check for memory leaks in application

---

## Database Connection Errors

**Symptoms**: API returns 500 errors with database-related messages

### Step 1: Check Application Logs

```bash
kubectl logs -n consent -l app=consent | grep -i "database\|connection\|timeout"
```

### Step 2: Verify Database Connectivity

```bash
# Load environment
export $(cat .env.sit | xargs)

# Test connection from local machine
psql "host=$DB_HOST port=$DB_PORT user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$DB_SSL_MODE" -c "SELECT 1;"
```

### Step 3: Check Connection Pool Status

From application logs:
```
pool exhausted
connection refused
too many connections
```

### Step 4: Database Diagnostics

```sql
-- Check active connections
SELECT count(*), state 
FROM pg_stat_activity 
WHERE datname = 'sit_consent'
GROUP BY state;

-- Check connection limit
SHOW max_connections;

-- Check current connections by user
SELECT usename, count(*) 
FROM pg_stat_activity 
GROUP BY usename;
```

### Common Fixes

| Issue | Fix |
|-------|-----|
| Connection timeout | Check security groups, VPC routing |
| SSL error | Verify DB_SSL_MODE=require in config |
| Pool exhausted | Increase DB_MAX_OPEN_CONNS or add connection pooling (PgBouncer) |
| Too many connections | Close idle connections, restart pods |

---

## Consent Not Found

**Symptoms**: API returns "consent not found" for valid citizen_id

### Step 1: Verify Data Subject Exists

```sql
-- Find data subject by citizen_id
SELECT id, citizen_id, created_at
FROM data_subjects
WHERE citizen_id = '1234567890123';
```

**If not found**: Data subject was never created

### Step 2: Check Consent Records

```sql
-- Get all consents for citizen
SELECT 
    c.id,
    p.code as purpose_code,
    c.purpose_version,
    dc.code as data_consumer_code,
    c.status,
    c.scope_value
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
JOIN data_consumers dc ON c.dc_id = dc.id
WHERE c.scope_value = '1234567890123';
```

### Step 3: Check Scope Value

```sql
-- Verify citizen_id format in consents
SELECT DISTINCT scope_value 
FROM consents 
WHERE scope_value LIKE '%1234567890123%';
```

**Issue**: Scope value might have extra characters or different format

### Step 4: Check Purpose Status

```sql
-- Verify purpose is active
SELECT code, is_active, created_at
FROM purposes
WHERE code = 'MKT';
```

**Issue**: Purpose might be inactive or not yet created

### Step 5: Check Consent Status

```sql
-- Check if consent exists but is not active
SELECT 
    c.id,
    c.status,
    c.granted_date,
    c.revoked_date
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
WHERE c.scope_value = '1234567890123'
AND p.code = 'MKT'
AND c.status != 'active';
```

**Issue**: Consent exists but is revoked/declined/expired

---

## Missing Audit Logs

**Symptoms**: Consent action performed but no audit log entry

### Step 1: Check Consent Exists

```sql
-- Verify consent was created
SELECT * FROM consents WHERE id = 'consent-uuid-here';
```

### Step 2: Check Audit Log

```sql
-- Get audit logs for consent
SELECT * 
FROM consent_audit_logs 
WHERE consent_id = 'consent-uuid-here'
ORDER BY performed_at DESC;
```

### Step 3: Check by Transaction ID

```sql
-- Find audit by transaction ID from API response
SELECT *
FROM consent_audit_logs
WHERE transaction_id = 'txn-123';
```

### Step 4: Check Application Logs

```bash
# Search for audit-related errors
kubectl logs -n consent -l app=consent | grep -i "audit\|transaction"
```

### Common Causes

| Cause | Check |
|-------|-------|
| Audit service disabled | Check `AUDIT_ENABLED` env var |
| Database transaction rollback | Check for errors in same transaction |
| Async processing delay | Wait a few seconds and retry query |
| Wrong transaction_id | Verify ID from API response |

---

## ExternalSecret Sync Failed

**Symptoms**: Pod fails to start, missing environment variables

### Step 1: Check ExternalSecret Status

```bash
kubectl get externalsecret -n consent
kubectl describe externalsecret consent-secrets -n consent
```

**Expected**: `SecretSynced` status with `True`
**Problem**: Status shows errors or `False`

### Step 2: Check Secret Exists

```bash
kubectl get secret consent-secrets -n consent
```

**If missing**: ExternalSecret not syncing

### Step 3: Check External Secrets Operator

```bash
# Check operator is running
kubectl get pods -n external-secrets

# Check operator logs
kubectl logs -n external-secrets deployment/external-secrets-operator
```

### Step 4: Verify AWS Access

```bash
# Check if secret exists in AWS
aws secretsmanager get-secret-value \
  --secret-id sit/aux-systems/consent \
  --region ap-southeast-7
```

### Step 5: Common Fixes

| Issue | Fix |
|-------|-----|
| ExternalSecret not found | Verify `ClusterSecretStore` name: `aws-secrets-store` |
| AWS auth failed | Check IRSA or AWS credentials |
| Secret not found in AWS | Create secret in AWS Secrets Manager |
| Sync delay | Wait for `refreshInterval` (1h) or restart operator |

### Force Sync

```bash
# Restart External Secrets Operator
kubectl rollout restart deployment/external-secrets-operator -n external-secrets

# Or annotate to trigger sync
kubectl annotate externalsecret consent-secrets -n consent force-sync=$(date +%s)
```

---

## High Latency / Slow Queries

**Symptoms**: API response times > 500ms, database query timeout

### Step 1: Check Pod Resources

```bash
# Check CPU/Memory usage
kubectl top pod -n consent

# Check resource limits
kubectl describe pod -n consent <pod-name> | grep -A10 "Resources"
```

### Step 2: Check Database Performance

```sql
-- Check slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Step 3: Check Connection Pool

From application logs:
```
connection pool exhausted
acquiring connection timeout
```

### Step 4: Common Fixes

| Issue | Fix |
|-------|-----|
| Missing indexes | Add indexes on frequently queried columns |
| Large table scans | Add composite indexes, optimize queries |
| Connection pool small | Increase `DB_MAX_OPEN_CONNS` |
| High CPU usage | Scale deployment replicas |
| Lock contention | Optimize transaction scope, reduce lock time |

### Optimization Queries

```sql
-- Add index on consent lookups (if missing)
CREATE INDEX IF NOT EXISTS idx_consents_scope_status 
ON consents(scope_value, status);

-- Add index on audit log date
CREATE INDEX IF NOT EXISTS idx_audit_performed_at 
ON consent_audit_logs(performed_at DESC);

-- Analyze table statistics
ANALYZE consents;
ANALYZE consent_audit_logs;
```

---

## Quick Reference Commands

```bash
# Full service health check
kubectl config use-context arn:aws:eks:ap-southeast-7:290768402609:cluster/aux-eks-goqmac0w
kubectl get all -n consent
kubectl get events -n consent --sort-by='.lastTimestamp' | tail -20

# Check logs
kubectl logs -n consent -l app=consent --tail=200

# Database connection test
export $(cat .env.sit | xargs)
psql "host=$DB_HOST port=$DB_PORT user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$DB_SSL_MODE" -c "SELECT 1;"

# Run diagnostics script
./scripts/k8s-diagnostics.sh
```

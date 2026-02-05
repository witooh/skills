# Common Queries

Pre-built SQL queries for troubleshooting the consent service database.

## Connection

```bash
# Connect to database
psql -h aux-rds-goqmac0w.cluster-cpig66gqgrwx.ap-southeast-7.rds.amazonaws.com \
     -p 5432 \
     -U consent_service \
     -d sit_consent
```

Or load from environment:
```bash
export $(cat .env.sit | xargs)
psql "host=$DB_HOST port=$DB_PORT user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$DB_SSL_MODE"
```

---

## Consent Queries

### Get Consent by Citizen ID

```sql
-- Get all consents for a citizen
SELECT 
    c.id,
    c.scope_value as citizen_id,
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
WHERE c.scope_value = '1234567890123'
ORDER BY c.created_at DESC;
```

### Get Active Consents

```sql
-- Get only active consents for a citizen
SELECT 
    c.id,
    p.code as purpose_code,
    c.purpose_version,
    dc.code as data_consumer_code,
    c.granted_date,
    c.collection_point_id
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
JOIN data_consumers dc ON c.dc_id = dc.id
WHERE c.scope_value = '1234567890123'
AND c.status = 'active';
```

### Get Consent Details

```sql
-- Full consent details with purpose info
SELECT 
    c.id as consent_id,
    c.scope_value as citizen_id,
    p.code as purpose_code,
    p.name_en as purpose_name,
    c.purpose_version,
    pv.consent_content_en,
    dc.code as data_consumer_code,
    dc.name_en as data_consumer_name,
    c.status,
    c.granted_date,
    c.revoked_date,
    c.collection_point_id,
    c.created_at,
    c.updated_at
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
JOIN purpose_versions pv ON c.purpose_id = pv.purpose_id 
    AND c.purpose_version = pv.version
JOIN data_consumers dc ON c.dc_id = dc.id
WHERE c.id = 'uuid-here';
```

### Count Consents by Status

```sql
-- Count consents grouped by status
SELECT 
    status,
    COUNT(*) as count
FROM consents
GROUP BY status
ORDER BY count DESC;
```

### Recent Consents

```sql
-- Get consents created in last 24 hours
SELECT 
    c.id,
    c.scope_value,
    p.code as purpose_code,
    c.status,
    c.created_at
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
WHERE c.created_at > NOW() - INTERVAL '24 hours'
ORDER BY c.created_at DESC
LIMIT 50;
```

---

## Audit Log Queries

### Get Audit Trail for Consent

```sql
-- Get complete audit history for a consent
SELECT 
    cal.transaction_id,
    cal.action,
    cal.performed_by,
    cal.performed_at,
    cal.metadata->>'ip_address' as ip_address,
    cal.snapshot
FROM consent_audit_logs cal
WHERE cal.consent_id = 'uuid-here'
ORDER BY cal.performed_at DESC;
```

### Get Audit by Transaction ID

```sql
-- Get all actions in a specific transaction
SELECT 
    cal.consent_id,
    cal.action,
    cal.performed_at,
    c.scope_value,
    p.code as purpose_code
FROM consent_audit_logs cal
JOIN consents c ON cal.consent_id = c.id
JOIN purposes p ON c.purpose_id = p.id
WHERE cal.transaction_id = 'txn-123'
ORDER BY cal.performed_at;
```

### Recent Audit Activity

```sql
-- Get audit logs from last hour
SELECT 
    cal.transaction_id,
    cal.consent_id,
    cal.action,
    cal.performed_at,
    c.scope_value,
    p.code as purpose_code
FROM consent_audit_logs cal
JOIN consents c ON cal.consent_id = c.id
JOIN purposes p ON c.purpose_id = p.id
WHERE cal.performed_at > NOW() - INTERVAL '1 hour'
ORDER BY cal.performed_at DESC
LIMIT 100;
```

### Audit Statistics

```sql
-- Count audit actions by type
SELECT 
    action,
    COUNT(*) as count
FROM consent_audit_logs
WHERE performed_at > NOW() - INTERVAL '24 hours'
GROUP BY action
ORDER BY count DESC;
```

---

## Purpose Queries

### Get Purpose by Code

```sql
-- Get purpose details by code
SELECT 
    p.id,
    p.code,
    p.name_en,
    p.name_th,
    p.description,
    p.scope,
    p.period_days,
    p.is_active,
    p.created_at
FROM purposes p
WHERE p.code = 'MKT';
```

### Get Purpose with Latest Version

```sql
-- Get purpose with its latest version
SELECT 
    p.id,
    p.code,
    p.name_en,
    pv.version as latest_version,
    pv.consent_content_en,
    pv.effective_date
FROM purposes p
LEFT JOIN LATERAL (
    SELECT * FROM purpose_versions 
    WHERE purpose_id = p.id 
    ORDER BY version DESC 
    LIMIT 1
) pv ON true
WHERE p.code = 'MKT';
```

### Get Purpose Data Sets

```sql
-- Get data sets required for a purpose version
SELECT 
    ds.set_code,
    ds.set_name,
    ds.is_sensitive,
    pds.is_required
FROM purpose_data_sets pds
JOIN data_sets ds ON pds.data_set_id = ds.id
WHERE pds.purpose_id = 'purpose-uuid-here'
AND pds.purpose_version = 1.0
ORDER BY ds.set_code;
```

### List All Active Purposes

```sql
-- Get all active purposes with their versions
SELECT 
    p.code,
    p.name_en,
    p.scope,
    p.period_days,
    pv.version,
    pv.effective_date
FROM purposes p
LEFT JOIN LATERAL (
    SELECT * FROM purpose_versions 
    WHERE purpose_id = p.id 
    ORDER BY version DESC 
    LIMIT 1
) pv ON true
WHERE p.is_active = true
ORDER BY p.code;
```

---

## Data Consumer Queries

### Get Data Consumer by Code

```sql
-- Get data consumer details
SELECT 
    id,
    code,
    name_en,
    name_th,
    consumer_type,
    created_at
FROM data_consumers
WHERE code = 'TCMB';
```

### List All Data Consumers

```sql
-- Get all data consumers
SELECT 
    code,
    name_en,
    consumer_type,
    created_at
FROM data_consumers
ORDER BY code;
```

---

## Data Subject Queries

### Get Data Subject by Citizen ID

```sql
-- Find data subject
SELECT 
    id,
    citizen_id,
    created_at
FROM data_subjects
WHERE citizen_id = '1234567890123';
```

### Get Data Subject with Consents

```sql
-- Get data subject and all their consents
SELECT 
    ds.id as data_subject_id,
    ds.citizen_id,
    c.id as consent_id,
    p.code as purpose_code,
    c.status,
    c.created_at as consent_created
FROM data_subjects ds
LEFT JOIN consents c ON ds.id = c.data_subject_id
LEFT JOIN purposes p ON c.purpose_id = p.id
WHERE ds.citizen_id = '1234567890123'
ORDER BY c.created_at DESC;
```

---

## Consistency Check Queries

### Orphaned Consents

```sql
-- Find consents with missing data subjects
SELECT c.* 
FROM consents c
LEFT JOIN data_subjects ds ON c.data_subject_id = ds.id
WHERE ds.id IS NULL;
```

### Orphaned Audit Logs

```sql
-- Find audit logs with missing consents
SELECT cal.* 
FROM consent_audit_logs cal
LEFT JOIN consents c ON cal.consent_id = c.id
WHERE c.id IS NULL;
```

### Invalid Purpose References

```sql
-- Find consents referencing non-existent purposes
SELECT c.* 
FROM consents c
LEFT JOIN purposes p ON c.purpose_id = p.id
WHERE p.id IS NULL;
```

### Consents with Inactive Purposes

```sql
-- Find active consents for inactive purposes
SELECT 
    c.id,
    c.scope_value,
    c.status,
    p.code,
    p.is_active as purpose_active
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
WHERE p.is_active = false 
AND c.status = 'active';
```

### Missing Audit Logs

```sql
-- Find consents without audit logs
SELECT c.*
FROM consents c
LEFT JOIN consent_audit_logs cal ON c.id = cal.consent_id
WHERE cal.id IS NULL;
```

### Duplicate Consents

```sql
-- Find duplicate consents (same citizen, purpose, version, consumer, scope)
SELECT 
    scope_value,
    purpose_id,
    purpose_version,
    dc_id,
    COUNT(*) as duplicate_count
FROM consents
GROUP BY scope_value, purpose_id, purpose_version, dc_id
HAVING COUNT(*) > 1;
```

---

## Terms & Conditions Queries

### Get Active T&C

```sql
-- Get currently active T&C version
SELECT 
    id,
    version,
    title_en,
    effective_date,
    is_active
FROM terms_conditions
WHERE is_active = true
AND effective_date <= CURRENT_DATE
ORDER BY version DESC
LIMIT 1;
```

### Get T&C Acceptances

```sql
-- Get T&C acceptances for a citizen
SELECT 
    tca.id,
    tca.data_subject_id,
    tc.version as tc_version,
    tca.accepted_at,
    tca.ip_address,
    tca.device_id
FROM terms_conditions_acceptances tca
JOIN terms_conditions tc ON tca.terms_conditions_id = tc.id
WHERE tca.data_subject_id = 'data-subject-uuid-here'
ORDER BY tca.accepted_at DESC;
```

---

## Statistics Queries

### Database Overview

```sql
-- Get row counts for all tables
SELECT 
    'consents' as table_name, COUNT(*) as row_count FROM consents
UNION ALL
SELECT 'consent_audit_logs', COUNT(*) FROM consent_audit_logs
UNION ALL
SELECT 'data_subjects', COUNT(*) FROM data_subjects
UNION ALL
SELECT 'purposes', COUNT(*) FROM purposes
UNION ALL
SELECT 'purpose_versions', COUNT(*) FROM purpose_versions
UNION ALL
SELECT 'data_consumers', COUNT(*) FROM data_consumers
UNION ALL
SELECT 'data_sets', COUNT(*) FROM data_sets
UNION ALL
SELECT 'terms_conditions', COUNT(*) FROM terms_conditions
UNION ALL
SELECT 'terms_conditions_acceptances', COUNT(*) FROM terms_conditions_acceptances
ORDER BY table_name;
```

### Consent Activity Summary

```sql
-- Summary of consent activity
SELECT 
    DATE(created_at) as date,
    status,
    COUNT(*) as count
FROM consents
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at), status
ORDER BY date DESC, status;
```

### Top Data Consumers

```sql
-- Most active data consumers
SELECT 
    dc.code,
    dc.name_en,
    COUNT(c.id) as consent_count
FROM data_consumers dc
LEFT JOIN consents c ON dc.id = c.dc_id
GROUP BY dc.id, dc.code, dc.name_en
ORDER BY consent_count DESC;
```

### Purpose Usage

```sql
-- Consent count by purpose
SELECT 
    p.code,
    p.name_en,
    COUNT(c.id) as consent_count,
    COUNT(CASE WHEN c.status = 'active' THEN 1 END) as active_count
FROM purposes p
LEFT JOIN consents c ON p.id = c.purpose_id
GROUP BY p.id, p.code, p.name_en
ORDER BY consent_count DESC;
```

# Database Schema Reference

Complete reference for the consent service PostgreSQL database schema.

## Overview

- **Database**: `sit_consent` (SIT), `uat_consent` (UAT)
- **Host**: `aux-rds-goqmac0w.cluster-cpig66gqgrwx.ap-southeast-7.rds.amazonaws.com`
- **Port**: 5432
- **Tables**: 13 tables organized by domain

## Table of Contents

1. [Core Consent Tables](#core-consent-tables)
2. [Configuration Tables](#configuration-tables)
3. [Terms & Conditions Tables](#terms--conditions-tables)
4. [Entity Relationships](#entity-relationships)

---

## Core Consent Tables

### 1. consents

Main consent records table.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique consent identifier |
| data_subject_id | UUID (FK) | Reference to data_subjects |
| purpose_id | UUID (FK) | Reference to purposes |
| purpose_version | DECIMAL | Purpose version number |
| dc_id | UUID (FK) | Reference to data_consumers |
| scope_value | VARCHAR | Citizen ID or Account Number |
| status | consent_status (ENUM) | active, revoked, declined, expired |
| granted_date | TIMESTAMP | When consent was granted |
| revoked_date | TIMESTAMP | When consent was revoked |
| collection_point_id | UUID (FK) | Where consent was collected |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

**Indexes**:
- Unique: (data_subject_id, purpose_id, purpose_version, dc_id, scope_value)
- Index on status for filtering
- Index on data_subject_id for lookups

**Key Queries**:
```sql
-- Get consent by citizen_id
SELECT * FROM consents 
WHERE scope_value = '1234567890123' 
AND status = 'active';

-- Get consent history for a purpose
SELECT * FROM consents 
WHERE purpose_id = 'uuid-here' 
ORDER BY created_at DESC;
```

### 2. consent_audit_logs

Complete audit trail for all consent actions.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique audit log identifier |
| transaction_id | VARCHAR | API request transaction ID |
| consent_id | UUID (FK) | Reference to consents |
| action | VARCHAR | Action type: accept, revoke, decline, expire, update |
| snapshot | JSONB | Full consent state at time of action |
| metadata | JSONB | Additional request metadata (IP, user agent, etc.) |
| performed_by | VARCHAR | User/system that performed action |
| performed_at | TIMESTAMP | When action was performed |
| created_at | TIMESTAMP | Record creation time |

**Indexes**:
- Index on consent_id for audit lookups
- Index on transaction_id for request tracing
- Index on performed_at for time-based queries

**Key Queries**:
```sql
-- Get audit trail for a consent
SELECT * FROM consent_audit_logs 
WHERE consent_id = 'uuid-here' 
ORDER BY performed_at DESC;

-- Get all actions in a transaction
SELECT * FROM consent_audit_logs 
WHERE transaction_id = 'txn-123';
```

### 3. data_subjects

Individuals (citizens) who provide consent.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| citizen_id | VARCHAR(13) | Thai national ID (unique) |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

**Key Queries**:
```sql
-- Find data subject by citizen_id
SELECT * FROM data_subjects 
WHERE citizen_id = '1234567890123';
```

---

## Configuration Tables

### 4. purposes

Consent purposes (Marketing, Analytics, etc.).

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique purpose identifier |
| code | VARCHAR (UNIQUE) | Purpose code (e.g., MKT, ANA, LOAN) |
| name_th | VARCHAR | Thai name |
| name_en | VARCHAR | English name |
| description | TEXT | Purpose description |
| scope | purpose_scope (ENUM) | customer (citizen_id) or accountNo |
| period_days | INTEGER | Consent validity period |
| is_active | BOOLEAN | Whether purpose is active |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

**Key Queries**:
```sql
-- Get active purpose by code
SELECT * FROM purposes 
WHERE code = 'MKT' 
AND is_active = true;

-- Get all active purposes
SELECT * FROM purposes 
WHERE is_active = true 
ORDER BY code;
```

### 5. purpose_versions

Versioned purpose details.

| Column | Type | Description |
|--------|------|-------------|
| purpose_id | UUID (FK, PK) | Reference to purposes |
| version | DECIMAL (PK) | Version number |
| consent_content_th | TEXT | Thai consent content text |
| consent_content_en | TEXT | English consent content text |
| effective_date | DATE | When version becomes effective |
| created_at | TIMESTAMP | Record creation time |

**Key Queries**:
```sql
-- Get latest version of a purpose
SELECT * FROM purpose_versions 
WHERE purpose_id = 'uuid-here' 
ORDER BY version DESC 
LIMIT 1;

-- Get all versions of a purpose
SELECT * FROM purpose_versions 
WHERE purpose_id = 'uuid-here' 
ORDER BY version DESC;
```

### 6. data_sets

Data categories (Name, Email, Phone, etc.).

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| set_code | VARCHAR (UNIQUE) | Code (e.g., NAME, EMAIL, PHONE) |
| set_name | VARCHAR | Human-readable name |
| is_sensitive | BOOLEAN | Whether data is sensitive/PII |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### 7. purpose_data_sets

Links purposes to required data sets.

| Column | Type | Description |
|--------|------|-------------|
| purpose_id | UUID (FK, PK) | Reference to purposes |
| purpose_version | DECIMAL (PK) | Purpose version |
| data_set_id | UUID (FK, PK) | Reference to data_sets |
| is_required | BOOLEAN | Whether data set is required |
| created_at | TIMESTAMP | Record creation time |

**Key Queries**:
```sql
-- Get data sets required for a purpose version
SELECT ds.*, pds.is_required 
FROM purpose_data_sets pds
JOIN data_sets ds ON pds.data_set_id = ds.id
WHERE pds.purpose_id = 'uuid-here' 
AND pds.purpose_version = 1.0;
```

### 8. data_consumers

Organizations consuming data.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| code | VARCHAR (UNIQUE) | Consumer code (e.g., TCMB, PARTNER_A) |
| name_th | VARCHAR | Thai name |
| name_en | VARCHAR | English name |
| consumer_type | consumer_type (ENUM) | INTERNAL, PARTNER, THIRD_PARTY |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

**Key Queries**:
```sql
-- Get data consumer by code
SELECT * FROM data_consumers 
WHERE code = 'TCMB';
```

---

## Collection Hierarchy

### 9. segments

Business segments (Customer, HR, etc.).

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| code | VARCHAR (UNIQUE) | Segment code |
| name_th | VARCHAR | Thai name |
| name_en | VARCHAR | English name |
| description | TEXT | Description |
| is_active | BOOLEAN | Whether segment is active |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### 10. channels

Communication channels under segments.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| segment_id | UUID (FK) | Reference to segments |
| code | VARCHAR | Channel code |
| name_th | VARCHAR | Thai name |
| name_en | VARCHAR | English name |
| description | TEXT | Description |
| is_active | BOOLEAN | Whether channel is active |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### 11. collection_points

Where consent is collected.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| channel_id | UUID (FK) | Reference to channels |
| code | VARCHAR | Collection point code |
| name_th | VARCHAR | Thai name |
| name_en | VARCHAR | English name |
| description | TEXT | Description |
| location | VARCHAR | Physical/digital location |
| is_active | BOOLEAN | Whether collection point is active |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

---

## Terms & Conditions Tables

### 12. terms_conditions

T&C versions.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| version | INTEGER (UNIQUE) | Version number |
| title_th | VARCHAR | Thai title |
| title_en | VARCHAR | English title |
| content_th | TEXT | Thai content |
| content_en | TEXT | English content |
| effective_date | DATE | When T&C becomes effective |
| is_active | BOOLEAN | Whether T&C is active |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Last update time |

### 13. terms_conditions_acceptances

User T&C acceptances.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID (PK) | Unique identifier |
| data_subject_id | UUID (FK) | Reference to data_subjects (nullable for anonymous) |
| terms_conditions_id | UUID (FK) | Reference to terms_conditions |
| accepted_at | TIMESTAMP | When T&C was accepted |
| device_id | VARCHAR | Device identifier for anonymous acceptance |
| ip_address | VARCHAR | IP address of acceptance |
| user_agent | VARCHAR | User agent string |
| created_at | TIMESTAMP | Record creation time |

---

## Entity Relationships

```
segments (1)
    └── channels (N)
        └── collection_points (N)
            └── consents (N)

data_subjects (1)
    └── consents (N)
    └── terms_conditions_acceptances (N)

purposes (1)
    └── purpose_versions (N)
    └── purpose_data_sets (N)
        └── data_sets (1)

data_consumers (1)
    └── consents (N)

consents (1)
    └── consent_audit_logs (N)

terms_conditions (1)
    └── terms_conditions_acceptances (N)
```

## Key Foreign Key Constraints

| Child Table | Parent Table | Column |
|-------------|--------------|--------|
| consents | data_subjects | data_subject_id |
| consents | purposes | purpose_id |
| consents | data_consumers | dc_id |
| consents | collection_points | collection_point_id |
| channels | segments | segment_id |
| collection_points | channels | channel_id |
| purpose_versions | purposes | purpose_id |
| purpose_data_sets | purposes | purpose_id |
| purpose_data_sets | data_sets | data_set_id |
| consent_audit_logs | consents | consent_id |
| terms_conditions_acceptances | data_subjects | data_subject_id |
| terms_conditions_acceptances | terms_conditions | terms_conditions_id |

## Troubleshooting Data Consistency

Check for orphaned records:

```sql
-- Orphaned consents (missing data_subject)
SELECT c.* FROM consents c
LEFT JOIN data_subjects ds ON c.data_subject_id = ds.id
WHERE ds.id IS NULL;

-- Orphaned consents (missing purpose)
SELECT c.* FROM consents c
LEFT JOIN purposes p ON c.purpose_id = p.id
WHERE p.id IS NULL;

-- Orphaned audit logs (missing consent)
SELECT cal.* FROM consent_audit_logs cal
LEFT JOIN consents c ON cal.consent_id = c.id
WHERE c.id IS NULL;

-- Consents with inactive purposes
SELECT c.*, p.code, p.is_active
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
WHERE p.is_active = false AND c.status = 'active';
```

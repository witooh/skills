# Consent Code Bugs

Troubleshooting guide for consent code-related bugs and issues.

## Table of Contents

1. [Consent Code Not Found](#1-consent-code-not-found)
2. [Duplicate Consent Code](#2-duplicate-consent-code)
3. [Consent Code Case Sensitivity](#3-consent-code-case-sensitivity)
4. [Invalid Consent Code Format](#4-invalid-consent-code-format)
5. [Consent Code Returns Wrong Purpose](#5-consent-code-returns-wrong-purpose)
6. [Consent Code Version Mismatch](#6-consent-code-version-mismatch)
7. [Consent Code with Expired/Inactive Purpose](#7-consent-code-with-expiredinactive-purpose)

---

## 1. Consent Code Not Found

### Symptoms

- API returns error: `purpose code 'XYZ' not found`
- Consent creation fails with 404
- Application logs show: `ErrPurposeNotFound`

### Diagnosis

#### Step 1: Verify Code Exists in Database

```sql
-- Check if purpose code exists
SELECT 
    id,
    code,
    name_en,
    is_active,
    created_at
FROM purposes
WHERE code = 'XYZ';

-- Check with case variations
SELECT 
    id,
    code,
    name_en,
    is_active
FROM purposes
WHERE LOWER(code) = LOWER('XYZ');
```

#### Step 2: Check Code Format

```sql
-- Check for whitespace or special characters
SELECT 
    code,
    LENGTH(code) as code_length,
    code ~ '^[A-Z0-9_]+$' as valid_format
FROM purposes
WHERE code LIKE '%XYZ%';
```

#### Step 3: Check Environment

```bash
# Verify you're querying the correct database
psql "host=$DB_HOST port=$DB_PORT user=$DB_USER password=$DB_PASSWORD dbname=$DB_NAME sslmode=$DB_SSL_MODE" -c "SELECT current_database();"
```

### Common Causes

| Cause | Explanation |
|-------|-------------|
| Typo in code | User entered 'MKT1' instead of 'MKT' |
| Wrong environment | Code exists in SIT but not UAT |
| Case sensitivity | PostgreSQL collation differences |
| Trailing spaces | Code has invisible whitespace |
| Code not deployed | Migration not applied |

### Resolution

```sql
-- If code doesn't exist, check similar codes
SELECT 
    code,
    name_en,
    similarity(code, 'XYZ') as similarity_score
FROM purposes
ORDER BY similarity(code, 'XYZ') DESC
LIMIT 5;

-- Create missing purpose (if needed)
-- Note: Should be done through application/migration, not manual insert
```

---

## 2. Duplicate Consent Code

### Symptoms

- API returns error: `unique constraint violation on purpose code`
- Cannot create new purpose with existing code
- Database error: `duplicate key value violates unique constraint "purposes_code_key"`

### Diagnosis

#### Step 1: Find Existing Code

```sql
-- Check for existing code
SELECT 
    id,
    code,
    name_en,
    is_active,
    created_at
FROM purposes
WHERE code = 'NEW_CODE';

-- Check for similar codes
SELECT 
    id,
    code,
    name_en
FROM purposes
WHERE code LIKE '%NEW%'
ORDER BY code;
```

#### Step 2: Check for Soft-Deleted Records

```sql
-- Check if there's a deleted_at column (if soft delete is implemented)
SELECT 
    id,
    code,
    name_en,
    is_active
FROM purposes
WHERE code = 'NEW_CODE';
-- Note: Current schema doesn't have soft delete, but check is_active
```

### Common Causes

| Cause | Explanation |
|-------|-------------|
| Code already exists | Purpose was created previously |
| Reactivated purpose | Purpose is inactive but code exists |
| Migration conflict | Two migrations trying to insert same code |
| Concurrent requests | Race condition in creation |

### Resolution

```sql
-- If purpose is inactive, reactivate it
UPDATE purposes 
SET is_active = true, 
    updated_at = NOW()
WHERE code = 'NEW_CODE'
AND is_active = false;

-- Or use a different code
-- Generate unique code with timestamp
-- Example: NEW_CODE_20240115
```

---

## 3. Consent Code Case Sensitivity

### Symptoms

- Code works in local environment but fails in SIT/UAT
- `MKT` works but `mkt` fails (or vice versa)
- Inconsistent behavior between environments

### Diagnosis

#### Step 1: Check PostgreSQL Collation

```sql
-- Check database collation
SELECT datname, datcollate, datctype 
FROM pg_database 
WHERE datname = current_database();

-- Check table collation
SELECT tablename, table_collation 
FROM pg_tables 
WHERE tablename = 'purposes';
```

#### Step 2: Test Case Sensitivity

```sql
-- Test exact match
SELECT * FROM purposes WHERE code = 'mkt';

-- Test case-insensitive match
SELECT * FROM purposes WHERE LOWER(code) = LOWER('mkt');

-- Test with ILIKE
SELECT * FROM purposes WHERE code ILIKE 'mkt';
```

### Root Cause

PostgreSQL string comparison depends on collation settings:
- `en_US.utf8` (typical): Case-sensitive by default
- `C` locale: Case-sensitive, binary comparison
- Application logic should be consistent

### Resolution

#### Option A: Fix Application Code (Recommended)

Ensure application normalizes codes before comparison:
```go
// Convert to uppercase before query
code = strings.ToUpper(code)

// Or use case-insensitive query
// WHERE LOWER(code) = LOWER($1)
```

#### Option B: Database-Level Fix

```sql
-- Create case-insensitive index
CREATE INDEX idx_purposes_code_lower 
ON purposes(LOWER(code));

-- Query with case-insensitive match
SELECT * FROM purposes 
WHERE LOWER(code) = LOWER('mkt');
```

#### Option C: Standardize Codes

```sql
-- Convert all existing codes to uppercase
UPDATE purposes 
SET code = UPPER(code),
    updated_at = NOW()
WHERE code != UPPER(code);
```

---

## 4. Invalid Consent Code Format

### Symptoms

- Validation error: `invalid purpose code format`
- Code rejected despite appearing valid
- Pattern validation failures

### Diagnosis

#### Step 1: Check Validation Rules

```sql
-- Check existing code patterns
SELECT 
    code,
    LENGTH(code) as length,
    code ~ '^[A-Z0-9_]+$' as alphanumeric_underscore_only,
    code ~ '[A-Z]' as has_uppercase,
    code ~ '[0-9]' as has_number
FROM purposes
ORDER BY code;
```

#### Step 2: Test Specific Code

```sql
-- Test code against validation rules
SELECT 
    'NEW-CODE' as test_code,
    LENGTH('NEW-CODE') as length,
    'NEW-CODE' ~ '^[A-Z0-9_]+$' as valid_format,
    'NEW-CODE' ~ '-' as has_hyphen;
```

### Common Validation Rules

| Rule | Pattern | Example |
|------|---------|---------|
| Alphanumeric + underscore | `^[A-Z0-9_]+$` | `MKT_2024` |
| Length limit | `LENGTH(code) <= 20` | `MKT` |
| No special chars | `!~ '[-/ ]'` | Not `MKT-2024` |
| Uppercase only | `code = UPPER(code)` | `MKT` not `mkt` |

### Common Causes

| Invalid Code | Reason |
|--------------|--------|
| `MKT-2024` | Contains hyphen |
| `MKT 2024` | Contains space |
| `mkt` | Lowercase letters |
| `MKT@2024` | Special characters |
| `Marketing_Purpose_2024_January` | Too long (>20 chars) |

### Resolution

```sql
-- Fix invalid codes
UPDATE purposes 
SET code = REGEXP_REPLACE(UPPER(code), '[^A-Z0-9_]', '_', 'g'),
    updated_at = NOW()
WHERE code !~ '^[A-Z0-9_]+$';

-- Or manually fix specific codes
UPDATE purposes 
SET code = 'MKT_2024',
    updated_at = NOW()
WHERE code = 'MKT-2024';
```

---

## 5. Consent Code Returns Wrong Purpose

### Symptoms

- Consent created for wrong purpose
- `MKT` code returns analytics purpose instead of marketing
- Similar codes causing confusion

### Diagnosis

#### Step 1: Find Similar Codes

```sql
-- Find codes similar to target
SELECT 
    code,
    name_en,
    similarity(code, 'MKT') as similarity_score
FROM purposes
ORDER BY similarity(code, 'MKT') DESC
LIMIT 10;

-- Check for prefix matches
SELECT 
    code,
    name_en
FROM purposes
WHERE code LIKE 'MKT%';
```

#### Step 2: Check Code Prefixes

```sql
-- Find codes that might be confused
SELECT 
    code,
    name_en,
    is_active
FROM purposes
WHERE code IN ('MKT', 'MK', 'MKTG', 'MKT2', 'MKT_B', 'MKT_A');
```

### Common Causes

| Issue | Example |
|-------|---------|
| Prefix confusion | `MKT` vs `MK` vs `MKTG` |
| Suffix variations | `MKT_2024` vs `MKT_2023` |
| Inactive code | Old `MKT` inactive, new `MKT_V2` active |
| Partial matching | Query matches `MK` and returns first result |

### Resolution

#### Step 1: Ensure Exact Matching

```sql
-- Use exact match, not partial
SELECT * FROM purposes WHERE code = 'MKT';
-- Not: WHERE code LIKE 'MKT%'
```

#### Step 2: Rename Confusing Codes

```sql
-- Rename ambiguous codes
UPDATE purposes 
SET code = 'MKTG_ANALYTICS',
    name_en = 'Marketing Analytics',
    updated_at = NOW()
WHERE code = 'MKT'
AND name_en LIKE '%analytics%';

-- Or deactivate confusing codes
UPDATE purposes 
SET is_active = false,
    updated_at = NOW()
WHERE code = 'MKT_OLD';
```

---

## 6. Consent Code Version Mismatch

### Symptoms

- Consent created with wrong purpose version
- API request for version 1.0 but consent stored as version 2.0
- Version validation errors

### Diagnosis

#### Step 1: Check Purpose Versions

```sql
-- Get all versions of a purpose
SELECT 
    purpose_id,
    version,
    effective_date,
    consent_content_en
FROM purpose_versions
WHERE purpose_id = (
    SELECT id FROM purposes WHERE code = 'MKT'
)
ORDER BY version DESC;
```

#### Step 2: Check Requested vs Stored Version

```sql
-- Find consents with mismatched versions
SELECT 
    c.id,
    c.scope_value,
    p.code,
    c.purpose_version as stored_version,
    pv.version as actual_latest_version,
    pv.effective_date
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
LEFT JOIN purpose_versions pv ON c.purpose_id = pv.purpose_id 
    AND c.purpose_version = pv.version
WHERE p.code = 'MKT'
AND c.created_at > NOW() - INTERVAL '24 hours';
```

#### Step 3: Check Version Validity

```sql
-- Find consents with invalid versions
SELECT 
    c.id,
    c.purpose_id,
    c.purpose_version,
    p.code
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
WHERE NOT EXISTS (
    SELECT 1 FROM purpose_versions pv
    WHERE pv.purpose_id = c.purpose_id
    AND pv.version = c.purpose_version
);
```

### Common Causes

| Cause | Explanation |
|-------|-------------|
| Default version | API doesn't specify version, uses default |
| Version not provided | Request missing purpose_version field |
| Invalid version | Requested version doesn't exist |
| Future version | Version effective_date is in the future |

### Resolution

```sql
-- Find latest active version
SELECT 
    pv.purpose_id,
    pv.version,
    pv.effective_date
FROM purpose_versions pv
JOIN purposes p ON pv.purpose_id = p.id
WHERE p.code = 'MKT'
AND pv.effective_date <= CURRENT_DATE
ORDER BY pv.version DESC
LIMIT 1;

-- Update invalid version references (if necessary)
-- Note: This should be done carefully as it affects data integrity
```

---

## 7. Consent Code with Expired/Inactive Purpose

### Symptoms

- Cannot create consent for valid-looking code
- Error: `purpose is not active`
- Consent fails with purpose validation error

### Diagnosis

#### Step 1: Check Purpose Status

```sql
-- Check purpose active status
SELECT 
    id,
    code,
    name_en,
    is_active,
    created_at,
    updated_at
FROM purposes
WHERE code = 'MKT';
```

#### Step 2: Check Purpose Version Effective Date

```sql
-- Check version effective dates
SELECT 
    pv.purpose_id,
    p.code,
    pv.version,
    pv.effective_date,
    pv.effective_date > CURRENT_DATE as is_future
FROM purpose_versions pv
JOIN purposes p ON pv.purpose_id = p.id
WHERE p.code = 'MKT'
ORDER BY pv.version DESC;
```

#### Step 3: Find Active Consents for Inactive Purposes

```sql
-- Data consistency check
SELECT 
    c.id,
    c.scope_value,
    c.status,
    p.code,
    p.is_active as purpose_active,
    c.created_at
FROM consents c
JOIN purposes p ON c.purpose_id = p.id
WHERE p.is_active = false
AND c.status = 'active'
ORDER BY c.created_at DESC
LIMIT 20;
```

### Common Causes

| Cause | Explanation |
|-------|-------------|
| Purpose deactivated | Purpose was set to inactive |
| Version not effective | Purpose version has future effective_date |
| No active versions | All versions expired or not yet effective |
| Soft-delete | Purpose marked deleted but not purged |

### Resolution

#### Option A: Reactivate Purpose

```sql
-- Reactivate inactive purpose
UPDATE purposes 
SET is_active = true,
    updated_at = NOW()
WHERE code = 'MKT'
AND is_active = false;
```

#### Option B: Update Version Effective Date

```sql
-- Make version effective immediately
UPDATE purpose_versions 
SET effective_date = CURRENT_DATE
WHERE purpose_id = (SELECT id FROM purposes WHERE code = 'MKT')
AND version = 2.0
AND effective_date > CURRENT_DATE;
```

#### Option C: Handle Inactive Consents

```sql
-- Mark consents for inactive purposes as expired
UPDATE consents c
SET status = 'expired',
    updated_at = NOW()
FROM purposes p
WHERE c.purpose_id = p.id
AND p.is_active = false
AND c.status = 'active';
```

---

## Quick Reference: Common Consent Codes

### Standard Purpose Codes

| Code | Description | Scope |
|------|-------------|-------|
| MKT | Marketing | customer |
| ANA | Analytics | customer |
| LOAN | Loan Processing | accountNo |
| SRV | Service Notifications | customer |

### Data Consumer Codes

| Code | Type | Description |
|------|------|-------------|
| TCMB | INTERNAL | TCR Bank |
| PARTNER_A | PARTNER | Partner A |
| VENDOR_X | THIRD_PARTY | Vendor X |

### Debugging Queries

```sql
-- Find all purpose codes
SELECT code, name_en, is_active 
FROM purposes 
ORDER BY code;

-- Find all data consumer codes
SELECT code, name_en, consumer_type 
FROM data_consumers 
ORDER BY code;

-- Check for duplicate or similar codes
SELECT 
    code,
    COUNT(*) OVER (PARTITION BY LOWER(code)) as similar_count
FROM purposes
ORDER BY LOWER(code), code;
```

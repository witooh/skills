**Module:** Savings Account
**Version:** 1.0.0
**Created Date:** 2026-03-17

---

## Test Suite 1: Product Configuration

---

#### TC-001: Configuring the primary denomination of the product

**GIVEN** a bank offers a savings product
**WHEN** configuring the product
**THEN** the bank can specify the primary denomination in which the account will transact

**Endpoint:** `POST /v1/products`
**Request Body:**
```json
{
  "name": "Savings Account",
  "denomination": "THB"
}
```
**Expected Response:**
```json
HTTP 201
{
  "id": "PROD-001",
  "name": "Savings Account",
  "denomination": "THB",
  "status": "ACTIVE"
}
```

**Test Steps:**

1. Log in as Bank Admin
2. Create a new savings product via `POST /v1/products`
3. Set primary denomination = THB
4. Verify the response status and body

**Expected Result:** Product is saved with denomination = THB
**Test Data:** `denomination: "THB"`
**Precondition:** None

---

#### TC-002: Account opening with configured primary denomination

**GIVEN** a bank offers a savings product
**AND** the primary denomination of the product is configured as THB
**WHEN** an account is opened with denomination = THB
**THEN** the account should be opened successfully in Vault

**Endpoint:** `POST /v1/accounts`
**Request Body:**
```json
{
  "product_id": "PROD-001",
  "denomination": "THB",
  "customer_id": "CUST-001"
}
```
**Expected Response:**
```json
HTTP 200
{
  "account_id": "ACC-001",
  "status": "OPEN",
  "denomination": "THB"
}
```

**Test Steps:**

1. Call the account opening API via `POST /v1/accounts` with denomination = THB
2. Verify the response status = 200
3. Verify the account record: status = OPEN, denomination = THB

**Expected Result:** HTTP 200, account status = OPEN, denomination = THB
**Test Data:** `account_id: "ACC-001"`, `denomination: "THB"`
**Precondition:** TC-001 must pass

---

## Test Suite 2: Transaction Validation

---

#### TC-003: Accepting a credit or debit in a primary denomination

**GIVEN** there is an account where the primary denomination is THB
**WHEN** a credit or debit is attempted in THB
**THEN** the transaction is accepted

**Endpoint:** `POST /v1/accounts/{account_id}/transactions`
**Request Body:**
```json
{
  "type": "CREDIT",
  "amount": 1000,
  "denomination": "THB"
}
```
**Expected Response:**
```json
HTTP 200
{
  "transaction_id": "TXN-001",
  "status": "ACCEPTED",
  "amount": 1000,
  "denomination": "THB"
}
```

**Test Steps:**

1. Call `POST /v1/accounts/ACC-001/transactions` with denomination = THB, amount = 1000
2. Verify the response status = 200 and transaction status = ACCEPTED

**Expected Result:** HTTP 200, transaction status = ACCEPTED
**Test Data:** `amount: 1000`, `denomination: "THB"`
**Precondition:** TC-002 must pass

---

#### TC-004: Rejecting a credit or debit in a non-primary denomination

**GIVEN** there is an account where the primary denomination is THB
**WHEN** a credit or debit is attempted in USD
**THEN** the transaction is rejected

**Endpoint:** `POST /v1/accounts/{account_id}/transactions`
**Request Body:**
```json
{
  "type": "CREDIT",
  "amount": 100,
  "denomination": "USD"
}
```
**Expected Response:**
```json
HTTP 400
{
  "error": "Invalid denomination",
  "message": "Account ACC-001 only accepts THB"
}
```

**Test Steps:**

1. Call `POST /v1/accounts/ACC-001/transactions` with denomination = USD, amount = 100
2. Verify the response status = 400 and error = "Invalid denomination"

**Expected Result:** HTTP 400, error = "Invalid denomination"
**Test Data:** `amount: 100`, `denomination: "USD"`
**Precondition:** TC-002 must pass

---

## Test Case Summary

| ID     | Suite                  | Description                                    | Precondition |
| ------ | ---------------------- | ---------------------------------------------- | ------------ |
| TC-001 | Product Configuration  | Configure primary denomination                 | None         |
| TC-002 | Product Configuration  | Open account with configured denomination      | TC-001       |
| TC-003 | Transaction Validation | Accept transaction in primary denomination     | TC-002       |
| TC-004 | Transaction Validation | Reject transaction in non-primary denomination | TC-002       |

**Total Test Cases:** 4

---

## Notes

- TC-003 and TC-004 require TC-002 to pass first
- Test data uses the staging environment only

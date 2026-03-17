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

**Test Steps:**

1. Log in as Bank Admin
2. Create a new savings product
3. Set primary denomination = THB
4. Save the configuration

**Expected Result:** Product is saved with denomination = THB
**Test Data:** `denomination: "THB"`
**Precondition:** None

---

#### TC-002: Account opening with configured primary denomination

**GIVEN** a bank offers a savings product
**AND** the primary denomination of the product is configured as THB
**WHEN** an account is opened with denomination = THB
**THEN** the account should be opened successfully in Vault

**Test Steps:**

1. Call the account opening API with denomination = THB
2. Verify the response status
3. Verify the account record in Vault

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

**Test Steps:**

1. Call the deposit API with denomination = THB, amount = 1000
2. Verify the transaction status in the response

**Expected Result:** HTTP 200, transaction status = ACCEPTED
**Test Data:** `amount: 1000`, `denomination: "THB"`
**Precondition:** TC-002 must pass

---

#### TC-004: Rejecting a credit or debit in a non-primary denomination

**GIVEN** there is an account where the primary denomination is THB
**WHEN** a credit or debit is attempted in USD
**THEN** the transaction is rejected

**Test Steps:**

1. Call the deposit API with denomination = USD, amount = 100
2. Verify the error response

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

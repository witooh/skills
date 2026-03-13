# API Documentation Template

Use this template whenever generating or updating API documentation (e.g., `docs/api-doc.md`). Follow the structure exactly so all docs look consistent across services.

---

## Document Header

```markdown
# <Service Name> API Documentation

**Version:** <X.Y>
**Base URL:** `/api/v<N>`

## Overview

<One paragraph describing what this service does and its primary purpose.>

---
```

---

## Table of Contents

List every section and sub-section as anchor links. Group related endpoints under a numbered top-level section.

```markdown
## Table of Contents

1. [Authentication](#1-authentication)
2. [<Resource> APIs](#2-resource-apis)
   - [2.1 <Endpoint Name>](#21-endpoint-name)
   - [2.2 <Endpoint Name>](#22-endpoint-name)
3. [Error Responses](#3-error-responses)
```

---

## Endpoint Template

Each endpoint follows this exact structure. Do not skip sections — use `_(not applicable)_` if a section genuinely has no content.

````markdown
### <N.M> <Endpoint Name>

<One sentence describing what this endpoint does.>

- **Method:** `GET` | `POST` | `PUT` | `PATCH` | `DELETE`
- **Path:** `/api/v1/<resource>/<path-param>`
- **Auth:** `Bearer token` | `API Key` | `None`

#### Path Parameters (if any)

| Field Name | Description | Type   | Mandatory | Example    | Remark |
| ---------- | ----------- | ------ | --------- | ---------- | ------ |
| `id`       | Resource ID | String | M         | `"uuid-1"` |        |

#### Query Parameters (if any)

| Field Name | Description           | Type   | Mandatory | Example | Remark        |
| ---------- | --------------------- | ------ | --------- | ------- | ------------- |
| `page`     | Page number (1-based) | Number | O         | `1`     | Default: `1`  |
| `limit`    | Items per page        | Number | O         | `20`    | Default: `20` |

#### Request Body (if any)

| Field Name   | Description          | Type    | Mandatory | Example           | Remark                |
| ------------ | -------------------- | ------- | --------- | ----------------- | --------------------- |
| `field_name` | What this field does | String  | M         | `"example_value"` |                       |
| `items`      | List of item objects | Array   | M         |                   | See Item Object below |
| `flag`       | Boolean toggle       | Boolean | O         | `true`            |                       |

**Item Object:**

| Field Name | Description     | Type   | Mandatory | Example   | Remark |
| ---------- | --------------- | ------ | --------- | --------- | ------ |
| `code`     | Item code       | String | M         | `"CODE1"` |        |
| `value`    | Optional detail | String | O         | `"abc"`   |        |

#### Request Example

```json
{
  "field_name": "example_value",
  "items": [{ "code": "CODE1" }, { "code": "CODE2", "value": "abc" }],
  "flag": true
}
```

#### Response (<HTTP Status> <Status Text>)

| Field Name   | Description            | Type   | Mandatory | Example                  | Remark               |
| ------------ | ---------------------- | ------ | --------- | ------------------------ | -------------------- |
| `id`         | UUID of created record | String | M         | `"uuid-v4"`              |                      |
| `status`     | Current status         | String | M         | `"active"`               | "active", "inactive" |
| `created_at` | ISO 8601 timestamp     | String | M         | `"2024-01-01T10:00:00Z"` |                      |
| `updated_at` | ISO 8601 timestamp     | String | M         | `"2024-01-01T10:00:00Z"` |                      |

#### Response Example

```json
{
  "id": "uuid-v4",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

#### Error Responses

| Status | Error Message         | Description                    |
| ------ | --------------------- | ------------------------------ |
| 400    | invalid request       | Request body validation failed |
| 404    | record not found      | Resource does not exist        |
| 422    | <specific message>    | Business rule violation        |
| 500    | internal server error | Server-side failure            |
````

---

## Field Table Conventions

| Convention  | Meaning                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------- |
| Mandatory   | Use `M` for required fields, `O` for optional                                                            |
| Type values | `String`, `Number`, `Boolean`, `Array`, `Object`                                                         |
| Timestamps  | Always ISO 8601 format: `"2024-01-01T10:00:00Z"`                                                         |
| UUIDs       | Use `"uuid-v4"` or `"uuid-<noun>"` as example values (e.g., `"uuid-consent-1"`)                          |
| Nested obj  | Use `Array` or `Object` type + `See <Name> Object below` in Remark column, then add a separate sub-table |
| Enum values | List allowed values in Remark (e.g., `"active"`, `"inactive"`, `"revoked"`)                              |
| Null fields | Show `null` in Example when the field can be null                                                        |

---

## Common Error Responses Section

Include this at the end of the document to avoid repeating across every endpoint:

```markdown
## <N>. Error Responses

All endpoints may return the following common errors:

| Status | Error Message         | Description                         |
| ------ | --------------------- | ----------------------------------- |
| 400    | invalid request       | Request body or query param invalid |
| 401    | unauthorized          | Missing or invalid authentication   |
| 403    | forbidden             | Insufficient permissions            |
| 404    | not found             | Resource does not exist             |
| 500    | internal server error | Unexpected server-side failure      |
```

---

## Checklist Before Finalizing

- [ ] Every endpoint has Method, Path, and at least one example
- [ ] All field tables use `M`/`O` for Mandatory column
- [ ] Nested objects each have their own sub-table
- [ ] Error Responses table covers all possible HTTP status codes
- [ ] Table of Contents links match actual heading anchors
- [ ] Version number in document header is up to date

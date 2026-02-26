# Certificate Type API Implementation

This document explains the implementation of template linking in CertificateType CRUD operations.

## Overview

The implementation adds the ability to link certificate types to certificate templates, enabling the frontend to fetch template details (name and layout configuration) when retrieving certificate types.

## Changes Made

### 1. Schema (`app/schemas/certificate_type.py`)

Created new Pydantic schemas for CertificateType:

- **CertificateTypeBase**: Base schema with common fields
  - `name`: Certificate type name (required)
  - `category`: Optional category
  - `target_role`: Either "STUDENT" or "STAFF" (default: "STUDENT")
  - `template_id`: Optional UUID link to CertificateTemplate

- **CertificateTypeCreate**: Schema for POST requests
- **CertificateTypeUpdate**: Schema for PATCH requests (all fields optional)
- **TemplateInfo**: Nested schema for template details in responses
- **CertificateTypeRead**: Response schema with nested template info

### 2. Service (`app/services/certificate_type_service.py`)

Created CertificateTypeService with CRUD operations:

- **create(payload)**: Creates new certificate type
  - Validates that `template_id` exists if provided
  - Raises 400 error if template not found

- **get_all()**: Retrieves all certificate types
  - Uses `joinedload(CertificateType.template)` for eager loading
  - Returns template details in each response

- **get_by_id(id)**: Retrieves single certificate type by ID
  - Includes template details in response

- **update(id, payload)**: Updates certificate type
  - Validates template_id if being updated
  - Supports partial updates

### 3. Endpoint (`app/api/v1/endpoints/certificate_type.py`)

Created REST endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/certificate-types/` | Create new certificate type |
| GET | `/api/v1/certificate-types/` | Get all certificate types |
| GET | `/api/v1/certificate-types/{id}` | Get certificate type by ID |
| PATCH | `/api/v1/certificate-types/{id}` | Update certificate type |

### 4. Router Registration (`app/main.py`)

Registered the certificate_type router with prefix `/api/v1/certificate-types`.

## Example Responses

### GET /api/v1/certificate-types/

```json
{
  "name": "Advanced Course Completion Certificate",
  "category": "Completion",
  "target_role": "STUDENT",
  "template_id": "ebf1cc0e-e606-4806-9497-004ac3c68a19",
  "id": 3,
  "template": {
    "id": "ebf1cc0e-e606-4806-9497-004ac3c68a19",
    "name": "student_curriculum",
    "layout_config": []
  }
}
```

### POST /api/v1/certificate-types/

Request:
```json
{
  "name": "New Certificate Type",
  "target_role": "STUDENT",
  "template_id": "ebf1cc0e-e606-4806-9497-004ac3c68a19"
}
```

Response:
```json
{
  "name": "New Certificate Type",
  "category": null,
  "target_role": "STUDENT",
  "template_id": "ebf1cc0e-e606-4806-9497-004ac3c68a19",
  "id": 12,
  "template": {
    "id": "ebf1cc0e-e606-4806-9497-004ac3c68a19",
    "name": "student_curriculum",
    "layout_config": []
  }
}
```

### Error Handling

- **400 Bad Request**: If template_id is provided but doesn't exist
- **404 Not Found**: If certificate type with given ID doesn't exist

## Previous Bug Fix

Before implementing this feature, a bug was fixed in the template endpoint:

### Issue
The `GET /api/v1/templates/` endpoint was returning a 500 Internal Server Error due to a validation error.

### Root Cause
The `layout_config` column in the database stored data as either:
1. `None` (NULL)
2. A `dict` (e.g., `{'watermark': 'kshrd_logo', ...}`) instead of a list

The Pydantic schema expected `List[TemplateElement]` but received incompatible types.

### Fix
Added a `field_validator` in `TemplateRead` schema (`app/schemas/certificate_template.py`) to convert:
- `None` → empty list `[]`
- `dict` → empty list `[]`

This ensures backward compatibility with existing data.

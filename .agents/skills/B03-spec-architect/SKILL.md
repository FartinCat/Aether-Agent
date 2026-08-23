---
name: B03-spec-architect
description: Formal technical specification & contract engine. Translates chosen architectural strategies into unambiguous, enforceable specifications (data contracts, API schemas, state machines, error codes).
category: plan
aliases: [spec-architect, spec-generator, contract-architect, specification]
---

# Skill: B03-spec-architect (Formal Technical Specification & Contract Engine)

**Objective**: Transform high-level requirements and selected architectural plans into a formal, binding technical specification (`SPEC.md`). Establish rock-solid data contracts, API schemas, lifecycle state transitions, and error codes *before* any implementation begins. Eliminate assumptions, hallucinations, and breaking changes.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines formal specification engineering protocols with an automated specification health validator:

```
B03-spec-architect/
├── SKILL.md                  # Specification protocol & 5-pillar contract standard
├── scripts/
│   └── validate_spec.py     # Static specification auditor & portability validator
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `B03-spec-architect/` directly into any `.agents/skills/` directory to enable rigorous specification engineering.

---

## 2. Core Operating Principles

1. **Contract-First Mandate**:
   - Never begin coding or task breakdown without an agreed-upon technical contract.
   - Ambiguities in field names, status codes, or state transitions must be locked down in `SPEC.md`.

2. **The 5 Pillars of Formal Specification**:
   - Every specification must satisfy all five pillars:
     1. **Acceptance Criteria**: Verifiable Given/When/Then scenarios.
     2. **Data Models & Schemas**: Exact types, nullability, primary/foreign keys, and validation rules.
     3. **API & Interface Signatures**: Request payloads, response structures, headers, and HTTP status codes.
     4. **State Machine & Lifecycle Transitions**: Explicit valid states and transition triggers (rejecting illegal transitions).
     5. **Error Taxonomy & Recovery**: Deterministic error codes, failure boundaries, and user remediation guidance.

3. **Ingest Before Specifying (Ensemble vs. Standalone)**:
   - **Ensemble Mode**: Ingest `<!-- CONTEXT_ANCHOR:PLAN_VARIATIONS -->` from `B02-planner` and `<!-- CONTEXT_ANCHOR:DECISION_RECORD -->` from `B01-grill-me`.
   - **Standalone Fallback**: If running without upstream skills, inspect repository models and type definitions directly using standard tools.

4. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean, relative paths (`src/...`).

---

## 3. The 5 Specification Pillars Standard

```
┌─────────────────────────────────────────────────────────────┐
│ Pillar 1: Acceptance Criteria                               │
│ (Given / When / Then, Edge-case acceptance tests)           │
├─────────────────────────────────────────────────────────────┤
│ Pillar 2: Data Models & Schema Contracts                    │
│ (TypeScript interfaces, Prisma models, Pydantic schemas)    │
├─────────────────────────────────────────────────────────────┤
│ Pillar 3: API & Interface Signatures                        │
│ (HTTP methods, endpoints, payloads, HTTP status codes)      │
├─────────────────────────────────────────────────────────────┤
│ Pillar 4: State Machine & Lifecycle Transitions             │
│ (Valid states: IDLE -> PROCESSING -> COMPLETED / FAILED)    │
├─────────────────────────────────────────────────────────────┤
│ Pillar 5: Error Taxonomy & Recovery                         │
│ (ERR_RATE_LIMIT, ERR_INVALID_PAYLOAD, retry/timeout bounds) │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Specification Validator

`B03-spec-architect` includes a self-contained static auditor: `scripts/validate_spec.py`.

### How to Run:
```bash
python .agents/skills/B03-spec-architect/scripts/validate_spec.py path/to/SPEC.md
```

### What it Enforces:
- Verifies that all 5 specification pillars are covered.
- Checks for Given/When/Then acceptance criteria.
- Validates typed schemas and error taxonomies.
- Enforces zero hardcoded machine paths (portability check).
- Returns health score (0–100%) and required fixes.

---

## 5. Output Format Standard

Generate specifications using this structured template:

```markdown
<!-- CONTEXT_ANCHOR:SYSTEM_SPEC -->
# Technical Specification: [Feature / System Name]

**Version**: 1.0.0  
**Status**: APPROVED  
**Related Strategy**: [Reference to selected variation from B02-planner]

---

### 1. Feature Overview & Acceptance Criteria
- **Given** [a authenticated user with active subscription],
- **When** [they trigger a batch export of invoice data],
- **Then** [the system enqueues an export job, returns 202 Accepted with a JobId, and streams updates via SSE].

### 2. Data Models & Schemas
```typescript
export interface ExportJob {
  id: string; // UUID v4
  userId: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  createdAt: string; // ISO 8601
  downloadUrl?: string; // Signed S3 URL, nullable
}
```

### 3. API & Interface Contracts
- **POST** `/api/v1/exports`
  - **Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
  - **Request Body**:
    ```json
    { "format": "CSV", "dateRange": { "from": "2026-01-01", "to": "2026-06-30" } }
    ```
  - **Success Response**: `202 Accepted`
  - **Payload**: `{ "jobId": "exp_8921a", "status": "PENDING" }`

### 4. State Machine & Transitions
- Valid transitions:
  - `PENDING` ➔ `PROCESSING` (Worker acquires lock)
  - `PROCESSING` ➔ `COMPLETED` (Upload finished, URL generated)
  - `PROCESSING` ➔ `FAILED` (Worker timeout or DB error)
- *Illegal Transition*: Cannot transition directly from `PENDING` to `COMPLETED`.

### 5. Error Taxonomy & Recovery
| Error Code | HTTP Status | Trigger Condition | Remediation / Fallback |
| :--- | :---: | :--- | :--- |
| `ERR_EXPORT_RATE_LIMIT` | 429 | >3 active jobs in queue | Alert user with cooldown timer (60s) |
| `ERR_DATE_RANGE_INVALID`| 400 | `from` date is after `to` date | Reject payload with validation message |
| `ERR_STORAGE_TIMEOUT`   | 504 | S3 upload exceeds 30s | Retry up to 3x with exponential backoff |
<!-- END_ANCHOR:SYSTEM_SPEC -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/spec`, `/specify`, or `/contract`.
- **In Workflow**: Runs immediately after **`B02-planner`**. Solidifies the chosen variation into a binding contract. Passes directly to **`B04-plan-synthesizer`** and **`B05-task-executor`**.

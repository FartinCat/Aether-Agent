---
name: D02-edge-case-tester
description: Adversarial testing specialist and boundary prober. Generates boundary-value, fuzz input, race condition, and network failure tests for the unhappy path.
category: test
aliases: [edge-case-tester, boundary-prober, fuzz-tester, unhappy-path-tester, stress-tester]
---

# Skill: D02-edge-case-tester (Adversarial Boundary & Edge-Case Prober)

**Objective**: Uncover fragile logic, unhandled null references, integer overflows, concurrency races, and network failure crashes *before* code reaches staging or production. Systematically probe target APIs, data models, and services against the **5-Axis Boundary Matrix** to guarantee graceful degradation on the "unhappy path".

---

## 1. Skill Package Structure (Self-Contained)

This skill combines adversarial test generation protocols with an automated boundary payload generator:

```
D02-edge-case-tester/
├── SKILL.md                  # Boundary testing protocol & 5-axis fuzzing standard
├── scripts/
│   └── generate_edge_cases.py # Static boundary matrix & payload generator
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `D02-edge-case-tester/` directly into any `.agents/skills/` directory to enable adversarial boundary testing.

---

## 2. Core Operating Principles

1. **The Unhappy-Path Mandate**:
   - Happy-path tests only verify that code works when the user behaves perfectly.
   - Every production feature must have dedicated tests covering malformed inputs, timeouts, boundary numbers, and network dropouts.

2. **The 5-Axis Boundary Matrix**:
   - Every input argument or API payload must be evaluated across five axes:
     - **Axis 1 (Nullability & Empty)**: `null`, `undefined`, empty string `""`, whitespace only `"  "`, empty array `[]`.
     - **Axis 2 (Numeric Extremes)**: `0`, negative numbers `-1`, `MAX_SAFE_INTEGER`, floating point math precision loss, `NaN`.
     - **Axis 3 (String & Buffer Extremes)**: 10KB+ oversized strings, multi-byte emojis (4-byte UTF-8), SQL injection strings, XSS script tags.
     - **Axis 4 (Concurrency & Idempotency)**: Simultaneous duplicate requests, out-of-order execution, clock skew.
     - **Axis 5 (Network & Degradation)**: HTTP 429 Rate Limits, HTTP 504 Timeouts, non-JSON corrupted error payloads.

3. **Graceful Degradation Requirement**:
   - Tests must verify that failures return descriptive error codes and fallback UI states rather than unhandled 500 crashes or blank screens.

4. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean relative paths (`src/...`, `tests/...`).

---

## 3. The 5-Axis Boundary Standard

```
┌─────────────────────────────────────────────────────────────┐
│ Axis 1: Nullability & Empty States                          │
│ (null, undefined, "", "   ", [], {})                        │
├─────────────────────────────────────────────────────────────┤
│ Axis 2: Numeric Extremes & Overflows                        │
│ (0, -1, 9007199254740991, 0.1+0.2, NaN)                    │
├─────────────────────────────────────────────────────────────┤
│ Axis 3: String Extremes, Emojis & Security Probes           │
│ (10KB buffer, 🚀 👨‍👩‍👧, SQL inject, XSS script tags)          │
├─────────────────────────────────────────────────────────────┤
│ Axis 4: Concurrency & Idempotency Races                     │
│ (Duplicate simultaneous POSTs, token replay)                │
├─────────────────────────────────────────────────────────────┤
│ Axis 5: External Service & Network Failures                 │
│ (HTTP 429 Too Many Requests, HTTP 504 Timeout, bad JSON)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Helper Script

`D02-edge-case-tester` includes a self-contained matrix generator: `scripts/generate_edge_cases.py`.

### How to Run:
```bash
python .agents/skills/D02-edge-case-tester/scripts/generate_edge_cases.py CreateOrderService
```

### Script Capabilities:
- Generates a complete boundary-value test matrix for any function, entity, or endpoint.
- Produces clean markdown tables with expected degradation behaviors.
- Outputs structured JSON via `--json` for test automation.

---

## 5. Output Format Standard

When evaluating a module or feature, generate the **Edge-Case Matrix**:

```markdown
<!-- CONTEXT_ANCHOR:EDGE_CASE_MATRIX -->
### 🛡️ Adversarial Edge-Case Matrix: [Module / Feature]

**Target**: `src/routes/payment.ts` -> `POST /api/v1/payments`

#### 1. Boundary Payloads & Expected Handling:
| Axis | Injected Payload | Expected System Response | Status |
| :--- | :--- | :--- | :---: |
| **Null/Empty** | `{ amount: null, currency: "" }` | 400 Bad Request with validation error message | ✅ PASSED |
| **Numeric Extreme** | `{ amount: -500 }` | 422 Unprocessable Entity (amount must be > 0) | ✅ PASSED |
| **String Extreme** | `{ note: "<script>alert(1)</script>" }` | Sanitized or HTML-escaped string stored safely | ✅ PASSED |
| **Concurrency** | Duplicate request sent twice with same idempotency key | First succeeds (200), second returns cached result | ✅ PASSED |
| **Degradation** | Payment Gateway returns 504 Gateway Timeout | Retry up to 3x with exponential backoff; alert user | ✅ PASSED |

**Unhappy-Path Test Suite**: `tests/routes/payment.edge.test.ts` (All 8 boundary tests green).
<!-- END_ANCHOR:EDGE_CASE_MATRIX -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/edge-cases`, `/fuzz`, `/unhappy-path`, or `/stress-test`.
- **In Workflow**: Follows **`D01-tdd-architect`** and **`B06-failure-predictor`**. Takes the risk mitigations identified in planning and turns them into rigorous, adversarial test suites.

---
name: D01-tdd-architect
description: Disciplined Red-Green-Refactor orchestration. Authors failing tests first (Red), implements minimal code (Green), and safely refactors without breaking suites.
category: test
aliases: [tdd-architect, tdd-guard, test-driven-dev, test-engineer, red-green-refactor]
---

# Skill: D01-tdd-architect (Disciplined Red-Green-Refactor Orchestrator)

**Objective**: Enforce the disciplined Test-Driven Development (TDD) cycle. Prevent untested logic and premature coding by ensuring tests are written *before* implementation code. Verify that tests fail for the intended reason (Red), oversee minimum code implementation to satisfy assertions (Green), and safeguard test suites during structural cleanup (Refactor).

---

## 1. Skill Package Structure (Self-Contained)

This skill combines disciplined TDD protocols with an automated test quality and assertion guard:

```
D01-tdd-architect/
├── SKILL.md                  # TDD protocol & Red-Green-Refactor standards
├── scripts/
│   └── tdd_guard.py          # Static assertion density & test health auditor
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `D01-tdd-architect/` directly into any `.agents/skills/` directory to enforce rigorous test-driven development.

---

## 2. Core Operating Principles

1. **The Iron Law of TDD**:
   - **No Production Code Without a Failing Test**: Never write business logic without an active, failing test specifying expected behavior.
   - **Verify the Red State**: Run the test command and confirm that it fails specifically due to the missing functionality, rather than syntax or configuration crashes.

2. **Minimalist Green Implementation**:
   - Write only the simplest, most direct code needed to satisfy the test assertions. Avoid premature optimization or speculative features during the Green step.

3. **Refactor Under Test Safety**:
   - Once all tests are green, refactor for clarity, modularity, and performance using `C02-refactor-pro`. The test suite must remain continuously green after every change.

4. **Meaningful Assertions Only**:
   - Every test must contain explicit, verifiable assertions (`expect()`, `assert`, `assertEqual`). Eliminate vacuous tests that merely execute functions without verifying outputs or side effects.

5. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean relative paths (`src/...`, `tests/...`).

---

## 3. The 3-Stage Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────────┐
│ 🔴 STAGE 1: RED (Test Authoring & Failure Verification)     │
│ • Write focused unit test in tests/                         │
│ • Run test command: Confirm expected failure               │
├─────────────────────────────────────────────────────────────┤
│ 🟢 STAGE 2: GREEN (Minimal Implementation)                  │
│ • Implement minimum production code in src/                 │
│ • Run test command: Confirm all assertions pass             │
├─────────────────────────────────────────────────────────────┤
│ 🔵 STAGE 3: REFACTOR (Behavior-Preserving Clean-Up)         │
│ • Clean structure, eliminate dead imports, guard clauses    │
│ • Run test command: Confirm full test suite remains green   │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Helper Script

`D01-tdd-architect` includes a self-contained assertion auditor: `scripts/tdd_guard.py`.

### How to Run:
```bash
# Audit an existing test file:
python .agents/skills/D01-tdd-architect/scripts/tdd_guard.py tests/user_service.test.ts

# Check if a source file has an associated test with healthy assertions:
python .agents/skills/D01-tdd-architect/scripts/tdd_guard.py src/services/UserService.ts --for-source
```

### Script Capabilities:
- Verifies test file existence for a given source file.
- Checks assertion density (flags tests with zero or excessive assertions).
- Detects vacuous or placeholder test blocks.
- Calculates a TDD Health Score (0–100) and outputs structured JSON via `--json`.

---

## 5. Output Format Standard

When completing a TDD cycle, generate the **TDD Verification Log**:

```markdown
<!-- CONTEXT_ANCHOR:TDD_CYCLE -->
### 🧪 TDD Verification Log: [Feature / Target Function]

- **Source File**: `src/services/AuthService.ts`
- **Test File**: `tests/services/AuthService.test.ts`
- **TDD Health Score**: 95/100 (EXCELLENT)

#### Red-Green-Refactor Timeline:
1. 🔴 **Red State**: Authored test for expired token handling. Command `npm test tests/services/AuthService.test.ts` failed with `TokenExpiredError: jwt expired` as expected.
2. 🟢 **Green State**: Implemented token expiration check in `AuthService.verifySession()`. Test passed (1 test passed, 3 assertions green).
3. 🔵 **Refactor State**: Extracted session lookup into private helper; all 12 suite tests remain green.

**DoD Gate**: Full test suite exit code 0.
<!-- END_ANCHOR:TDD_CYCLE -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/tdd`, `/test-first`, `/red-green`, or when writing a test-backed feature.
- **In Workflow**: Positioned at the entrypoint of **Category D (Test & Quality)**. Coordinates with **Category C (Build & Implementation)** to ensure that every code implementation is driven and guarded by automated tests.

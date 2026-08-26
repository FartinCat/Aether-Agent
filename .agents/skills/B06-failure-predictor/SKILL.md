---
name: B06-failure-predictor
description: Pre-execution failure predictor & risk gate. Audits proposed code changes, roadmaps, and file writes against blast radius, schema constraints, and anti-patterns before execution begins.
category: plan
aliases: [failure-predictor, immune-gate, risk-assessor, predict-failures]
---

# Skill: B06-failure-predictor (Pre-Flight Risk & Failure Predictor)

**Objective**: Operate as the system's pre-flight immune gate. Proactively audit proposed code changes, file modifications, and execution roadmaps *before* a single line of logic is written. Predict breaking changes, data model corruptions, fragile areas, and unhandled failure modes, assigning a deterministic 5-level risk score and verification gate.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines cognitive pre-check heuristics with an automated risk pattern scanner:

```
B06-failure-predictor/
├── SKILL.md                  # Pre-flight audit protocol & risk gating rules
├── scripts/
│   └── scan_risks.py         # Static risk pattern scanner & blast-radius calculator
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `B06-failure-predictor/` directly into any `.agents/skills/` directory to enable instant, automated pre-execution risk auditing.

---

## 2. Core Operating Principles

1. **Audit Before Execution**:
   - Never write code blind. Before modifying an existing file or executing a plan from `B05-task-executor`, evaluate potential failure modes and regressions.

2. **Blast-Radius Consciousness (Ensemble vs. Standalone)**:
   - **Ensemble Mode**: Ingest downstream consumer reports (`<!-- CONTEXT_ANCHOR:DEPENDENCY_MAP -->` from `A04-dependency-mapper`).
   - **Standalone Fallback**: Run built-in `scripts/scan_risks.py` to autonomously search the repository for callers and calculate blast radius without needing external skills installed.

3. **Schema & Model Grounding**:
   - Cross-reference database schemas (`A06-schema-scanner` or local ORM/SQL definitions). Changing field names or adding non-nullable columns without defaults causes runtime database crashes.

4. **Resilience to the "Unhappy Path"**:
   - Ensure external APIs, network calls, and database operations have timeouts, retry bounds, and graceful fallbacks (as defined in requirements or `B01-grill-me`).

5. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean relative paths (`src/...`).

---

## 3. The 4-Step Pre-Flight Audit Protocol

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Blast-Radius & Dependency Cross-Check               │
│ (Identify upstream callers and downstream dependents)       │
├─────────────────────────────────────────────────────────────┤
│ Step 2: Schema & Data Model Verification                    │
│ (Verify field names, null constraints, and active types)    │
├─────────────────────────────────────────────────────────────┤
│ Step 3: Anti-Pattern & Vulnerability Scan                   │
│ (Run scan_risks.py for hardcoded secrets, unbound queries)  │
├─────────────────────────────────────────────────────────────┤
│ Step 4: Deterministic Risk Scoring & Verification Gating    │
│ (Level 1: Safe -> Level 5: Halt / Decompose / Sign-off)     │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Blast-Radius Cross-Check
- Check how many files import the target:
  - **Isolated (0 consumers)**: Low blast risk (+0).
  - **Low (1–2 consumers)**: Standard callers (+10).
  - **Medium (3–5 consumers)**: Shared utility (+25).
  - **High (>5 consumers)**: Core infrastructural module (+40).

### Step 2: Schema & Data Model Verification
- Check if proposed changes touch database models or API contracts:
  - Adding a non-nullable field without a `DEFAULT`? (High crash risk).
  - Renaming an active column without a deprecation migration? (Immediate breaking change).
  - Changing numeric ID types from `Int` to `UUID`? (Cross-table foreign key break).

### Step 3: Anti-Pattern & Vulnerability Scan
- Run `scripts/scan_risks.py` on the target file or inspect proposed logic:
  - **Hardcoded secrets**: API keys, bearer tokens, passwords (+35).
  - **Unbounded queries**: `SELECT *` without `LIMIT` or pagination (+20).
  - **Destructive operations**: `DROP TABLE`, `TRUNCATE`, column deletions (+40).
  - **Unhandled network calls**: HTTP calls without timeouts or `try/catch` (+15).

### Step 4: Verification Gating Hierarchy

| Risk Level | Score Range | Classification | Required Execution Gate |
| :--- | :--- | :--- | :--- |
| **Level 1** | **0 – 25** | **Low Risk** | Safe for immediate autonomous execution. Standard code edit. |
| **Level 2** | **26 – 50** | **Moderate Risk** | Standard implementation. Requires local unit test pass before merge. |
| **Level 3** | **51 – 75** | **Elevated Risk** | Multi-file impact. Integration test and downstream caller review mandatory. |
| **Level 4–5**| **76 – 100**| **Critical Risk** | **HALT EXECUTION**. High regression probability. Must decompose into atomic sub-tasks or require explicit user sign-off. |

---

## 4. Automated Helper Script

`B06-failure-predictor` includes a self-contained risk scanner: `scripts/scan_risks.py`.

### How to Run:
```bash
python .agents/skills/B06-failure-predictor/scripts/scan_risks.py path/to/file.py
```

### Script Output:
- Scans for anti-patterns and calculates downstream blast consumers.
- Outputs deterministic Risk Score, Risk Level, and Gate Recommendation in text or JSON (`--json`).

---

## 5. Output Format Standard

When auditing a plan or proposed change, generate the **Failure Prediction Report**:

```markdown
<!-- CONTEXT_ANCHOR:FAILURE_PREDICTION -->
### 🛡️ Pre-Flight Failure Prediction Report

- **Target / Action**: [Description of planned change]
- **Risk Score**: [Score/100] → **[Level 1 | Level 2 | Level 3 | Level 4-5]**
- **Blast Radius**: [Isolated / Low / Medium / High] — [N downstream consumers]

#### Identified Failure Modes & Anti-Patterns:
1. ⚠️ **[Risk Title]**: [Description of what could go wrong and why]
2. ⚠️ **[Risk Title]**: [Description of what could go wrong and why]

#### Required Verification Gate:
- **Gate Recommendation**: [PROCEED / CAUTION: Unit Tests / GATE: Integration Tests / HALT: Decompose]
- **Mitigation Safeguards**:
  - [Specific preventative constraint, e.g. "Add DEFAULT value to column" or "Wrap API call in exponential retry"]
<!-- END_ANCHOR:FAILURE_PREDICTION -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/predict-failures`, `/risk-check`, or before executing a complex refactor.
- **In Workflow**: Runs directly after **`B05-task-executor`** and before Category C (Implementation). Ensures that coding agents execute tasks with built-in immune safeguards and appropriate verification gates.

---
name: B02-planner
description: Strategic architectural planner. Generates structured feature and architecture plans with explicit variations (Minimalist, Modular, Enterprise) and trade-off comparison matrices before specification.
category: plan
aliases: [planner, strategy-planner, architectural-planner, plan-variants]
---

# Skill: B02-planner (Strategic Architectural Planner with Variations)

**Objective**: Convert requirements and locked decisions from `B01-grill-me` into structured, phased architectural plans. Enforce the **Multi-Variation Mandate**: never produce a single dogmatic plan. Always formulate 2–3 distinct architectural approaches (Minimalist, Modular, and Enterprise) and evaluate them using objective trade-off scorecards before technical specifications are locked.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines strategic architectural planning protocols with an automated variation comparator:

```
B02-planner/
├── SKILL.md                  # Planning protocol & variation comparison standard
├── scripts/
│   └── plan_comparator.py   # Static variation parser & trade-off scorecard generator
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `B02-planner/` directly into any `.agents/skills/` directory to enable multi-variant architectural planning.

---

## 2. Core Operating Principles

1. **The Multi-Variation Mandate**:
   - Never offer a single "take it or leave it" architecture.
   - For every non-trivial feature or refactor, always formulate 2–3 concrete variations:
     - **Variation Alpha (Lean / Minimalist)**: Lowest code delta, zero new dependencies, fast delivery, minimal abstraction.
     - **Variation Beta (Idiomatic / Modular - Standard Recommendation)**: Clean separation of concerns, decoupled domain logic, high testability, and standard framework conventions.
     - **Variation Gamma (Enterprise / Scalable)**: Pluggable interfaces, event-driven or async decoupling, enterprise logging, telemetry, and horizontal scale readiness.

2. **Ingest Before Planning (Ensemble vs. Standalone)**:
   - **Ensemble Mode**: Ingest `<!-- CONTEXT_ANCHOR:DECISION_RECORD -->` from `B01-grill-me`.
   - **Standalone Fallback**: If running without `B01-grill-me` installed, inspect existing project manifests (`package.json`, `pyproject.toml`, `Cargo.toml`) and folder hierarchy directly using standard tools.

3. **Objective Trade-Off Scorecard**:
   - Every proposal must be evaluated across 5 core vectors:
     - **Velocity (1–10)**: How quickly can this be safely implemented and deployed?
     - **Maintainability (1–10)**: How easy is it for future developers or agents to modify without side effects?
     - **Blast Radius / Risk (1–10)**: How many shared modules, schemas, or callers are affected?
     - **Dependency Footprint**: Are new libraries required?
     - **Migration / Rollback Ease**: Can changes be rolled back safely if unexpected failures occur?

4. **Zero Raw File Paths**:
   - Skills must remain 100% portable. Never hardcode absolute system paths or machine drives. Use generic relative paths (`src/...`, `lib/...`) and context protocol anchors.

---

## 3. The 3 Architectural Variations Standard

When drafting architectural plans, define each approach with clear boundaries:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Variation Alpha: Lean / Minimalist                                     │
│ • Focus: Speed, minimal files touched, inline logic, zero new deps     │
│ • Best When: Fast prototypes, internal tools, tight deadlines          │
├────────────────────────────────────────────────────────────────────────┤
│ Variation Beta: Idiomatic / Modular (Recommended)                     │
│ • Focus: Clean service layer, isolated tests, framework best practices │
│ • Best When: Core product features, standard team collaboration       │
├────────────────────────────────────────────────────────────────────────┤
│ Variation Gamma: Enterprise / Future-Proof                             │
│ • Focus: Decoupled adapters, pub/sub events, telemetry, pluggability   │
│ • Best When: High-throughput systems, multi-tenant architectures       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Variation Comparator Script

`B02-planner` includes a self-contained helper script: `scripts/plan_comparator.py`.

### How to Run:
```bash
python .agents/skills/B02-planner/scripts/plan_comparator.py path/to/PLANS.md
```

### Script Capabilities:
- Parses `### Variation A:`, `### Variation B:`, etc.
- Scans files touched and dependency changes across each variation.
- Generates an objective markdown comparison table and automated verdict.
- Supports structured JSON output via `--json`.

---

## 5. Output Format Standard

Generate architectural plans using this structured template:

```markdown
<!-- CONTEXT_ANCHOR:PLAN_VARIATIONS -->
# Architectural Strategic Plan: [Feature / Target System]

**Context**: [Summary of requirements and target objective]

---

### Variation A: Lean / Minimalist
- **Core Strategy**: [Direct implementation with minimal abstraction]
- **Target Files**:
  - `src/components/Target.tsx`
  - `src/utils/helper.ts`
- **Dependencies**: None.
- **Pros & Cons**:
  - ✅ Fast delivery (<1 day), minimal moving parts.
  - ⚠️ Coupled directly to caller; harder to swap backend later.

### Variation B: Idiomatic / Modular (Recommended)
- **Core Strategy**: [Dedicated service layer with interface contracts]
- **Target Files**:
  - `src/services/TargetService.ts` [NEW]
  - `src/types/target.ts` [NEW]
  - `src/components/Target.tsx`
- **Dependencies**: None.
- **Pros & Cons**:
  - ✅ High testability, decoupled business rules, clean maintenance.
  - ⚠️ Requires 2 additional files.

### Variation C: Enterprise / Extensible
- **Core Strategy**: [Adapter pattern with event emitter / logging hooks]
- **Target Files**:
  - `src/core/adapters/TargetAdapter.ts` [NEW]
  - `src/core/events/dispatcher.ts`
- **Dependencies**: `eventemitter3` (optional)
- **Pros & Cons**:
  - ✅ Infinite extensibility, plugin-ready.
  - ⚠️ Higher cognitive load and boilerplate for simple use cases.

---

### 📊 Trade-Off Scorecard
| Metric | Variation A (Lean) | Variation B (Modular) | Variation C (Enterprise) |
| :--- | :---: | :---: | :---: |
| **Velocity** | 9/10 | 8/10 | 5/10 |
| **Maintainability** | 5/10 | 9/10 | 8/10 |
| **Risk / Blast Radius** | Low (3/10) | Low (2/10) | Medium (5/10) |
| **Verdict** | Quick Patch | **Recommended Baseline** | Over-engineered |
<!-- END_ANCHOR:PLAN_VARIATIONS -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/plan`, `/variants`, or when exploring how to build a feature.
- **In Workflow**: Runs immediately following **`B01-grill-me`**, turning the `DECISION_RECORD` into comparative architectural variations. Hands off to **`B03-spec-architect`** or **`B04-plan-synthesizer`** to lock the formal specification and golden plan.

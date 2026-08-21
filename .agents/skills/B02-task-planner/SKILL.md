---
name: B02-task-planner
description: Strategic task decomposer & roadmap architect. Breaks complex goals into atomic, low-cognitive-load milestones (<=2 files per task) with dependency ordering and built-in plan linter.
category: plan
aliases: [task-planner, decomposer, roadmap-architect, planner]
---

# Skill: B02-task-planner (Strategic Task Decomposer & Roadmap Architect)

**Objective**: Decompose high-level feature requirements, refactoring initiatives, and architecture decisions into small, atomic, dependency-aware execution steps. Prevent agent hallucinations, context exhaustion, and regressions by enforcing the **Low Cognitive Load Protocol** (≤2 files touched per task) and validating roadmaps with the self-contained plan linter.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines cognitive decomposition protocols with an automated static plan linter:

```
B02-task-planner/
├── SKILL.md                  # Decomposition protocol & cognitive load rules
├── scripts/
│   └── plan_linter.py        # Static plan linter & cognitive load validator
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `B02-task-planner/` directly into any `.agents/skills/` directory to enable deterministic, safe task roadmaps.

---

## 2. Core Operating Principles

1. **Ingest Before Planning**:
   - Never write a plan from a blank slate.
   - Always ingest the `DECISION_RECORD` from [`B01-grill-me`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/B01-grill-me) (locked UX, data models, edge cases, scope fences).
   - Ingest Category A discovery anchors:
     - [`A01-deep-scan`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A01-deep-scan) for repo architecture and language stack.
     - [`A04-dependency-mapper`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A04-dependency-mapper) for blast-radius reverse consumers.
     - [`A05-route-scanner`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A05-route-scanner) for existing URL/API endpoints.
     - [`A06-schema-scanner`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A06-schema-scanner) for database models and field names.

2. **The Low Cognitive Load Protocol**:
   - **Max 1–2 files per task**: An agent asked to modify 5+ files simultaneously will lose context or make subtle import errors. Each task must touch at most 1–2 files.
   - **Small diffs**: Tasks should aim for <50 lines of code change.
   - **Sequential progression**: Do not start Phase N+1 until Phase N has passed its verification criteria.

3. **Blast-Radius Accountability**:
   - If a task modifies an existing function signature, the planner MUST schedule downstream caller updates in subsequent tasks based on [`A04-dependency-mapper`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A04-dependency-mapper).

4. **Verifiable Definition of Done (DoD)**:
   - Every phase must conclude with an unambiguous, automated, or observable test gate (e.g. `pytest tests/test_user.py`, `npm run build`, `tsc --noEmit`).

---

## 3. The 4-Phase Decomposition Hierarchy

All plans are organized into a strict four-phase progression:

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Foundation & Types                                 │
│ (Data models, schemas, type definitions, configs)           │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 2: Core Logic & Services                              │
│ (Pure functions, domain business rules, service layer)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 3: Integration & Wiring                               │
│ (API endpoints, UI components, downstream blast consumers)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Phase 4: Verification & Quality Gate                        │
│ (End-to-end testing, failure recovery checks, linter audit) │
└─────────────────────────────────────────────────────────────┘
```

### Phase 1: Foundation & Types
- Define data contracts, database models ([`A06-schema-scanner`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A06-schema-scanner)), interfaces, and config keys first.
- Tag new files with `[NEW]` for easy identification.
- *DoD*: Type checking passes without compiler errors.

### Phase 2: Core Logic & Services
- Implement business functions and core algorithms in isolation.
- Keep functions pure and decoupled from framework controllers or UI templates.
- *DoD*: Unit tests for core logic execute and pass.

### Phase 3: Integration & Wiring
- Wire core services into API routes ([`A05-route-scanner`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A05-route-scanner)), controllers, or frontend views.
- Update downstream callers identified by [`A04-dependency-mapper`](file:///d:/Git_Work/Aether%20Agent/.agents/skills/A04-dependency-mapper) to prevent broken imports.
- *DoD*: Integration endpoints respond successfully with expected payloads.

### Phase 4: Verification & Quality Gate
- Run test suites, verify edge-case recovery (handling the "unhappy path" locked in `B01-grill-me`), and check build health.
- *DoD*: Full test suite green, linter clean, zero regressions.

---

## 4. Automated Plan Linter

`B02-task-planner` includes a self-contained static plan linter: `scripts/plan_linter.py`.

### How to Run:
```bash
python .agents/skills/B02-task-planner/scripts/plan_linter.py path/to/PLAN.md
```

### What it Enforces:
- **Phase sequencing**: Flags missing phase headers.
- **Cognitive Load Violation**: Flags any task that touches >2 source files.
- **File existence**: Warns if a referenced file does not exist on disk and is not marked `[NEW]`.
- **Definition of Done**: Warns if any phase lacks an explicit verification gate.

---

## 5. Output Format Standard

Generate the implementation plan using this structured template:

```markdown
<!-- CONTEXT_ANCHOR:TASK_PLAN -->
# Implementation Plan: [Feature / Task Name]

**Grounded References**:
- Decision Record: [`B01-grill-me`](file:///path/to/DECISION_RECORD.md)
- Blast Radius: [N consumers identified via A04]
- Schemas: [Target models via A06]

---

### Phase 1: Foundation & Types
- [ ] Task 1.1: Define schema models in `path/to/model.ts` [NEW]
- [ ] Task 1.2: Add type contracts in `path/to/types.ts`
- **Definition of Done**: Type checks pass (`npx tsc --noEmit`).

### Phase 2: Core Logic & Services
- [ ] Task 2.1: Implement business logic in `path/to/service.ts` [NEW]
- [ ] Task 2.2: Add unit tests in `path/to/service.test.ts` [NEW]
- **Definition of Done**: Unit tests pass (`npm test path/to/service.test.ts`).

### Phase 3: Integration & Wiring
- [ ] Task 3.1: Wire route handler in `path/to/routes.ts`
- [ ] Task 3.2: Update downstream caller in `path/to/caller.ts` (Blast radius)
- **Definition of Done**: Endpoint returns 200 OK for valid requests.

### Phase 4: Verification & Failure Recovery
- [ ] Task 4.1: Test unhappy paths (timeouts, rate limits, invalid inputs)
- [ ] Task 4.2: Run full regression test suite
- **Definition of Done**: All tests pass, build succeeds with exit code 0.
<!-- END_ANCHOR:TASK_PLAN -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/plan`, `/planner`, or when breaking down a complex goal.
- **In Workflow**: Runs immediately after **`B01-grill-me`**, turning the `DECISION_RECORD` into an atomic roadmap. Hands off directly to **`B03-failure-predictor`** for pre-flight risk auditing before code generation begins.

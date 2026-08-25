---
name: B05-task-executor
description: Atomic task decomposer & execution engine. Decomposes synthesized plans into strict low-cognitive-load tasks (<=2 files/task), tracking execution states and verifying phase Definitions of Done.
category: plan
aliases: [task-executor, task-planner, decomposer, execution-engine, roadmap-architect]
---

# Skill: B05-task-executor (Atomic Task Decomposer & Execution Engine)

**Objective**: Convert high-level synthesized plans from `B04-plan-synthesizer` and technical specifications from `B03-spec-architect` into small, atomic, dependency-aware execution steps. Enforce the **Low Cognitive Load Protocol** (≤2 files touched per task), track progressive task execution states (`[ ]` PENDING, `[-]` IN PROGRESS, `[x]` COMPLETED), and validate verifiable Definitions of Done before advancing phases.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines atomic decomposition and execution tracking protocols with an automated roadmap execution engine:

```
B05-task-executor/
├── SKILL.md                  # Decomposition protocol & cognitive load rules
├── scripts/
│   ├── task_executor.py     # Execution engine, state tracker & progress calculator
│   └── plan_linter.py       # Static plan linter & cognitive load validator
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `B05-task-executor/` directly into any `.agents/skills/` directory to enable safe, incremental task decomposition and execution.

---

## 2. Core Operating Principles

1. **Ingest Before Decomposing (Ensemble vs. Standalone)**:
   - **Ensemble Mode (Preferred)**:
     - Ingest `<!-- CONTEXT_ANCHOR:SYNTHESIZED_PLAN -->` from `B04-plan-synthesizer`.
     - Ingest `<!-- CONTEXT_ANCHOR:SYSTEM_SPEC -->` from `B03-spec-architect`.
   - **Standalone Mode (Autonomous Fallback)**:
     - If running without upstream skills, inspect repository manifests, existing routes, and data models directly using standard cognitive tools (`grep_search`, `view_file`) before drafting the roadmap.

2. **The Low Cognitive Load Protocol**:
   - **Max 1–2 files per task**: An agent asked to modify 5+ files simultaneously loses context and produces subtle regressions. Each task must touch at most 1–2 files.
   - **Small diffs**: Tasks should aim for <50 lines of code change.
   - **Strict sequential progression**: Never start Phase N+1 until Phase N has passed its automated verification gate.

3. **Active Task Execution Loop**:
   - Maintain deterministic task states:
     - `[ ]` **PENDING**: Scheduled but untouched.
     - `[-]` **IN_PROGRESS**: Active task currently being executed.
     - `[x]` **COMPLETED**: Passed definition of done, committed.
     - `[!]` **BLOCKED / FAILED**: Verification failed; requires targeted remediation.

4. **Verifiable Definition of Done (DoD)**:
   - Every phase must conclude with an unambiguous, automated, or observable test command (e.g. `pytest tests/test_user.py`, `npm run build`, `npx tsc --noEmit`).

5. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean relative paths (`src/...`).

---

## 3. The 4-Phase Decomposition Hierarchy

All roadmaps are structured into a strict four-phase progression:

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Foundation & Types                                 │
│ (Data models, schemas, type definitions, configs)           │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: Core Logic & Services                              │
│ (Pure functions, domain business rules, service layer)      │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: Integration & Wiring                               │
│ (API endpoints, UI components, downstream blast consumers)  │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: Verification & Failure Recovery Gate               │
│ (End-to-end testing, failure recovery checks, linter audit) │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Helper Scripts

`B05-task-executor` includes two self-contained helper scripts:

### A. Execution Engine & Progress Tracker:
```bash
python .agents/skills/B05-task-executor/scripts/task_executor.py path/to/ROADMAP.md
```
- Tracks task completion states (`[ ]` ➔ `[-]` ➔ `[x]`).
- Calculates completion percentage and phase breakdown.
- Emits structured JSON via `--json`.

### B. Static Plan Linter:
```bash
python .agents/skills/B05-task-executor/scripts/plan_linter.py path/to/ROADMAP.md
```
- Enforces the Low Cognitive Load Protocol (flags tasks touching >2 files).
- Warns if referenced files do not exist and are not marked `[NEW]`.
- Checks for missing Definition of Done criteria.

---

## 5. Output Format Standard

Generate execution roadmaps using this structured template:

```markdown
<!-- CONTEXT_ANCHOR:TASK_ROADMAP -->
# Execution Roadmap: [Feature / Target System]

**Context**: [Reference to Synthesized Golden Plan from B04]  
**Target Blast Radius**: [Estimated file footprint]

---

### Phase 1: Foundation & Types
- [ ] Task 1.1: Define schema models in `src/models/user.ts` [NEW]
- [ ] Task 1.2: Add type contracts in `src/types/user.ts`
- **Definition of Done**: `npx tsc --noEmit` exits with code 0.

### Phase 2: Core Logic & Services
- [ ] Task 2.1: Implement business logic in `src/services/UserService.ts` [NEW]
- [ ] Task 2.2: Add unit tests in `src/services/UserService.test.ts` [NEW]
- **Definition of Done**: `npm test src/services/UserService.test.ts` passes.

### Phase 3: Integration & Wiring
- [ ] Task 3.1: Wire route handler in `src/routes/user.ts`
- [ ] Task 3.2: Update caller component in `src/components/UserProfile.tsx`
- **Definition of Done**: Endpoint returns 200 OK for valid requests.

### Phase 4: Verification & Failure Recovery
- [ ] Task 4.1: Test unhappy paths (timeouts, rate limits, invalid inputs)
- [ ] Task 4.2: Run full regression test suite
- **Definition of Done**: All test suites green, exit code 0.
<!-- END_ANCHOR:TASK_ROADMAP -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/execute`, `/tasks`, `/roadmap`, or `/plan-executor`.
- **In Workflow**: Runs immediately following **`B04-plan-synthesizer`**. Translates the Golden Plan into atomic execution tasks. Hands off directly to **`B06-failure-predictor`** for pre-flight immune auditing before any code edits begin.

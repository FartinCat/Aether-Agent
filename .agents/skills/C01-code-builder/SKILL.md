---
name: C01-code-builder
description: Atomic implementation engine. Executes B05 execution roadmaps with small, surgical diffs (<=2 files, <50 lines/edit), zero regressions, and automated Definition of Done verification.
category: build
aliases: [code-builder, builder, implementer, atomic-coder, feature-builder]
---

# Skill: C01-code-builder (Atomic Code Implementation Engine)

**Objective**: Convert atomic tasks from `B05-task-executor` and technical contracts from `B03-spec-architect` into high-quality, production-ready code. Enforce the **Atomic Edit Protocol**: execute one task at a time, touch at most 1–2 files per edit, keep diffs small (<50 lines), preserve existing context and comments, and verify the phase's Definition of Done before advancing.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines disciplined surgical coding protocols with an automated diff and cognitive load monitor:

```
C01-code-builder/
├── SKILL.md                  # Atomic implementation protocol & surgical edit rules
├── scripts/
│   └── diff_guard.py         # Static diff analyzer & cognitive load monitor
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `C01-code-builder/` directly into any `.agents/skills/` directory to enable reliable, regression-free code implementation.

---

## 2. Core Operating Principles

1. **The Atomic Edit Protocol**:
   - **One Task at a Time**: Never attempt to implement multiple roadmap tasks in a single burst.
   - **Max 1–2 Files per Edit**: Confine code changes strictly to the files scheduled in the task.
   - **Small, Focused Diffs**: Aim for <50 lines of code change per step. Large file overwrites cause token exhaustion, lost functions, and hallucinated imports.

2. **Context & Documentation Preservation**:
   - **Never wipe existing comments**: Preserve all existing docstrings, explanatory comments, and architectural notes unrelated to the task.
   - **Surgical edits over full replacements**: Use targeted replacement tools rather than completely overwriting existing source files.

3. **Verification Before Advancement**:
   - After applying changes for a task, immediately execute the verification command specified in the phase's Definition of Done (e.g. `npm test`, `pytest`, `tsc --noEmit`).
   - If tests or type-checks fail, pause and resolve the issue immediately. Never move to the next task on a broken build.

4. **Ingest Before Building (Ensemble vs. Standalone)**:
   - **Ensemble Mode (Preferred)**:
     - Ingest `<!-- CONTEXT_ANCHOR:TASK_ROADMAP -->` from `B05-task-executor`.
     - Ingest `<!-- CONTEXT_ANCHOR:SYSTEM_SPEC -->` from `B03-spec-architect`.
     - Ingest `<!-- CONTEXT_ANCHOR:FAILURE_PREDICTION -->` from `B06-failure-predictor` (heed identified risk mitigations).
   - **Standalone Fallback**:
     - If invoked independently on a single file or feature, read the target file and adjacent types directly before proposing surgical modifications.

5. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean relative paths (`src/...`).

---

## 3. The 4-Step Implementation Loop

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Pre-Check & Blast Assessment                        │
│ (Inspect target file, verify types, heed B06 risk gates)    │
├─────────────────────────────────────────────────────────────┤
│ Step 2: Surgical Code Modification                          │
│ (Apply targeted diff, max 1-2 files, preserve comments)     │
├─────────────────────────────────────────────────────────────┤
│ Step 3: Run Diff Guard & Verification Gate                  │
│ (Run diff_guard.py, execute compiler/test DoD command)      │
├─────────────────────────────────────────────────────────────┤
│ Step 4: Task Progress Update & Commit Readiness             │
│ (Mark task [x] in B05 roadmap, ready for atomic commit)     │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Helper Script

`C01-code-builder` includes a self-contained cognitive load monitor: `scripts/diff_guard.py`.

### How to Run:
```bash
# Audit active git changes for size and file limits:
python .agents/skills/C01-code-builder/scripts/diff_guard.py

# Check a single modified file for bracket/syntax balance:
python .agents/skills/C01-code-builder/scripts/diff_guard.py --file src/services/UserService.ts
```

### What it Enforces:
- Flags any edit touching >2 files in a single task.
- Warns if lines changed exceeds the atomic threshold (>80 lines).
- Verifies bracket and syntax balance to prevent truncated file writes.
- Supports `--json` and `--root` parameters.

---

## 5. Output Format Standard

When completing a code implementation task, generate the **Implementation Record**:

```markdown
<!-- CONTEXT_ANCHOR:CODE_IMPLEMENTATION -->
### 🛠️ Implementation Record: [Task ID & Name]

- **Target Files**:
  - `src/services/UserService.ts` (+32, -4)
  - `src/types/user.ts` (+12, -0)
- **DoD Verification Command**: `npx tsc --noEmit && npm test src/services/UserService.test.ts`
- **Result**: ✅ All type checks and tests passed (exit code 0).

#### Summary of Changes:
1. Implemented `UserService.getUserById` with null-check safeguard.
2. Added `UserResponse` interface contract matching `B03-spec-architect`.
3. Added timeout boundary (5000ms) as recommended by `B06-failure-predictor`.

**Roadmap State**: Task 2.1 marked `[x]` COMPLETED.
<!-- END_ANCHOR:CODE_IMPLEMENTATION -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/build`, `/implement`, `/code`, or when executing an approved task.
- **In Workflow**: Runs immediately after **`B06-failure-predictor`**. Takes scheduled tasks from **`B05-task-executor`**, applies surgical edits, verifies Definitions of Done, and hands off to **Category D (Test & Quality)** and **Category E (Review & Security)**.

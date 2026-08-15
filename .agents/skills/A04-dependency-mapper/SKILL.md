---
name: A04-dependency-mapper
aliases:
  - blast-radius-scanner
  - import-graph
description: AST-based import/export graph and blast-radius analyzer. Traces upstream consumers and downstream dependencies of any file to prevent silent regressions during refactors.
category: scan
---

# Skill: A04-dependency-mapper (Blast-Radius & Import Graph Scanner)

> **Core Purpose**: Prevent the "Silent Refactor Crash". When modifying a file, this skill identifies every other file that imports it, calculates the blast-radius risk, and warns you to update all consumer files simultaneously.

---

## 1. Skill Package Structure (Self-Contained)

This skill packages its own lightweight, zero-dependency import crawler within its own folder:

```
A04-dependency-mapper/
├── SKILL.md                  # Blast-radius protocol & refactoring guidelines
├── scripts/
│   └── scan_imports.py       # Pure standard-library import & reverse-dependency crawler (<100ms)
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `A04-dependency-mapper/` into any `.agents/skills/` directory to instantly protect against refactoring regressions.

---

## 2. Core Operating Principles

1. **Never Edit in Isolation**: If a file has 3 or more consumers, changing its exported function signatures, return types, or exported constants without updating those consumers will break the build.
2. **Blast-Radius Risk Tiers**:
   - **LOW (0 consumers)**: Leaf node or entrypoint. Safe to modify with isolated testing.
   - **MEDIUM (1–2 consumers)**: Targeted impact. Inspect the 1–2 callers before finalizing changes.
   - **HIGH (3–5 consumers)**: Significant surface. Any signature change must be accompanied by updates to all callers.
   - **CRITICAL (6+ consumers)**: Core shared primitive. Treat as a breaking API change. Consider adding backwards-compatible adapters or updating all consumers in a single atomic commit.
3. **Circular Import Detection**: Actively detect A -> B -> A import loops that cause runtime `undefined` errors or memory leaks.

---

## 3. The 3-Step Blast Radius Protocol

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Target File Identification                          │
│ (Specify the file you intend to create, edit, or refactor)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 2: Execute Dependency Graph Crawler                    │
│ (Run internal helper: python scan_imports.py <target_file>) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 3: Impact Analysis & Co-Edit Planning                  │
│ (Generate Blast Radius Warning & list of consumer files)    │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Target File Identification
Identify the target file that is about to be modified (e.g. `src/services/auth.ts`, `utils/date.py`).

### Step 2: Execute Dependency Graph Crawler
Run the skill's self-contained script:
```bash
python "<path_to_skill>/scripts/scan_imports.py" "path/to/target_file"
```
In `<100ms`, the script returns a compact JSON summary containing:
- `imported_by`: All files in the repository that import this file.
- `internal_dependencies`: All internal files imported by this file.
- `circular_dependencies`: Any detected cyclic import loops.
- `blast_radius_risk`: `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.

### Step 3: Impact Analysis & Co-Edit Planning
Review the consumer list:
- If `imported_by` is non-empty, list each consumer and the specific functions they import.
- Formulate a co-edit plan: *"Modifying function `X` in target file requires corresponding updates to files `A`, `B`, and `C`."*

---

## 4. Output Modes

### Mode A: Standalone Blast-Radius Impact Warning
*Use this when invoked directly by the user or before refactoring.*

```markdown
## 💥 Blast-Radius Report: `src/utils/formatDate.ts`

### 1. Risk Assessment
- **Risk Level**: 🔴 **HIGH** (4 consumer files detected)
- **Safe to Edit Directly**: ⚠️ **NO** — Requires co-editing downstream consumers.

### 2. Consumer Files (Files That Will Break If Signature Changes)
The following files import `formatDate.ts`:
1. [`src/components/UserCard.tsx`](file:///path/to/file#L12) — imports `{ formatDate }`
2. [`src/routes/invoices.ts`](file:///path/to/file#L8) — imports `{ formatDate }`
3. [`src/reports/exportCsv.ts`](file:///path/to/file#L5) — imports `{ formatDate }`
4. [`src/views/Dashboard.tsx`](file:///path/to/file#L18) — imports `{ formatDate }`

### 3. Downstream Dependencies (What This File Relies On)
- `date-fns` (external package)
- `src/constants/locales.ts` (internal)

### 4. Circular Import Check
- ✅ No circular dependency loops detected.

### 5. Recommended Refactoring Strategy
- If changing parameter types in `formatDate()`, stage simultaneous updates to all 4 consumer files listed above to maintain build integrity.
```

### Mode B: Ensemble Machine Context Anchor
*Use this when feeding into `Category B (Planner)` or `Category E (Antibug)`.*

```markdown
<!-- CONTEXT_ANCHOR:DEPENDENCY_MAP -->
{
  "target_file": "src/utils/formatDate.ts",
  "blast_radius_risk": "HIGH",
  "consumer_count": 4,
  "affected_files": [
    "src/components/UserCard.tsx",
    "src/routes/invoices.ts",
    "src/reports/exportCsv.ts",
    "src/views/Dashboard.tsx"
  ],
  "co_edit_required": true
}
<!-- /CONTEXT_ANCHOR -->
```

---

## 5. Invocation & Workflow Integration
- **Manual**: Run before refactoring, deleting, or renaming any core utility (`/dependency-mapper <filename>`).
- **In Workflow**: Automatically runs during `Category B (Planner)` when scoping multi-file tasks, and during `Category E (Antibug)` to verify that bug fixes do not cause regressions in calling modules.

---
name: C02-refactor-pro
description: Surgical behavior-preserving refactoring engine. Eliminates technical debt, unused/dead code, and anti-patterns without breaking public contracts or introducing regressions.
category: build
aliases: [refactor-pro, refactorer, code-cleaner, dead-code-remover, modernizer]
---

# Skill: C02-refactor-pro (Surgical Behavior-Preserving Refactoring Engine)

**Objective**: Execute safe, targeted refactoring initiatives. Eliminate technical debt, dead code, duplicated logic, obsolete comments, and code smells without modifying external API signatures, database schemas, or observable system behavior. Every refactoring operation must guarantee zero regressions.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines behavior-preserving refactoring patterns with an automated dead code and technical debt auditor:

```
C02-refactor-pro/
├── SKILL.md                  # Refactoring protocol & contract invariance rules
├── scripts/
│   └── dead_code_finder.py   # Static unused import & dead code scanner
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `C02-refactor-pro/` directly into any `.agents/skills/` directory to enable deterministic, safe code refactoring.

---

## 2. Core Operating Principles

1. **The Behavior-Preservation Law**:
   - **Never mix refactoring with feature development**: Refactorings must solely improve code structure, readability, and performance. New features or behavioral changes must be handled in separate atomic tasks.
   - **Green-Before, Green-After**: The existing test suite must pass *before* any refactoring begins, and must pass *after* the refactor is completed.

2. **Public Contract Invariance**:
   - Exported function signatures, method names, parameter orders, and return types must remain 100% invariant.
   - If a function signature must be modernized, schedule a deprecation wrapper rather than a breaking deletion.

3. **Blast-Aware Pruning**:
   - Before pruning a helper function or constant, verify that zero external files import it.
   - Strip dead imports and commented-out code blocks that clutter active files.

4. **Preserve Surrounding Docstrings & Comments**:
   - Clean obsolete commented code blocks, but **never wipe active docstrings**, business logic explanations, or architectural notes.

5. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean relative paths (`src/...`).

---

## 3. The 4 Refactoring Patterns Standard

```
┌─────────────────────────────────────────────────────────────┐
│ Pattern 1: Dead Code & Import Pruning                       │
│ (Remove unused imports, dead constants, commented blocks)   │
├─────────────────────────────────────────────────────────────┤
│ Pattern 2: Extract Method & Pure Function Isolation         │
│ (Break 100+ line monoliths into focused, pure helpers)      │
├─────────────────────────────────────────────────────────────┤
│ Pattern 3: Cognitive Complexity Reduction                   │
│ (Replace deep nested if/else with guard clauses & returns)  │
├─────────────────────────────────────────────────────────────┤
│ Pattern 4: Contract-Preserving Internal Modernization       │
│ (Upgrade async/await, replace any types with typed models)  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Helper Script

`C02-refactor-pro` includes a self-contained debt scanner: `scripts/dead_code_finder.py`.

### How to Run:
```bash
python .agents/skills/C02-refactor-pro/scripts/dead_code_finder.py path/to/target.ts
```

### Script Capabilities:
- Identifies unused imported symbols in TypeScript/JavaScript and Python.
- Scans for dead commented-out code blocks (≥3 lines).
- Detects unreachable statements following return or throw statements.
- Emits clean human recommendations or structured JSON via `--json`.

---

## 5. Output Format Standard

When completing a refactoring task, generate the **Refactoring Report**:

```markdown
<!-- CONTEXT_ANCHOR:REFACTOR_REPORT -->
### 🧹 Refactoring Report: [Target Module / File]

- **Target File**: `src/services/PaymentService.ts`
- **Pre-Refactor Verification**: ✅ All unit tests green (14 passed).
- **Post-Refactor Verification**: ✅ All unit tests green (14 passed).

#### Changes Applied:
1. **Pruned Dead Code**: Removed 3 unused imports (`axios`, `ConfigOptions`, `LegacyFormatter`).
2. **Reduced Nesting**: Converted 4-level nested `if/else` block into early return guard clauses.
3. **Contract Preservation**: Preserved exact `processPayment(orderId, amount)` signature and return types.
4. **Cleaned Artifacts**: Removed 12 lines of legacy commented-out code.

**Regressions Detected**: 0 (Zero external callers affected).
<!-- END_ANCHOR:REFACTOR_REPORT -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/refactor`, `/clean-code`, `/prune`, or `/debt-cleanup`.
- **In Workflow**: Runs in **Category C (Build & Implementation)** after initial implementation or during dedicated technical debt cleanup cycles. Coordinates with **Category D (Test & Quality)** to ensure test suites remain continuously green.

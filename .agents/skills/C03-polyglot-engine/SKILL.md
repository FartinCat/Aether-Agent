---
name: C03-polyglot-engine
description: Multi-language idiomatic code specialist. Enforces native idioms, type safety, error wrapping, and ecosystem conventions across TypeScript, Python, Rust, Go, and SQL.
category: build
aliases: [polyglot-engine, language-specialist, idiomatic-code, code-standards, polyglot]
---

# Skill: C03-polyglot-engine (Polyglot Idiomatic Code Specialist)

**Objective**: Ensure that all generated or refactored code across TypeScript, Python, Go, Rust, and SQL adheres strictly to native language conventions and best practices. Eliminate non-idiomatic code (such as Java-style code written in Python, or JavaScript habits leaking into Rust/Go) and enforce zero-hallucinated third-party dependencies.

---

## 1. Skill Package Structure (Self-Contained)

This skill combines ecosystem-specific idiomatic style guides with an automated static idiom auditor:

```
C03-polyglot-engine/
├── SKILL.md                  # Language conventions & idiomatic coding rules
├── scripts/
│   └── idiom_checker.py      # Multi-language static idiom & convention auditor
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `C03-polyglot-engine/` directly into any `.agents/skills/` directory to enforce ecosystem-native code quality.

---

## 2. Core Operating Principles

1. **Native Ecosystem Fidelity**:
   - Write code that reads like it was authored by a seasoned specialist in that language, rather than a generic translation:
     - **TypeScript**: Strict type boundaries, no `any`, discriminated unions, strict null handling, async/await with typed Promises.
     - **Python**: PEP 8 compliance, explicit type annotations, list/dict comprehensions, dataclasses, context managers (`with`).
     - **Go**: Explicit error handling (`if err != nil`), `context.Context` propagation, idiomatic channels/goroutines, table-driven tests.
     - **Rust**: Ownership/borrowing idioms, pattern matching on `Result<T, E>` and `Option<T>`, zero production `unwrap()`.
     - **SQL**: Explicit column selection (no `SELECT *`), parameterized queries, indexed join columns, atomic transactions.

2. **Zero Hallucinated Dependencies**:
   - Always prefer standard library solutions. If an external package is needed, verify that it already exists in the project manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) before importing it.

3. **Defensive Error Handling**:
   - Never suppress errors silently with empty catch blocks or bare `except:`.
   - Propagate errors with helpful context and domain-specific error codes.

4. **The Independence Law**:
   - Zero raw absolute system paths (`d:\`, `file:///`, `C:\`). All file references must use clean relative paths (`src/...`).

---

## 3. Language Idiom Matrix

```
┌─────────────────────────────────────────────────────────────┐
│ TypeScript / JavaScript                                     │
│ • No 'any' (use 'unknown' or interfaces)                    │
│ • Strict equality ('===') only                              │
│ • Discriminated unions for multi-state responses            │
├─────────────────────────────────────────────────────────────┤
│ Python                                                      │
│ • Type hints on all public functions                        │
│ • Never use mutable defaults (def f(x=[]) is forbidden)     │
│ • Context managers for I/O and locks                        │
├─────────────────────────────────────────────────────────────┤
│ Go                                                          │
│ • Immediate error checking (if err != nil { return err })   │
│ • Accept interfaces, return concrete structs                │
├─────────────────────────────────────────────────────────────┤
│ Rust                                                        │
│ • Propagate errors via '?' operator                         │
│ • Prefer references over unnecessary .clone() calls         │
├─────────────────────────────────────────────────────────────┤
│ SQL                                                         │
│ • Parameterized inputs (prevent SQL injection)              │
│ • Explicit SELECT column lists                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Helper Script

`C03-polyglot-engine` includes a self-contained idiom auditor: `scripts/idiom_checker.py`.

### How to Run:
```bash
python .agents/skills/C03-polyglot-engine/scripts/idiom_checker.py path/to/source.ts
```

### Script Capabilities:
- Audits `.ts`, `.tsx`, `.py`, `.go`, `.rs`, and `.sql` source files.
- Flags non-idiomatic patterns (`any` types, bare excepts, mutable defaults, unsafe unwraps, `SELECT *`).
- Calculates an Idiom Score (0–100) and required fixes.
- Supports `--json` output for automated tooling.

---

## 5. Output Format Standard

When completing a language-specific audit or implementation, generate the **Idiomatic Verification Report**:

```markdown
<!-- CONTEXT_ANCHOR:IDIOMATIC_VERIFICATION -->
### 💎 Idiomatic Verification Report: [File Name]

- **Target File**: `src/services/AnalyticsEngine.ts`
- **Idiom Score**: 95/100 (EXCELLENT)
- **Language Stack**: TypeScript 5.x

#### Standards Confirmed:
1. ✅ **Strict Typing**: Zero `any` types detected; all input arguments and return promises strictly typed.
2. ✅ **Equality**: All comparisons use strict equality (`===`).
3. ✅ **Error Handling**: Custom `AnalyticsError` class propagated with typed error codes.
4. ✅ **Dependencies**: Zero unapproved external dependencies introduced.
<!-- END_ANCHOR:IDIOMATIC_VERIFICATION -->
```

---

## 6. Invocation & Workflow Integration
- **Manual**: Triggered via `/idioms`, `/polyglot`, `/standards`, or `/lang-check`.
- **In Workflow**: Operates within **Category C (Build & Implementation)** alongside `C01-code-builder` and `C02-refactor-pro` to ensure that all written code adheres to ecosystem-native standards before hand-off to **Category D (Test & Quality)**.

---
name: A03-validator
aliases:
  - evidence-validator
  - research-loop
description: Pre-execution evidence and contradiction validator. Audits user requests, specs, and proposed plans against active code and dependency manifests to eliminate hallucinations and false assumptions before work begins.
category: scan
---

# Skill: A03-validator (Evidence & Contradiction Validator)

> **Alias**: `evidence-validator` / `research-loop`  
> **Mandate**: **Evidence before output. Always.** No agent may skip to a final plan, fix, or architectural change without first verifying that its assumptions match the active filesystem.

---

## 1. Skill Package Structure (Self-Contained)

This skill operates purely through systematic fact-checking and contradiction detection using standard IDE inspection tools:

```
A03-validator/
├── SKILL.md                  # Pre-execution validation protocol & contradiction rules
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `A03-validator/` into any `.agents/skills/` directory to instantly equip an agent with pre-execution grounding and hallucination prevention.

---

## 2. Core Operating Principles

1. **Verify, Never Assume**: When a task says *"Add feature X to service Y"*, do not assume service Y is configured as expected. Verify that service Y exists, check how it is implemented, and confirm its dependencies.
2. **Contradiction Detection**: Actively hunt for discrepancies between what documentation/prompts claim and what the code actually does.
3. **Strict Exclusion Rule**:
   Never treat agent infrastructure (e.g. `.agent/`, `.agents/`, `.git/`, `node_modules/`, `target/`, `.venv/`) as project evidence. They are operational tooling, not the application under validation.
4. **Universal Evidence Sources**:
   - **Active Code**: Source files (`.ts`, `.py`, `.rs`, `.go`, `.html`, `.css`, etc.).
   - **Manifests**: Dependency manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`).
   - **Config & Environment**: Configuration files (`.env.example`, `docker-compose.yml`, `tsconfig.json`).
   - **Specs & Docs**: Existing documentation (`docs/`, `README.md`, specs).
   - **Version History**: Git commit history (`git log -n 5`) to understand recent context.

---

## 3. The 4-Step Evidence Validation Protocol

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Claim & Assumption Extraction                       │
│ (Extract all facts, files, libraries, and types assumed)    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 2: Grounding & Existence Verification                  │
│ (Inspect filesystem to prove or disprove each assumption)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 3: Contradiction & Gap Audit                           │
│ (Flag conflicts, uninstalled packages, missing configs)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 4: Grounding Confidence & Validation Sheet             │
│ (Emit Confidence Score HIGH/MED/LOW + Verified Facts)       │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Claim & Assumption Extraction
Break down the incoming prompt, spec, or proposal into testable claims:
- **File Claims**: *"Modifying `src/auth/service.ts`"* -> Does this file exist?
- **Library Claims**: *"Using `bcrypt` for hashing"* -> Is `bcrypt` listed in dependencies?
- **Architecture Claims**: *"Extending the existing REST endpoint"* -> Is it actually REST or GraphQL?
- **Environment Claims**: *"Using `DATABASE_URL`"* -> Is it declared in `.env.example`?

### Step 2: Grounding & Existence Verification
Check the physical reality of the repository:
- Check manifest files to confirm package existence and exact versions.
- Check target file paths and symbols using search tools.
- Check environment templates for required keys.

### Step 3: Contradiction & Gap Audit
Identify any gaps:
- **Direct Contradiction**: Claim says one thing, code does another (e.g. prompt assumes JWT, code uses session cookies).
- **Missing Dependency**: Code or plan requires a package not yet installed.
- **Missing Secret / Config**: Code relies on environment variables not documented in `.env.example`.
- **Architectural Drift**: Proposed plan violates established patterns found during `A01-deep-scan`.

### Step 4: Grounding Confidence Score
Assign a confidence score based on physical evidence:
- **HIGH**: All referenced files, dependencies, and APIs exist. Zero contradictions found. Fully grounded to proceed.
- **MEDIUM**: Most dependencies exist, but minor gaps or ambiguous configurations were detected. Can proceed with explicit assumptions stated.
- **LOW**: Core files or packages do not exist. Significant contradictions detected. Must halt and request user clarification before planning or coding.

---

## 4. Output Modes

### Mode A: Standalone Developer Validation Sheet
*Use this when invoked directly by the user or before drafting a major proposal.*

```markdown
## 🛡️ Evidence Validation Report: [Task / Feature Name]

### 1. Grounding Assessment
- **Confidence Score**: [HIGH / MEDIUM / LOW]
- **Verdict**: [Ready to Plan / Needs Configuration / Blocked by Contradictions]

### 2. Verified Facts (Grounded in Code)
- ✅ Confirmed file exists: [`src/auth/handler.ts`](file:///path/to/file)
- ✅ Dependency confirmed: `jsonwebtoken@9.0.2` in `package.json`

### 3. Contradictions & Gaps Found
- ❌ **Contradiction**: Prompt assumes PostgreSQL, but `prisma/schema.prisma` is configured for SQLite (`provider = "sqlite"`).
- ⚠️ **Missing Prerequisite**: `REFRESH_TOKEN_SECRET` is not documented in `.env.example`.

### 4. Recommended Action
- [Explicit step to resolve gap, e.g. "Update schema to postgres or proceed using SQLite"]
```

### Mode B: Ensemble Machine Context Anchor
*Use this when running as Step 2 of a pipeline (between `A01-deep-scan` and `Category B: Planner`).*

```markdown
<!-- CONTEXT_ANCHOR:VALIDATOR -->
{
  "grounding_confidence": "HIGH",
  "verified_files": ["src/routes/api.ts", "package.json"],
  "contradictions": [],
  "missing_dependencies": [],
  "unstated_assumptions": ["Assumes Redis is running locally for cache"],
  "ready_for_planning": true
}
<!-- /CONTEXT_ANCHOR -->
```

---

## 5. Invocation & Workflow Integration
- **Manual**: Run before planning any non-trivial change or refactor (`/validator`).
- **In Workflow**: Runs immediately after `A01-deep-scan` and immediately before `Category B (Planner)`. Ensures downstream planning agents never hallucinate or build on false premises.
